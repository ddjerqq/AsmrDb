CREATE TABLE items
(
    id       INTEGER NOT NULL
        CONSTRAINT items_pk
            PRIMARY KEY ,
    type     varchar(32) DEFAULT 'item' NOT NULL,
    rarity   REAL        DEFAULT 0.5    NOT NULL,
    owner_id INTEGER     DEFAULT NULL
        REFERENCES users
);

CREATE UNIQUE INDEX items_id_uindex
    ON items (id);


CREATE TABLE users
(
    id         INTEGER      NOT NULL
        CONSTRAINT users_pk
            PRIMARY KEY ,
    username   NVARCHAR(50) NOT NULL,
    experience INTEGER DEFAULT 0 NOT NULL,
    wallet     INTEGER DEFAULT 0 NOT NULL,
    bank       INTEGER DEFAULT 0 NOT NULL
);

CREATE UNIQUE INDEX users_snowflake_uindex
    ON users (id);