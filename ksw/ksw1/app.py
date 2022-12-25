from flask import Flask,redirect
app = Flask(__name__)
import requests

@app.route('/ksw1/<value>/')
def ksw1(value):
	if int(value) > 369:
		return 'The Game Finish'
	s=value
	count=0
	for x in s:
		if x=='3' or x=='6' or x=='9':
			count+=1
	if count ==0:
		print("[ksw1] "+value)
		k=int(value)+1
		k=str(k)
		f=open('log.txt',"a",encoding='utf-8')
		f.write('[ksw1] '+value+'\n')
		f.close()
		response=requests.get('http://ksw2_con:5001/ksw2/'+k+'/')
	
		return "[ksw1] "+value+'<br>'+response.text
	else:
		print("[ksw1] "+"JJACK"*count)
		k=int(value)+1
		k=str(k)
		f=open('log.txt',"a",encoding='utf-8')
		f.write("[ksw1] "+"JJACK "*count)
		f.close()
		response=requests.get('http://ksw2_con:5001/ksw2/'+k+'/')
		return "[ksw1] "+"JJACK "*count+'<br>'+response.text
				
		
		
if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 5000, debug = True)
