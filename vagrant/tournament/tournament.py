#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
from contextlib import contextmanager

@contextmanager
def database_session():
    """Provide a clean way to access our database so it won't fail."""
    session = psycopg2.connect("dbname=tournament") #Connect to database
    cursor = session.cursor()
    try:
        yield cursor
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def deleteMatches():
    '''Remove all the match records from the database.'''
    with database_session() as cursor:
        query = 'TRUNCATE matches CASCADE;'
        cursor.execute(query)

def deletePlayers():
    '''Remove all the player records from the database.'''
    with database_session() as cursor:
        query = 'TRUNCATE players CASCADE;'
        cursor.execute(query)

def countPlayers(tourneyName = None):
    '''Return number of players in a tournament.'''
    with database_session() as cursor:
        tourneyName = bleach.clean(tourneyName)
        query = 'SELECT count(name) AS num FROM players'
        cursor.execute(query) if tourneyName == None else cursor.execute(query + ' ' + str(tourneyName))
        num = cursor.fetchone()[0]
        return num

def registerPlayer(name, birthdate = '1900-01-01', tourneyName = ''):
    '''Registers a player's name, birthday, and which tournament they are in.'''
    with database_session() as cursor:
        name = bleach.clean(name)
        birthdate = bleach.clean(birthdate)
        tourneyName = bleach.clean(tourneyName)
        query = "INSERT INTO players (name, birthdate, tourney) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, birthdate, tourneyName))

def playerStandings(tournament = ''):
    '''Returns a list of the players and their win records, sorted by wins.'''
    with database_session() as cursor:
        tournament = bleach.clean(tournament)
        cursor.execute('SELECT * FROM playerpoints;')
        standings = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
        return standings

def matchStandings():
    '''Returns a list of touples of all of the matches.'''
    with database_session() as cursor:
        cursor.execute('SELECT * FROM matches;')
        matches = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
        return matches

def reportMatch(winner, loser, tourneyName = ''):
    '''Records the outcome of a single match between two players.'''
    with database_session() as cursor:
        winner = bleach.clean(winner)
        loser = bleach.clean(loser)
        tourneyName = bleach.clean(tourneyName)
        # Add match
        query = 'INSERT INTO matches (winner, loser, tourney) VALUES (%s, %s, %s);'
        cursor.execute(query, (winner, loser, tourneyName))

def tournamentList():
    '''Returns a list of tuples of tournaments and the number of people attending'''
    with database_session() as cursor:
        cursor.execute('SELECT * FROM tourneyview;')
        tournaments = [(row[0], row[1]) for row in cur.fetchall()]
        return tournaments

def swissPairings():
    '''Return a list of tuples, each of which contains (id1, name1, id2, name2)'''
    with database_session() as cursor:
        playerList = []
        #Dig through playerStandings, concatenating each pair
        for index, row in enumerate(playerStandings(), start=1):
            if index % 2 != 0:
                playerList.append(row[:2] + playerStandings()[index][:2])
                row[:2] + playerStandings()[index][:2]
        return playerList
