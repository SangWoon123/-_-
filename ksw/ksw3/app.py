from flask import Flask,redirect
app = Flask(__name__)
import requests

@app.route('/ksw3/<value>/')
def ksw1(value):
	if int(value) > 369:
		return 'The Game Finish'
	s=value
	count=0
	for x in s:
		if x=='3' or x=='6' or x=='9':
			count+=1
	if count ==0:
		print("[ksw3] "+value)
		k=int(value)+1
		k=str(k)
		f=open('log.txt',"a",encoding='utf-8')
		f.write('[ksw3] '+value+'\n')
		f.close()
		response=requests.get('http://ksw4_con:5003/ksw4/'+k+'/')
	
		return "[ksw3] "+value+'<br>'+response.text
	else:
		print("[ksw3] "+"JJACK"*count)
		k=int(value)+1
		k=str(k)
		f=open('log.txt',"a",encoding='utf-8')
		f.write("[ksw3] "+"JJACK "*count)
		f.close()
		response=requests.get('http://ksw4_con:5003/ksw4/'+k+'/')
		return "[ksw3] "+"JJACK "*count+'<br>'+response.text
				
		
		
if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 5002, debug = True)
