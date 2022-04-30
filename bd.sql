create database sepomex;
use sepomex;

CREATE TABLE estados
(
	c_estado integer not null primary key,
	estado varchar(100) not null
);

CREATE TABLE municipios
(
    c_municipio integer not null primary key,
	municipio varchar(200) not null,
    c_cve_ciudad integer not null,
	c_estado integer not null
);

CREATE TABLE colonias(
	id_asenta_cpcons integer not null primary key,
	colonia varchar(200) not null,
    tipo_asentamiento varchar(200) not null,
    codigop integer not null,
    c_tipo_asenta integer not null,
    d_zona varchar(100) not null,
    c_municipio integer not null
);

alter table municipios add foreign key (c_estado) references estados(c_estado);
alter table colonias add foreign key (c_municipio) references municipios(c_municipio);