-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE table players(
  id serial primary key,
  name text,
  birthdate date,
  tourney text,
  rounds integer default 0,
  points integer default 0);

CREATE table matches(
  id serial primary key,
  ptwo serial references players(id),
  pone serial references players(id),
  tourney text,
  winner integer);

CREATE view playerpoints
  AS SELECT id, name, points, rounds
  FROM players
  ORDER BY points desc;

CREATE view tourneyview AS SELECT tourney, count(tourney) as num FROM players GROUP BY tourney ORDER BY num desc;
