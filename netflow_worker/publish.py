import subprocess
import time
from typing import Union
from pathlib import Path, PosixPath
from typing import List
from loguru import logger
from os import environ
import csv, io

from modules.rabbitmq import Publisher

NETFLOW_DIRECTORY = "/tmp/nfcap_files"
#NETFLOW_DIRECTORY = "data/"

TOTAL_FLOWS_PROCESSED = 0

def find_netflow_files(directory: str) -> List[PosixPath]:
    logger.info("Finding netflow binary files")
    files = []
    for p in Path(directory).iterdir():
        if not p.is_file():
            continue

        if p.name.startswith("nfcapd.current"):
            continue

        files.append(p.resolve())
    return files

def decode_nfcap_binary_file(path: Union[PosixPath, str]) -> List[dict]:
    logger.info("Attempting to gather data using nfdump")
    if not path.is_file():
        return []

    nfdump = subprocess.run(["nfdump", "-r", path, "-o", "csv", "-q"], capture_output=True, text=True)
    if nfdump.returncode != 0 or not nfdump.stdout:
        logger.error("Return code is either != 0 or no output from nfdump to perform further processing")
        return []

    if len(nfdump.stdout) <= 17:
        return []

    headers = "ts,te,td,sa,da,sp,dp,pr,flg,fwd,stos,ipkt,ibyt,opkt,obyt,in,out,sas,das,smk,dmk,dtos,dir,nh,nhb,svln,dvln,ismc,odmc,idmc,osmc,mpls1,mpls2,mpls3,mpls4,mpls5,mpls6,mpls7,mpls8,mpls9,mpls10,cl,sl,al,ra,eng,exid,tr"
    data = f"{headers}\n{nfdump.stdout}"
    formatted_data = format_netflow_output(data)
    return formatted_data

def format_netflow_output(nfdump_str: str, lines: int = 5, return_json: bool = True) -> List[dict]:
    global TOTAL_FLOWS_PROCESSED

    reader = csv.DictReader(io.StringIO(nfdump_str))
    flows = list(reader)
    TOTAL_FLOWS_PROCESSED += len(flows)
    return list(flows)

def cleanup(files: List[PosixPath]) -> None:
    logger.info("Cleaning up files")
    for file in files:
        if not file.is_file():
            logger.error(f"Unable to remove {file.name} to due to not being a file")
            continue

        logger.debug(f"Cleaning up file: {file.name}")
        file.unlink()
    logger.info("Finished cleaning up files")

def process():
    global TOTAL_FLOWS_PROCESSED

    files_to_process = find_netflow_files(directory=NETFLOW_DIRECTORY)
    if not files_to_process:
        logger.info("No files found to process...")
        return

    publisher = Publisher(config={"host": environ["RABBITMQ_HOST"], "username": environ["RABBITMQ_USERNAME"], "password": environ["RABBITMQ_PASSWORD"]})
    publisher.connect()
    for file_path in files_to_process:
        logger.info(f"Processing netflow binary file ({file_path.name})")
        decoded_json = decode_nfcap_binary_file(path=file_path)

        flows_published = 0
        for flow in decoded_json:
            publisher.publish(flow)
            flows_published += 1

        logger.info(f"Flows published to RabbitMQ: {flows_published}")

    publisher.close()
    cleanup(files=files_to_process)
    logger.info(f"Total flows processed: {TOTAL_FLOWS_PROCESSED}")
    TOTAL_FLOWS_PROCESSED = 0

if __name__ == "__main__":
    while True:
        try:
            process()
        except Exception as error:
            logger.error(error)

        logger.info("Sleeping for 5 seconds...")
        time.sleep(5)