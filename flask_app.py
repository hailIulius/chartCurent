import json
import random
import time
import csv
from datetime import datetime

from flask import Flask, Response, render_template

def readJSONCSVData():
	dbhour = {}
	with open('data/ianuarie.csv', newline='') as csvfile:
		dbcsv = list(csv.reader(csvfile, delimiter=';', quotechar='\"'));
		
		#"2018-12-20 14:00"

		for row in dbcsv[1:]:
			for count, item in list(enumerate(row))[1:]:
				#print(count, item)
				dt='{0}-{1}-{2} {3}:{4}'.format(row[0].split('.')[2],row[0].split('.')[1],row[0].split('.')[0],count-1,"00:00");
				#print(dt," ", item);
				dbhour[dt]=item.replace(",",".");
	return json.dumps( [{'time': ora, 'value': dbhour[ora]} for ora in dbhour]);

app = Flask(__name__)
random.seed()  # Initialize the random number generator


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
	def generate_random_data():
		while True:
			ret_val = readJSONCSVData();
			yield f"{ret_val}\n\n";
			time.sleep(10)
	return Response(generate_random_data(), mimetype='/event-stream')

@app.route('/static-data')
def static_data():
	return Response(readJSONCSVData(), mimetype='app/json')

#if __name__ == '__main__':
    #print(readJSONCSVData());
    #app.run(debug=True, threaded=True)
    

