DROP DATABASE IF EXISTS pmacct;
CREATE DATABASE pmacct;

USE pmacct;

CREATE USER 'pmacct'@'%' IDENTIFIED WITH mysql_native_password BY 'arealsmartpwd';
GRANT ALL PRIVILEGES ON pmacct.* TO pmacct@'%';

DROP TABLE IF EXISTS acct; 
CREATE TABLE acct (
    ip_src CHAR(45) NOT NULL,
    ip_dst CHAR(45) NOT NULL,
    port_src INT(2) UNSIGNED NOT NULL,
    port_dst INT(2) UNSIGNED NOT NULL,
    tcp_flags INT(4) UNSIGNED NOT NULL,
    ip_proto CHAR(6) NOT NULL,
	packets INT UNSIGNED NOT NULL,
	bytes BIGINT UNSIGNED NOT NULL,
	stamp_inserted DATETIME NOT NULL,
	stamp_updated DATETIME,
    PRIMARY KEY (ip_src, ip_dst, port_src, port_dst, ip_proto, stamp_inserted)
);