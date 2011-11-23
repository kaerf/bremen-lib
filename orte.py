import csv
import sys
import json
from datetime import datetime
from urllib import quote, urlopen
from pprint import pprint

SOURCE = 'Bibliotheken-Bremen.csv'

def load():
    data = []
    fh = open(SOURCE, 'rb')
    reader = csv.DictReader(fh)
    for row in reader:
        pprint(row)
        row_ = {}
        for k, v in row.items():
            try:
                row_[k] = float(v)
            except:
                row_[k] = v
        data.append(row_)
    fh.close()
    return data

def recon():
    fhi = open(SOURCE, 'rb')
    fho = open(SOURCE + '.clean2', 'wb')
    reader = csv.DictReader(fhi)
    writer = None
    for row in reader:
        print row['Name']
        row_ = {}
        for k, v in row.items():
            try:
                row_[k] = float(v)
            except:
                row_[k] = v
        row_ = geocode_row(row_)
        keys = sorted(row_.keys())
        if writer is None:
            writer = csv.writer(fho, row_.keys())
            writer.writerow(keys)
            #writer.writerow(dict(zip(row_.keys(), row.keys())))
        writer.writerow([row_[k] for k in keys])
        #print row_
    fhi.close()
    fho.close()

COLUMN_TIMES = [
    (0, 'Mo_von', 'Mo_bis'),
    (0, 'Mo1_von', 'Mo1_bis'),
    (1, 'Di_von', 'Di_bis'),
    (1, 'Di1_von', 'Di1_bis'),
    (2, 'Mi_vin', 'Mi_bis'),
    (2, 'Mi1_vin', 'Mi1_bis'),
    (3, 'Do_von', 'Do_bis'),
    (3, 'Do1_von', 'Do1_bis'),
    (4, 'Fr_von', 'Fr_bis'),
    (4, 'Fr1_von', 'Fr1_bis'),
    (5, 'Sa_von', 'Sa_bis'),
    (6, 'So_von', 'So_bis')
    ]

def match(row, dt):
    for candidate in COLUMN_TIMES:
        day, from_col, to_col = candidate
        if day != dt.weekday():
            continue
        if row.get(from_col, 24) <= dt.hour and \
                row.get(to_col, 0) >= dt.hour:
            return True
    return False

def search(data, dt, lat, lon):
    results = []
    for row in data:
        if match(row, dt):
            results.append(row)
    return results

def geocode_row(row):
    url = "http://nominatim.openstreetmap.org/search/?format=json&q=%s&countrycodes=de&limit=50"
    q = quote("%s %s, %s" % (row['Strasse'], row['Hausnummer'],
                             row['Stadt']))
    data = urlopen(url % q).read()
    #print url % q
    results = json.loads(data)
    if not len(results):
        print "Keine Adresse!"
        row['lat'] = None
        row['lon'] = None
        return row
    for i, res in enumerate(results):
        print i, ": ", res['display_name'].encode('utf-8')
    match = sys.stdin.readline()
    try:
        match = int(match)
    except:
        match = 0
    res = results[match]
    row['lat'] = res['lat']
    row['lon'] = res['lon']
    return row

if __name__ == '__main__':
    data = load()
    dt = datetime.now()
    res = search(data, dt, None, None)
    print [(r['Name'], r['lat'], r['lon']) for r in res]
    #recon()
