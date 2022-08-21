#!/bin/bash
/bin/nfcapd -D -p 9995 -s 500 -l /tmp/nfcap_files/ -t 10
python3 publish.py