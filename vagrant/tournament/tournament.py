#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect(close = False):
    conn = psycopg2.connect("dbname=tournament") #Connect to database
    #Close that thang if they request it, otherwise open another one up
    #psycopg2.close() if close
    return conn

def deleteMatches():
    """Remove all the match records from the database."""
    cur = connect().cursor()
    query = 'DELETE FROM matches'
    cur.execute(query)

def deletePlayers():
    """Remove all the player records from the database."""
    cur = connect().cursor()
    query = 'DELETE FROM players'
    cur.execute(query)

def countPlayers(region = None):
    cur = connect().cursor()
    region = bleach.clean(region)
    query = "SELECT count(name) AS num FROM players"
    cur.execute(query)
    return cur.fetchone()[0]

def registerPlayer(name, birthdate = None, region = '', teamNumber = 0):
    cur = connect().cursor()
    query = 'INSERT INTO players (name, birthdate,region,team) VALUES (%s, %s, %s, %s)'
    cur.execute(query, (name, birthdate, region, teamNumber))

def playerStandings():
    #Returns a list of the players and their win records, sorted by wins.
    cur = connect().cursor()
    cur.execute('SELECT * FROM playerpoints')
    standings = ({'id' str(row[0]), 'name': str(row[1]), 'wins': str(row[2]), 'matches': str(row[3])) }
        for row in cur.fetchall())

def reportMatch(winner, loser):
    #Records the outcome of a single match between two players.

def swissPairings():
    #Returns a list of pairs of players for the next round of a match.
    #Sort desc, group in 2's which allows for an easy "pairing"
    #Return a list of tuples, each of which contains (id1, name1, id2, name2)
