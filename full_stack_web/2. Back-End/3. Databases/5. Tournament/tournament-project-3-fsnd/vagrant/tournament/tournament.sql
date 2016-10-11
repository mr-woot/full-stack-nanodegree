-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop Database and Tables.
-- Cascade drops views associated with each table, if it exists.
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- Create Database and Tables.
-- CREATE DATABASE tournament;
-- \c tournament;
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
	);
CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players (id),
	loser INTEGER REFERENCES players (id)
	);

-- Test Cases

-- ADD TEST PLAYERS
-- INSERT INTO players(name) values('Tushar')
-- INSERT INTO players(name) values('Siddhant')
-- INSERT INTO players(name) values('Aditya')
-- INSERT INTO players(name) values('Tikku')
-- INSERT INTO players(name) values('Utkarsh')
-- INSERT INTO players(name) values('Mukul')
-- INSERT INTO players(name) values('Shekhar')
-- INSERT INTO players(name) values('Gusain')

-- ADD TEST MATCHES
-- INSERT INTO matches(winner, loser) values(1, 2)
-- INSERT INTO matches(winner, loser) values(3, 4)
-- INSERT INTO matches(winner, loser) values(5, 6)
-- INSERT INTO matches(winner, loser) values(7, 8)
-- INSERT INTO matches(winner, loser) values(2, 1)
-- INSERT INTO matches(winner, loser) values(4, 3)
-- INSERT INTO matches(winner, loser) values(6, 5)
-- INSERT INTO matches(winner, loser) values(8, 7)
-- INSERT INTO matches(winner, loser) values(1, 3)
-- INSERT INTO matches(winner, loser) values(5, 8)
-- INSERT INTO matches(winner, loser) values(4, 6)
-- INSERT INTO matches(winner, loser) values(2, 7)

-- Views
CREATE VIEW standings AS (
	SELECT players.id AS id, players.name AS name,
	(SELECT COUNT(*) FROM matches WHERE matches.winner = players.id) AS won,
	(SELECT COUNT(*) FROM matches WHERE players.id IN (winner, loser)) AS played
	FROM players
	GROUP BY players.id
	ORDER BY won DESC
	);