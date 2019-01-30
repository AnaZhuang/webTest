#@Persistence[database="sampledb"]
create sampledb;

CREATE TABLE customer (
	customer_id INT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	sex CHAR(1) NOT NULL DEFAULT 'M',
	birthday DATE NOT NULL,
	
	PRIMARY KEY(customer_id)
)DEFAULT CHARACTER SET UTF8;
