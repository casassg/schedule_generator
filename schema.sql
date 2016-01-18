drop table if exists classe;
drop table if exists grup;
drop table if exists assignatures;
create TABLE assignatures (
    nom varchar(255) not null,
    PRIMARY KEY (nom)
);

create TABLE grup (
    id integer not null,
    assig varchar(255) not null,
    PRIMARY KEY (assig, id),
    FOREIGN KEY (assig) REFERENCES assignatures (nom)
);

create TABLE classe (
    inici time not null,
    fi time not null,
    grup integer not null,
    dia varchar(20) not null,
    assig varchar(255) not null,
    PRIMARY KEY (inici, assig, fi, grup, dia),
    FOREIGN KEY (assig, grup) REFERENCES grup (assig, id)
);

