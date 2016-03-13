import Person
import Simulator
import sys


if __name__ == "__main__":

	if len(sys.argv)<2:
		print "Please specify Config file."
		exit(-1)
		
	config = sys.argv[1]
	people = Person.getResponders()
	print "Survey initiated" 
	for person in people:
		print person
		Simulator.take_survey(person, config)
		print "***************************************"
		
