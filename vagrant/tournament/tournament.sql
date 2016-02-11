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
  tourney text);

CREATE table matches(
  id serial primary key,
  winner serial references players,
  loser serial references players,
  tourney text);

CREATE view tourneyview AS SELECT players.tourney, count(players.tourney) as num FROM players, matches GROUP BY players.tourney ORDER BY num desc;

CREATE view matchcount
  AS SELECT players.id, count(players.id) as matches
  FROM matches, players
  WHERE loser = players.id or winner = players.id
  GROUP BY players.id;

CREATE view playerpoints
  AS SELECT players.id, name, count(winner) as points, count(matchcount.matches) as matches
  FROM players
  LEFT JOIN matchcount ON players.id = matchcount.id
  LEFT JOIN matches ON players.id = winner
  GROUP BY players.id
  ORDER BY points desc;
