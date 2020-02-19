import json
import random
import time
import csv
import operator
import collections
import os
from datetime import datetime

from flask import Flask, Response, render_template

dbhour = {}

def readCSVtoDict(csvFilename):
	with open(csvFilename, newline='') as csvfile:
		dbcsv = list(csv.reader(csvfile, delimiter=';', quotechar='\"'));
		
		#"2018-12-20 14:00"

		for row in dbcsv[1:]:
			for count, item in list(enumerate(row))[1:]:
				#print(count, item)
				dt='{0}-{1}-{2} {3}:{4}'.format(row[0].split('.')[2],row[0].split('.')[1],row[0].split('.')[0],count-1,"00");
				#print(dt," ", item);
				dbhour[dt]=float(item.replace(",",".").replace("-","0"));
	#return json.dumps( [{'time': ora, 'value': dbhour[ora]} for ora in dbhour]);

def readAllCSV(dirName):
	print("readAllCSV");
	dbhour = {}
	for file in os.listdir(dirName):
		if file.endswith(".csv"):
			fileN=os.path.join(dirName, file);
			print(fileN);
			readCSVtoDict(fileN);

pathToData = "/home/ig17o/curent/data/";
if(not os.path.exists("/home/ig17o/curent/data/") ):
	pathToData ="data/";
readAllCSV(pathToData);
itmax=max(dbhour.items(), key=operator.itemgetter(1));
itmin=min(dbhour.items(), key=operator.itemgetter(1));
oramax=max(dbhour.keys());
oramin=min(dbhour.keys());
print (itmax[0],itmax[1]);
print (itmin[0],itmin[1]);
print("Total consum: ", sum(dbhour.values()));
strStats="<p><b>Interval</b> : {0} - {1}</p><p><b>Total consum</b> : {2}</p><p><b>Cel mai mare consum</b> : {3} - {4}</p>".format(oramin,oramax,sum(dbhour.values()), itmax[0],itmax[1]);
print (strStats);
cachedJson = json.dumps( {'data':[{'time': ora, 'value': dbhour[ora]} for ora in sorted (dbhour.keys())],'stats':strStats});
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
    #print(readCSVtoDict());
    

    app.run(debug=True, threaded=True)

