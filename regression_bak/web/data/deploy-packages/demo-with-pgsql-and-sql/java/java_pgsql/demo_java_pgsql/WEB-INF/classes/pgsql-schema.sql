/*
 * The following table is used for demonstrating Ocean Driver usage.
 */

CREATE TABLE customer (
	customer_id serial,
	name VARCHAR(50) NOT NULL,
	sex CHAR(1) NOT NULL DEFAULT 'M',
	birthday DATE NOT NULL,
	PRIMARY KEY(customer_id)
);


#@Package[org.onecloud.ocean.demo.oceansql]
#@Persistence[database="sampledb"]
CREATE TABLE if not exists Employee(
    EmpId INT,
    EmpName VARCHAR(50) NULL,
    Sex VARCHAR(6) NULL,
    BirthDay DATE NULL,
    PRIMARY KEY(EmpId)
);