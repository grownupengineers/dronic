/*
    Script to initalize a database

    Schema:

    CredMap:    map credentials to the respective table
    - cred_id (str) - credential name
    - table (str) - table name

    Secret: a secret text
    - cred_id (str) - credential name
    - secret (str) - the secret text

    UserPass:   username and password
    - cred_id (str) - credential name
    - username (str) - the username
    - password (str) - the password
*/

CREATE TABLE CredMap(
    cred_id TEXT NOT NULL UNIQUE PRIMARY KEY,
    table TEXT NOT NULL
);

CREATE TABLE Secret(
    cred_id TEXT NOT NULL UNIQUE REFERENCES CredMap(cred_id),
    secret TEXT NOT NULL
);

CREATE TABLE UserPass(
    cred_id TEXT NOT NULL UNIQUE REFERENCES CredMap(cred_id),
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
