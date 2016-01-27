#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    return psycopg2.connect("dbname=tournament") #Connect to database

def deleteMatches():
    #Remove all the match records from the database.
    conn = connect()
    cur = conn.cursor()
    query = 'DELETE FROM matches;'
    cur.execute(query)
    conn.commit()
    cur.close()

def deletePlayers():
    #Remove all the player records from the database.
    conn = connect()
    cur = conn.cursor()
    query = 'DELETE FROM players;'
    cur.execute(query)
    conn.commit()
    conn.close()

def countPlayers(region = None):
    conn = connect()
    cur = conn.cursor()
    region = bleach.clean(region)
    cur.execute('SELECT count(name) AS num FROM players;')
    num = cur.fetchone()[0]
    conn.close()
    return num

def registerPlayer(name, birthdate = None, region = '', teamNumber = 0):
    conn = connect()
    cur = conn.cursor()
    name = bleach.clean(name)
    birthdate = bleach.clean(birthdate)
    region = bleach.clean(region)
    teamNumber = bleach.clean(teamNumber)
    query = "INSERT INTO players (name, birthdate, region, team) VALUES (%s, %s, %s, %s);"
    cur.execute(query, (name, birthdate, region, teamNumber))
    conn.commit()
    conn.close()

def playerStandings():
    #Returns a list of the players and their win records, sorted by wins.
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM playerpoints;')
    standings = [(row[0], row[1], row[2], row[3]) for row in cur.fetchall()]
    conn.close()
    return standings

def reportMatch(winner, loser, middler = None, region = None):
    #Records the outcome of a single match between two players.
    conn = connect()
    cur = conn.cursor()
    query = "INSERT INTO matches (pone, ptwo, pthree, region) VALUES (%s, %s, %s, %s);"
    cur.execute(query, (winner, loser, middler, region))
    conn.commit()
    conn.close()

#def swissPairings():
    #Returns a list of pairs of players for the next round of a match.
    #Sort desc, group in 2's which allows for an easy "pairing"
    #Return a list of tuples, each of which contains (id1, name1, id2, name2)
