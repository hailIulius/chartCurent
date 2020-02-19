import json
import time
import csv
import operator
import os
from datetime import datetime


from flask import Flask, Response, render_template


def getDataTime(strDateTime):
    return datetime.strptime(strDateTime, '%Y-%m-%d %H:%M')


def numeleZilei(strDateTime):
    day = getDataTime(strDateTime).weekday()
    day_name = ['Luni', 'Marti', 'Miercuri',
                'Joi', 'Vineri', 'Sambata', 'Duminica']
    return day_name[day]


def readCSVtoDict(csvFilename, dbhour):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    with open(csvFilename, newline='') as csvfile:
        dbcsv = list(csv.reader(csvfile, delimiter=';', quotechar='\"'))
        lastModified = datetime.strptime(time.ctime(os.path.getmtime(csvFilename)), "%a %b %d %H:%M:%S %Y").replace(hour=0, minute=0, second=0, microsecond=0)
        for row in dbcsv[1:]:
            for count, item in list(enumerate(row))[1:]:
                dt = '{0}-{1}-{2} {3:02d}:00'.format(row[0].split('.')[2], row[0].split('.')[
                                                     1], row[0].split('.')[0], count - 1);
                dtDateTime = getDataTime(dt)
                if (dtDateTime < lastModified and dtDateTime < today):
                    dbhour[dt] = float(item.replace(
                        ",", ".").replace("-", "-0.01"))


def readAllCSV(dirName):
    print("readAllCSV")
    dbhour = {}
    for file in os.listdir(dirName):
        if file.endswith(".csv"):
            fileN = os.path.join(dirName, file)
            print(fileN)
            readCSVtoDict(fileN, dbhour)
    return dbhour


def generateStats(dbhour):
    dbhourStats = dict((k, v) for k, v in dbhour.items() if float(v) >= 0)
    itmax = max(dbhourStats.items(), key=operator.itemgetter(1))
    oramax = max(dbhourStats.keys())
    oramin = min(dbhourStats.keys())
    suma = sum(dbhourStats.values())
    nrTotal = len(dbhour)
    nrValoriValide = len(dbhourStats)
    consumMediu = float(suma) / nrValoriValide

    strStats = "<p><b>Interval</b> : {0} - {1} </p>\
	<p><b>Total citiri</b> : {2} / Total ore citiri cu date : {3} / Ore lipsa : {4}</p> \
	<p><b>Total consum</b> : {5} kWh - Cost estimat(1kWh=0.7 LEI) {6:.2f} LEI</p> \
	<p><b>Consum mediu</b> : {7} <p> \
	</p><b>Cel mai mare consum</b> : {8}, {9} : {10} kWh</p> \
	".format(oramin, oramax, nrTotal, nrValoriValide, nrTotal - nrValoriValide, suma, float(suma) * 0.7, consumMediu, numeleZilei(itmax[0]), itmax[0], itmax[1]);
    return strStats, consumMediu


def staticResponseJson():
	pathToData = "/home/ig17o/curent/data/"
	if(not os.path.exists("/home/ig17o/curent/data/")):
		pathToData = "data/"
	dbhour = readAllCSV(pathToData)
	timeList, valueList  = zip(*sorted(zip(dbhour.keys(),dbhour.values())))
	print(len(timeList), " ", len(valueList))
	strSt, consumMediu = generateStats(dbhour)	
	cachedJson = json.dumps({'data': {'time': timeList, 'value': valueList}, 'stats': strSt, 'consumMediu': consumMediu});
	print (cachedJson)
	return cachedJson


cachedJson = staticResponseJson()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            yield f"{cachedJson}\n\n"
            time.sleep(10)
    return Response(generate_random_data(), mimetype='/event-stream')


@app.route('/static-data')
def static_data():
	print ("Request")
	staticResponseJson()
	return Response(cachedJson, mimetype='app/json')


if __name__ == '__main__':
	staticResponseJson()
	app.run(debug=True, threaded=True)
