-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE table players(id serial primary key, name text, birthdate date, region text, team serial, points serial);

CREATE table matches(id serial primary key, playerone text, playertwo text, playerthree text);

CREATE view playerpoints AS SELECT name, points FROM players ORDER BY points desc;

CREATE view regionsview AS SELECT region, count(region) as num FROM players GROUP BY region ORDER BY num desc;
