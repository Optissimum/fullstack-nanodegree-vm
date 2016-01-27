-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS * CASCADE;

CREATE table players(
  id serial primary key,
  name text,
  birthdate date,
  tourney text,
  matches integer default 0,
  points integer default 0);

CREATE table matches(
  id serial primary key,
  pone serial references players(id),
  ptwo serial references players(id),
  tourney text,
  winner text);

CREATE view playerpoints AS SELECT id, name, points, matches FROM players ORDER BY points desc;

CREATE view tourneyview AS SELECT tourney, count(tourney) as num FROM players GROUP BY tourney ORDER BY num desc;

CREATE view twomatch AS SELECT id, pone, ptwo, tourney FROM matches;
