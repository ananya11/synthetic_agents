import DbConnections
from sqlalchemy.sql import text

class Routing:
	def __init__(self, surveyName, dbName):
		self.surveyName = surveyName
		self.dbToConnect = dbName
		self.rdict = {}
		self.firstq = None
		self._buildTree()


	def _buildTree(self):
		routing = self._getRouting()
		
		for r in routing:
			self._append2dict(r[0], r[1], r[2])


	def _append2dict(self, curr_q, curr_ch, next_q):
		key = (curr_q, curr_ch)
		value = next_q
		
		self.rdict.update({key :value})
		
		
	def _getRouting(self):
		connection = DbConnections.create_connection(self.dbToConnect)
		survey = connection.execute(
				"select id \
				from dynamic_forms_formmodel \
				where name= '%s'" 
				%self.surveyName
				)
		q_ids = []

		#get all questions for the survey
		for s in survey:
			survey_id = s[0]
			ques_ids = connection.execute(
					"select id, position \
					from dynamic_forms_formfieldmodel \
					where parent_form_id=%s" 
					%survey_id
					)
			
			# list of all questions for the survey
			for qid in ques_ids:
				if qid[1]==1:
					self.firstq = qid[0]
				q_ids.append(qid[0])
			
			# oracle
			# get routing info
			routing = connection.execute(
				"select question_id, choice_text, next_question_id \
				from dynamic_forms_routing \
				where question_id in %s" %str(tuple(q_ids))
				)	


			# mysql
			# run this only if above line throws error in mysql
			#query = text(
			#	"select question_id, choice_text, next_question_id \
			#	from dynamic_forms_routing \
			#	where question_id in :q_ids"
			#	)	
			#routing = connection.execute(query, q_ids=tuple(q_ids)).fetchall()
			
		connection.close()
		return routing


	def getFirstQuestion(self):
		return self.firstq

	def getNextQuestion(self, curr_q, u_resp):
		try:
			return self.rdict[(curr_q, u_resp)]
		
		except:

			 #if user resp not present, check for '(any)'
			try:		
				return self.rdict[(curr_q, "(any)")]
			
			#if '(any)' not present, end survey
			except:
				return 'end'


#r = Routing("Simulation Routing test")
#print r.rdict
#print r.getFirstQuestion()
#print r.getNextQuestion(320, 'yes')
#print r.getNextQuestion(322, 'yes')
#print r.getNextQuestion(326,'no')
