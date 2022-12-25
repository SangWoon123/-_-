from flask import Flask,redirect
import requests
app = Flask(__name__)


	
@app.route('/ksw2/<value>/')
def ksw2(value):
	if int(value) > 369:
		return 'The Game Finish'
	s=value
	count=0
	for x in s:
		if x=='3' or x=='6' or x=='9':
			count+=1
	if count ==0:
		print("[ksw2] "+value)
		k=int(value)+1
		k=str(k)
		f=open('log.txt',"a",encoding='utf-8')
		f.write("[ksw2] "+value)
		f.close()
		response=requests.get('http://ksw3_con:5002/ksw3/'+k+'/')
		return "[ksw2] "+value+'<br>'+response.text
	else:
		print("[ksw2] "+"JJACK"*count)
		k=int(value)+1
		k=str(k)
		f=open('log.txt',"a",encoding='utf-8')
		f.write("[ksw2] "+"JJACK "*count)
		f.close()
		response=requests.get('http://ksw3_con:5002/ksw3/'+k+'/')
		return "[ksw2] "+"JJACK "*count+'<br>'+response.text

if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 5001, debug = True)
