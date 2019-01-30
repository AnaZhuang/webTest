#@Package[org.onecloud.ocean.demo.oceansql]
#@Persistence[database="sampledb"]

CREATE TABLE if not exists Employee(
    EmpId INT UNSIGNED,
    EmpName VARCHAR(50) NULL,
    Sex VARCHAR(6) NULL,

    BirthDay DATE NULL,
    PRIMARY KEY(EmpId)
)DEFAULT CHARACTER SET UTF8;