import json
import random
import time
import csv
import operator
import collections
import os
from datetime import datetime


from flask import Flask, Response, render_template


def getDataTime(strDateTime):
	dd=datetime.strptime(strDateTime, '%Y-%m-%d %H:%M');
	return dd;

def numeleZilei(strDateTime):
	day=getDataTime(strDateTime).weekday();
	day_name= ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata','Duminica']
	return day_name[day];

def readCSVtoDict(csvFilename,dbhour):
	today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0);
	with open(csvFilename, newline='') as csvfile:
		dbcsv = list(csv.reader(csvfile, delimiter=';', quotechar='\"'));
		lastModified = datetime.strptime(time.ctime(os.path.getmtime(csvFilename)), "%a %b %d %H:%M:%S %Y").replace(hour=0, minute=0, second=0, microsecond=0);
		for row in dbcsv[1:]:
			for count, item in list(enumerate(row))[1:]:
				#print(count, item)
				dt='{0}-{1}-{2} {3:02d}:00'.format(row[0].split('.')[2],row[0].split('.')[1],row[0].split('.')[0],count-1);
				#print(dt," ", item);
				#check time in the future
				dtDateTime = getDataTime(dt);
				if (dtDateTime<lastModified and dtDateTime<today):
					dbhour[dt]=float(item.replace(",",".").replace("-","-0.01"));
	#return json.dumps( [{'time': ora, 'value': dbhour[ora]} for ora in dbhour]);

def readAllCSV(dirName):
	print("readAllCSV");
	dbhour = {}
	for file in os.listdir(dirName):
		if file.endswith(".csv"):
			fileN=os.path.join(dirName, file);
			print(fileN);
			readCSVtoDict(fileN,dbhour);
	return dbhour;

def generateStats(dbhour):
	dbhourStats = dict((k, v) for k, v in dbhour.items() if float(v) >= 0) ;
	itmax=max(dbhourStats.items(), key=operator.itemgetter(1));
	itmin=min(dbhourStats.items(), key=operator.itemgetter(1));
	oramax=max(dbhourStats.keys());
	oramin=min(dbhourStats.keys());
	suma=sum(dbhourStats.values());
	nrTotal=len(dbhour);
	nrValoriValide=len(dbhourStats);
	consumMediu=float(suma)/nrValoriValide;

	strStats="<p><b>Interval</b> : {0} - {1} </p>\
	<p><b>Total citiri</b> : {2} / Total ore citiri cu date : {3} / Ore lipsa : {4}</p> \
	<p><b>Total consum</b> : {5} kWh</p> \
	<p><b>Consum mediu</b> : {6} <p> \
	</p><b>Cel mai mare consum</b> : {7}, {8} : {9} kWh</p> \
	".format(oramin,oramax,nrTotal,nrValoriValide,nrTotal-nrValoriValide,suma,consumMediu, numeleZilei(itmax[0]),itmax[0],itmax[1]);
	return strStats,consumMediu;


pathToData = "/home/ig17o/curent/data/";
if(not os.path.exists("/home/ig17o/curent/data/") ):
	pathToData ="data/";
dbhour = readAllCSV(pathToData);
strSt,consumMediu=generateStats(dbhour);
print ("Consum mediu", consumMediu);
cachedJson = json.dumps( {'data':[{'time': ora, 'value': dbhour[ora]} for ora in sorted (dbhour.keys())],'stats':strSt,'consumMediu':consumMediu});
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
	def generate_random_data():
		while True:
			yield f"{cachedJson}\n\n";
			time.sleep(10)
	return Response(generate_random_data(), mimetype='/event-stream')

@app.route('/static-data')
def static_data():
	print (cachedJson);
	return Response(cachedJson, mimetype='app/json')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

