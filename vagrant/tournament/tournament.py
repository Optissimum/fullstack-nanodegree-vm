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
    query = 'TRUNCATE matches CASCADE;'
    cur.execute(query)
    conn.commit()
    cur.close()

def deletePlayers():
    #Remove all the player records from the database.
    conn = connect()
    cur = conn.cursor()
    query = 'TRUNCATE players CASCADE;'
    cur.execute(query)
    conn.commit()
    conn.close()

def countPlayers(tourneyName = None):
    #Return number of players
    conn = connect()
    cur = conn.cursor()
    tourneyName = bleach.clean(tourneyName)
    query = 'SELECT count(name) AS num FROM players'
    cur.execute(query) if tourneyName == None else cur.execute(query + ' ' + str(tourneyName))
    num = cur.fetchone()[0]
    conn.close()
    return num

def registerPlayer(name, birthdate = '1900-01-01', tourneyName = ''):
    conn = connect()
    cur = conn.cursor()
    name = bleach.clean(name)
    birthdate = bleach.clean(birthdate)
    tourneyName = bleach.clean(tourneyName)
    query = "INSERT INTO players (name, birthdate, tourney) VALUES (%s, %s, %s)"
    cur.execute(query, (name, birthdate, tourneyName))
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

def reportMatch(winner, loser, tourneyName = ''):
    #Records the outcome of a single match between two players.
    conn = connect()
    cur = conn.cursor()
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    tourneyName = bleach.clean(tourneyName)
    # Add match
    query = 'INSERT INTO matches (pone, ptwo, tourney, winner) VALUES (%s, %s, %s, %s);'
    cur.execute(query, (winner, loser, tourneyName, winner))
    updatePlayerScores(cur)
    conn.commit()
    conn.close()

def updatePlayerScores(cursor):
    # Update tuple with the matches played totals
    cursor.execute('SELECT players.id, count(matches) as num FROM matches, players \
    WHERE matches.pone = players.id or matches.ptwo = players.id GROUP BY players.id;')
    matchList = [(row[0], row[1]) for row in cursor.fetchall()]
    print 'matchList', matchList
    # Update rounds count for each
    for row in matchList:
        print row
        cursor.execute('UPDATE players SET rounds = %s WHERE id = %s' % (row[1], row[0]))

    # Update wins tuple with the wins per player
    cursor.execute('SELECT players.id, count(matches) as num FROM matches, players \
    WHERE matches.winner = players.id GROUP BY players.id;')
    matchList = [(row[0], row[1]) for row in cursor.fetchall()]
    print 'matchList', matchList
    # Update wins count for winners
    for row in matchList:
        print row
        cursor.execute('UPDATE players SET points = %s WHERE id = %s' % (row[1], row[0]))

def tournamentList():
    #Returns a list of tuples of tournaments and the number of people attending
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tourneyview;')
    tournaments = [(row[0], row[1]) for row in cur.fetchall()]
    conn.close()
    return tournaments

def swissPairings():
    #Returns a list of pairs of players for the next round of a match.
    #Sort desc, group in 2's which allows for an easy "pairing"
    #Return a list of tuples, each of which contains (id1, name1, id2, name2)
    conn = connect()
    cur = conn.cursor()
    playerSet = []
    for index, row in enumerate(cur.fetchall()):
        cur.execute('SELECT * FROM playerpoints ORDER BY points desc LIMIT 2 OFFSET %s') % (index+1)*2
        playerSet.append((row[0], row[1]) for row in cur.fetchall())
    conn.close()
    return playerSet
