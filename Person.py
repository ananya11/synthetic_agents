import DbConnections
import numpy
import csv
import DecisionTree

syn_pop = 'data/synPop.csv'
bnd_syn_pop = 'data/synPopBinned.csv'

class Person:
	def __init__(self,user):
		self.PID = user["PID"]
		self.AGEP = user["AGEP"]
		self.SEX = "Male" if user["SEX"]==1 else "Female"
		self.HOME_ZIPCODE = user["HOME_ZIPCODE"]
		self.HINCP = user["HINCP"]
		self.HID = user["HID"]
		self.PERSONS = user["PERSONS"]
		self.BIN = "low" if user["BIN"]==1 else "medium" if user["BIN"]==2 else "high"
	

#	def binUser(self):
#		bins = ['high', 'medium', 'low']
#		u_bin = numpy.random.choice(bins, 1)
#		return u_bin[0]

	
	def __str__(self):
		return "{PID : %s, AGE : %s, SEX : %s, " \
				"HINCP : %s, PERSONS : %s, BIN : %s}" %(
			str(self.PID), str(self.AGEP), 
			self.SEX, str(self.HINCP), str(self.PERSONS), self.BIN) 


def get_person_info_all():
	cursor = DbConnections.create_connection('protopop')
	
	if_tbl_exists = cursor.execute(
				"select 1 from all_tables \
		   		where owner='ANANYA' and \
		   		table_name='PERSON_INFO_ALL'"
		   		)	
	
	u_details = None
	outfile = syn_pop
	with open(outfile, 'wb') as o_file:
		outcsv = csv.writer(o_file,dialect='excel')

		for r in if_tbl_exists:
			if r[0] == 1:
				cursor.execute(
					"select * \
					from PERSON_INFO_ALL"
					)
				header = []
				for cols in cursor.description:
					header.append(cols[0])
				outcsv.writerow(header)
				outcsv.writerows(cursor.fetchall())

	#connection.close()
	return outfile


def binUsers(syn_pop_file):
	bnd_pop_file = bnd_syn_pop
	DecisionTree.classify(syn_pop_file, bnd_pop_file)
	
	csv_to_list = []
	with open(bnd_pop_file, 'r') as f:
		csv_to_list = [{k: int(v) for k, v in row.items()}
			for row in csv.DictReader(f, skipinitialspace=True)]
	
		return csv_to_list



def getResponders():
	people = []
	
	syn_pop_file = get_person_info_all()
	u_details = binUsers(syn_pop_file)

	if u_details:
		for user in u_details:
			person = Person(user)
			people.append(person)
			
		return people

