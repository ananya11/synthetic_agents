from sqlalchemy import create_engine
import cx_Oracle

def create_connection(db):
	connStr = None
	if db.lower() == 'protopop':   #oracle
		connStr = 'uname/pwd@noldor-db.vbi.vt.edu:1521/ndssl.bioinformatics.vt.edu'
		db = cx_Oracle.connect(connStr)
		cursor = db.cursor()

		return cursor

	elif db.lower() == 'wisdm':     #mysql
		connStr = 'mysql://wisdmtest_user:test4ndssl@localhost/wisdmtest'
		engine =  create_engine(connStr)
		connection = engine.connect()

		return connection

	elif db.lower() == 'wisdmdev':	#oracle
		connStr = 'oracle://wisdm_dev:change1t@noldor-db.vbi.vt.edu:1521/ndssl'
		engine =  create_engine(connStr)
		connection = engine.connect()

		return connection

#get_survey_routing('Simulation Routing test')
