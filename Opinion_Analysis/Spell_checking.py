import subprocess
import json
def azure_Spell_checker(string):
	correct_string = list()	
	logFile = open("logfile.txt","w")
	try:
		#Key1 = fe6f0aea446d4865900109eec99c901e
		#key2 = 4d22853279cd46789031d25ba842acec
		r = subprocess.check_output('curl -v POST "https://api.cognitive.microsoft.com/bing/v5.0/spellcheck?mode=spell" -H "Ocp-Apim-Subscription-Key: fe6f0aea446d4865900109eec99c901e" --form "Text=' + string +'"', shell=True)
		output = json.loads(r)
		try:
			suggestions = output["flaggedTokens"]
			if len(suggestions) != 0:
				for i in range(0,len(suggestions)):
					string = string.replace(suggestions[i]['token'],suggestions[i]['suggestions'][0]['suggestion'])
		except Exception as e:
			print(e)
			logFile.write("Flagged token key does not exists in azure script\n")
	except Exception as e:
		print(e)
		logFile.write("Internet is not working which needed in post Requsts\n")

	return string
