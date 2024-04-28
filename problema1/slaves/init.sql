CREATE TABLE IF NOT EXISTS docType (
    type_id INT NOT NULL,
    type_name varchar(250) NOT NULL,
    PRIMARY KEY (type_id)
);

CREATE TABLE IF NOT EXISTS db1 (
    doc_id INT NOT NULL,
    title varchar(250) NOT NULL,
    type_id INT NOT NULL REFERENCES docType (type_id),
    PRIMARY KEY (doc_id)
);

CREATE TABLE IF NOT EXISTS db2 (
    doc_id INT NOT NULL,
    title varchar(250) NOT NULL,
    type_id INT NOT NULL REFERENCES docType (type_id),
    PRIMARY KEY (doc_id)
);

CREATE TABLE IF NOT EXISTS db3 (
    doc_id INT NOT NULL,
    title varchar(250) NOT NULL,
    type_id INT NOT NULL REFERENCES docType (type_id),
    PRIMARY KEY (doc_id)
);

CREATE TABLE IF NOT EXISTS db4 (
    doc_id INT NOT NULL,
    title varchar(250) NOT NULL,
    type_id INT NOT NULL REFERENCES docType (type_id),
    PRIMARY KEY (doc_id)
);

INSERT INTO docType (type_id, type_name) VALUES
(1, 'tesis'),
(2, 'libro'),
(3, 'video'),
(4, 'presentacion')
ON CONFLICT (type_id) DO NOTHING;

DO $$
BEGIN
    FOR i IN 1..10 LOOP
        INSERT INTO db1 (doc_id, title, type_id) VALUES (i, 'tesis ' || i, 1) ON CONFLICT (doc_id) DO NOTHING;
        INSERT INTO db2 (doc_id, title, type_id) VALUES (i, 'libro ' || i, 2) ON CONFLICT (doc_id) DO NOTHING;
        INSERT INTO db3 (doc_id, title, type_id) VALUES (i, 'video ' || i, 3) ON CONFLICT (doc_id) DO NOTHING;
        INSERT INTO db4 (doc_id, title, type_id) VALUES (i, 'presentacion ' || i, 4) ON CONFLICT (doc_id) DO NOTHING;
    END LOOP;
END $$;
