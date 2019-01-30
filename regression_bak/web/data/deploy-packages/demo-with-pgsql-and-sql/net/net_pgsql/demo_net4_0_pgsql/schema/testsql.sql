

SET search_path = "public", pg_catalog;

-- Definition

-- 
DROP TABLE "public"."hello";
CREATE TABLE "public"."hello" (
    "ID" integer NOT NULL,
    "Name" character varying(100),
    CONSTRAINT "hello_pkey" PRIMARY KEY ("ID")
) WITHOUT OIDS;

COPY "hello" FROM stdin;
1	addbcc
2	clouder
\.

-- Indexes

CREATE UNIQUE INDEX hello_pkey ON hello USING btree ("ID");
