from sqlalchemy import create_engine
import cx_Oracle

def create_connection(db):
	connStr = None
	if db.lower() == 'protopop':   #oracle
		connStr = 'uname/pwd@url:port/sid'
		db = cx_Oracle.connect(connStr)
		cursor = db.cursor()

		return cursor

	elif db.lower() == 'wisdm':     #mysql
		connStr = 'mysql://user:pwd@localhost/sid'
		engine =  create_engine(connStr)
		connection = engine.connect()

		return connection

	elif db.lower() == 'wisdmdev':	#oracle
		connStr = 'oracle://user:pwd@url:port/sid'
		engine =  create_engine(connStr)
		connection = engine.connect()

		return connection

#get_survey_routing('Simulation Routing test')
