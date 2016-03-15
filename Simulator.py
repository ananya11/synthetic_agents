import requests
import logging as simlogging
import json
from collections import OrderedDict
import numpy
from Routing import Routing

FORMAT = '%(asctime)-15s %(levelname)s:%(message)s'
simlogging.basicConfig(format=FORMAT, filemode='w', filename= "log.log", level=simlogging.DEBUG)

def get_all_responses(user, sname, dbName, sdata):
        u_resps = []
        u_bin = user.BIN
	
	if 'preamble' in sdata.keys() and sdata['preamble'] == True:
		u_resps.append(None)
   
	rt = Routing(sname, dbName)
	curr_q = rt.getFirstQuestion()
	
	while curr_q is not 'end':
		curr_q = str(curr_q)
		question_text = sdata[curr_q]["question_text"]
		question_type = sdata[curr_q]["question_type"]
    
		if sdata[curr_q]["demographic"]:
		    if sdata[curr_q]["choices"] and type(sdata[curr_q]["choices"]) is list:	#works only for household income
			hincp = user.HINCP
			val = sdata[curr_q]["choices"][hincp-1]

		    else:
			mapped_ora_col = sdata[curr_q]["mapped_ora_col"]
			val = getattr(user, mapped_ora_col.upper())

		    u_resps.append({question_text : val})
		    nextq = rt.getNextQuestion(long(curr_q), val)

		    curr_q = nextq		    
	
		else:
		    if sdata[curr_q]["range"]:
			try:
				key = sdata[curr_q]['range']['$ref']
				mapped_ora_col = sdata[curr_q][key]
				maxval = getattr(user, mapped_ora_col.upper())
			except:
				maxval = sdata[curr_q]['range']
				
			val = numpy.random.choice(range(maxval),1) #excluding you
			u_resps.append({question_text : val})
			nextq = rt.getNextQuestion(long(curr_q), val)
			curr_q = nextq


		    else:
			if "Radio" in question_type:
				pick = 1
				ch_probs = sdata[curr_q]["choices"][u_bin]
				choices = [ch for ch in ch_probs]
				probs = [ch_probs[ch] for ch in ch_probs]
				choose = numpy.random.choice(choices, pick, probs)

				u_resps.append({question_text : choose[0]})

				nextq = rt.getNextQuestion(long(curr_q), choose[0])
				curr_q = nextq


			elif "Check" in question_type:
				chosen = []
				temp = []

				choices = sdata[curr_q]["choices"][u_bin]
				#for key,value in choices.items():
				#	print key
				#	print value
				#	res = numpy.random.choice(['yes','no'],1,[value, 1-value])
				#	print res[0]
				#	#if res[0]=='yes':
				#	#	print value
				

				probs = numpy.random.uniform(size=(1, len(choices)))
				samples = probs < choices.values()
				
				print probs
				print choices.values()

				if numpy.any(samples):  #returns True is any of the elements is True
				    resp = numpy.choose(numpy.where(samples[0, :]), choices.keys())
				    for r in range(resp.size):
					chosen.append((question_text, resp.flat[r]))
					temp.append(resp.flat[r])
				else:
				    chosen.append((question_text, sdata[curr_q]["choices"]["default"]))
				    temp.append(sdata[curr_q]["choices"]["default"])
				
				
				u_resps.append(chosen)
				nextq = rt.getNextQuestion(long(curr_q), temp)
				curr_q = nextq

			elif "LineTextField" in question_type:
				u_resps = 'single line or multi-line answers not supported'
				curr_q = nextq


	return u_resps


def log(msg_type, msg):
    if msg_type == "error":
        simlogging.error(msg)

    elif msg_type == "debug":
        simlogging.warning(msg)

    else:
        simlogging.info(msg)


def httpLog(r):
	s_code = r.status_code
	
        if  200<=s_code<300:
		log("info", r.url+ "	"+str(s_code))
	elif 300 <= s_code < 400:
		log("debug", r.url+ "   "+str(s_code))
		log("debug", r.raise_for_status())
	elif s_code >= 400:
		log("error", r.url+ "   "+str(s_code))
		log("error", r.raise_for_status())

def readConfig(config_file):
	with open(config_file) as config:
		conf = json.load(config, object_pairs_hook=OrderedDict)
		metadata, sdata = conf.values()[0], conf.values()[1]

		return metadata, sdata


def take_survey(responder, config_file):
	metadata, sdata = readConfig(config_file)
	sname = metadata["sname"]
	url = metadata["surl"]
	dbName = metadata["sdb"]

	s_ans = get_all_responses(responder, sname, dbName, sdata)
	print s_ans
        
	with requests.Session() as s:
		log("info", responder)

		r = s.get(url)
		httpLog(r)
               
		for ans in s_ans:
                   data = ans
                   s.post(url, data=data)
                   httpLog(r)

                

				
		

		






