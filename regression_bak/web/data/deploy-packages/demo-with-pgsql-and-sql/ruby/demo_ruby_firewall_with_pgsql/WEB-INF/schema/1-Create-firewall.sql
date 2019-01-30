
SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--

CREATE TABLE batches (
    id integer NOT NULL,
    "desc" character varying(255),
    result character varying(255),
    zone_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
--

CREATE SEQUENCE batches_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE batches_id_seq OWNED BY batches.id;


--
--

CREATE TABLE check_types (
    id integer NOT NULL,
    name character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
--

CREATE SEQUENCE check_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--

ALTER SEQUENCE check_types_id_seq OWNED BY check_types.id;


--
--

CREATE TABLE deploy_batches (
    id integer NOT NULL,
    software_id integer,
    state integer DEFAULT 1,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);



--
--

CREATE SEQUENCE deploy_batches_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE deploy_batches_id_seq OWNED BY deploy_batches.id;


--

CREATE TABLE deploy_errors (
    id integer NOT NULL,
    name character varying(255),
    description character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);



--

CREATE SEQUENCE deploy_errors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--

ALTER SEQUENCE deploy_errors_id_seq OWNED BY deploy_errors.id;


--

CREATE TABLE deploy_logs (
    id integer NOT NULL,
    deploy_batch_id integer,
    machine_package_id integer,
    deploy_error_id integer,
    machine_deploy_state_id integer,
    upload_file_at timestamp without time zone,
    cause character varying(255),
    deploy boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE deploy_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE deploy_logs_id_seq OWNED BY deploy_logs.id;


--

CREATE TABLE deploy_states (
    id integer NOT NULL,
    name character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE deploy_states_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE deploy_states_id_seq OWNED BY deploy_states.id;


--

CREATE TABLE fs (
    id integer NOT NULL,
    sn integer,
    name character varying(255),
    package_id integer,
    content_type character varying(255),
    destine character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    md5sum character varying(255)
);


--

CREATE SEQUENCE fs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE fs_id_seq OWNED BY fs.id;


--

CREATE TABLE logs (
    id integer NOT NULL,
    batch_id integer,
    ip character varying(255),
    success boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE logs_id_seq OWNED BY logs.id;


--

CREATE TABLE machine_deploy_states (
    id integer NOT NULL,
    name character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE machine_deploy_states_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE machine_deploy_states_id_seq OWNED BY machine_deploy_states.id;


--

CREATE TABLE machines (
    id integer NOT NULL,
    ip character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE machines_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE machines_id_seq OWNED BY machines.id;


--

CREATE TABLE machines_packages (
    id integer NOT NULL,
    machine_id integer,
    package_id integer,
    software_id integer,
    installed boolean DEFAULT false,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE machines_packages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE machines_packages_id_seq OWNED BY machines_packages.id;


--

CREATE TABLE management_servers (
    id integer NOT NULL,
    ip character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE management_servers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE management_servers_id_seq OWNED BY management_servers.id;


--

CREATE TABLE packages (
    id integer NOT NULL,
    version integer,
    software_id integer,
    publish boolean DEFAULT false,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deploy_state_id integer DEFAULT 1
);


--

CREATE SEQUENCE packages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE packages_id_seq OWNED BY packages.id;


--

CREATE TABLE protocols (
    id integer NOT NULL,
    name character varying(255),
    ports character varying(255),
    tcp boolean,
    udp boolean,
    sys boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE protocols_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE protocols_id_seq OWNED BY protocols.id;


--

CREATE TABLE rules (
    id integer NOT NULL,
    ruleset_id integer,
    protocol_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE rules_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--

ALTER SEQUENCE rules_id_seq OWNED BY rules.id;


--

CREATE TABLE rulesets (
    id integer NOT NULL,
    from_id integer,
    to_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--

CREATE SEQUENCE rulesets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE rulesets_id_seq OWNED BY rulesets.id;



CREATE TABLE schema_migrations (
    version character varying(255) NOT NULL
);



CREATE TABLE softwares (
    id integer NOT NULL,
    name character varying(255),
    description character varying(255),
    start_command character varying(255),
    stop_command character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    scope character varying(255),
    check_type_id integer DEFAULT 0,
    check_value character varying(255),
    timeout integer DEFAULT 60,
    groups character varying(255),
    users character varying(255)
);


--

CREATE SEQUENCE softwares_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE softwares_id_seq OWNED BY softwares.id;



CREATE TABLE zones (
    id integer NOT NULL,
    name character varying(255),
    "desc" character varying(255),
    value character varying(255),
    sys boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);



CREATE SEQUENCE zones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE zones_id_seq OWNED BY zones.id;



ALTER TABLE ONLY batches ALTER COLUMN id SET DEFAULT nextval('batches_id_seq'::regclass);



ALTER TABLE ONLY check_types ALTER COLUMN id SET DEFAULT nextval('check_types_id_seq'::regclass);



ALTER TABLE ONLY deploy_batches ALTER COLUMN id SET DEFAULT nextval('deploy_batches_id_seq'::regclass);



ALTER TABLE ONLY deploy_errors ALTER COLUMN id SET DEFAULT nextval('deploy_errors_id_seq'::regclass);



ALTER TABLE ONLY deploy_logs ALTER COLUMN id SET DEFAULT nextval('deploy_logs_id_seq'::regclass);



ALTER TABLE ONLY deploy_states ALTER COLUMN id SET DEFAULT nextval('deploy_states_id_seq'::regclass);



ALTER TABLE ONLY fs ALTER COLUMN id SET DEFAULT nextval('fs_id_seq'::regclass);



ALTER TABLE ONLY logs ALTER COLUMN id SET DEFAULT nextval('logs_id_seq'::regclass);



ALTER TABLE ONLY machine_deploy_states ALTER COLUMN id SET DEFAULT nextval('machine_deploy_states_id_seq'::regclass);



ALTER TABLE ONLY machines ALTER COLUMN id SET DEFAULT nextval('machines_id_seq'::regclass);



ALTER TABLE ONLY machines_packages ALTER COLUMN id SET DEFAULT nextval('machines_packages_id_seq'::regclass);



ALTER TABLE ONLY management_servers ALTER COLUMN id SET DEFAULT nextval('management_servers_id_seq'::regclass);



ALTER TABLE ONLY packages ALTER COLUMN id SET DEFAULT nextval('packages_id_seq'::regclass);



ALTER TABLE ONLY protocols ALTER COLUMN id SET DEFAULT nextval('protocols_id_seq'::regclass);



ALTER TABLE ONLY rules ALTER COLUMN id SET DEFAULT nextval('rules_id_seq'::regclass);



ALTER TABLE ONLY rulesets ALTER COLUMN id SET DEFAULT nextval('rulesets_id_seq'::regclass);



ALTER TABLE ONLY softwares ALTER COLUMN id SET DEFAULT nextval('softwares_id_seq'::regclass);



ALTER TABLE ONLY zones ALTER COLUMN id SET DEFAULT nextval('zones_id_seq'::regclass);



ALTER TABLE ONLY batches
    ADD CONSTRAINT batches_pkey PRIMARY KEY (id);



ALTER TABLE ONLY check_types
    ADD CONSTRAINT check_types_pkey PRIMARY KEY (id);



ALTER TABLE ONLY deploy_batches
    ADD CONSTRAINT deploy_batches_pkey PRIMARY KEY (id);



ALTER TABLE ONLY deploy_errors
    ADD CONSTRAINT deploy_errors_pkey PRIMARY KEY (id);



ALTER TABLE ONLY deploy_logs
    ADD CONSTRAINT deploy_logs_pkey PRIMARY KEY (id);



ALTER TABLE ONLY deploy_states
    ADD CONSTRAINT deploy_states_pkey PRIMARY KEY (id);



ALTER TABLE ONLY fs
    ADD CONSTRAINT fs_pkey PRIMARY KEY (id);



ALTER TABLE ONLY logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);



ALTER TABLE ONLY machine_deploy_states
    ADD CONSTRAINT machine_deploy_states_pkey PRIMARY KEY (id);



ALTER TABLE ONLY machines_packages
    ADD CONSTRAINT machines_packages_pkey PRIMARY KEY (id);



ALTER TABLE ONLY machines
    ADD CONSTRAINT machines_pkey PRIMARY KEY (id);



ALTER TABLE ONLY management_servers
    ADD CONSTRAINT management_servers_pkey PRIMARY KEY (id);



ALTER TABLE ONLY packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (id);



ALTER TABLE ONLY protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);



ALTER TABLE ONLY rules
    ADD CONSTRAINT rules_pkey PRIMARY KEY (id);



ALTER TABLE ONLY rulesets
    ADD CONSTRAINT rulesets_pkey PRIMARY KEY (id);



ALTER TABLE ONLY softwares
    ADD CONSTRAINT softwares_pkey PRIMARY KEY (id);



ALTER TABLE ONLY zones
    ADD CONSTRAINT zones_pkey PRIMARY KEY (id);



CREATE UNIQUE INDEX unique_schema_migrations ON schema_migrations USING btree (version);



REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM root;
GRANT ALL ON SCHEMA public TO root;
GRANT ALL ON SCHEMA public TO PUBLIC;



