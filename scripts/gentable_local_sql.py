
import requests
from requests.auth import HTTPBasicAuth
import csv
import json
from pprint import pprint
from datetime import datetime, time, date, timezone
from dateutil import tz, parser
import os

os.chdir('C:/Cicero/newsletter-upcoming-elections/newsletter-widget-share')
SQL_FILEPATH = 'sql-script-output/sql_output_2024-01-29.csv'

OUTPULFOLDERNAME = "2024-01-29-output-tables"
EMAIL_DATE = datetime(2024,1,31,tzinfo=timezone.utc)
TODAY = datetime(2024,1,29,tzinfo=timezone.utc)


def makeEDTdatestring_fromfulldt_trello( obj ):

	try: 
		date = parser.parse(obj)
		
		return date
	except:
		return None

def makeEDTdatestring_fromfulldt( obj ):

	try: 
		date = parser.parse(obj)

		return date.replace(hour=5 )
	except:
		return None


def myconverter(o):
	if isinstance(o, datetime):
		return o.__str__()


def load_sql_output():
	
	with open(SQL_FILEPATH, newline='', encoding='utf8') as csvfile:
		data = csv.DictReader(csvfile)

		pd = process_local_sql(data)
	return pd


def process_local_sql(d):
	rd = []
	for r in d:
		
		#r = d[k]

		#print(r)
		try:
			r['upcoming_election'] = makeEDTdatestring_fromfulldt(r['upcoming_election'])
		except:
			pass
		
		rd.append(r)
	return rd


def within_week(x):
	if 'upcoming_election' not in x:
		return False
	else:
		return abs((x['upcoming_election'] - EMAIL_DATE).days) < 7


def within_last_three_month(x):
	if 'upcoming_election' not in x:
		return False
	else:
		return -7 > (x['upcoming_election'] - EMAIL_DATE).days > -90

def within_next_month(x):
	if 'upcoming_election' not in x:
		return False
	else:
		return 0 < (x['upcoming_election'] - EMAIL_DATE).days < 30

def within_next_2_month(x):
	if 'upcoming_election' not in x:
		return False
	else:
		return 0 < (x['upcoming_election'] - EMAIL_DATE).days < 68

def sort_by_election(d):

	today = datetime.today()

	timedelta = (TODAY - EMAIL_DATE).days
	print("timedelta --> ", timedelta)

	#this_week = list(sorted(filter(lambda x: within_week(x), d),key = lambda i: i['next_election'],reverse=False))
	next_month = list(sorted(filter(lambda x: within_next_month(x), d),key = lambda i: i['upcoming_election'],reverse=False))
	next_2_month = list(sorted(filter(lambda x: within_next_2_month(x), d),key = lambda i: i['upcoming_election'],reverse=False))
	#last_three_month = list(sorted(filter(lambda x: within_last_three_month(x), d),key = lambda i: i['next_election'],reverse=False))

	#print( 'len this week ', len(this_week) )
	print( 'len next month ', len(next_month) )
	#print( 'len last 3 month ', len(last_three_month) )

	#for e in last_three_month:
		#print(e)
		#print( ' This election for {} took place {} and the data is in stage {}'.format(e['sk'], e['next_election'], e['nameList']) )

	return next_2_month

def make_output(board_data):
	upcoming = sort_by_election(board_data)

	gf =  OUTPULFOLDERNAME + '-geooutput'
	#for i in [[recent,gf+'/recent.csv'],[upcoming,gf+'/upcoming.csv'],[current,gf+'/current.csv']]:
	for i in [[upcoming,gf+'/upcoming.csv']]:
		write_geo_doc(i[0],i[1])


	#print_table(recent, 'recent-elections-table.html', show_status=True)
	print_table(upcoming, 'upcoming-elections-table.html', show_status=False)
	#print_table(current, 'current-elections-table.html', show_status=False)


def write_geo_doc(l, filename):
	lookup = get_centroid_lookup()
	for e in l:
		sk = e['sk']

		print( sk )
		#print('centroid: ', centroid)


		if e['special'] == 'True':
			e['ue_remarks'] += ' (Special Election)'
		if e['runoff'] == 'True':
			e['ue_remarks'] += ' (Special Election)'


		try:
			r = next(iter(list(filter(lambda x: sk in x['chambers'] ,lookup ))),None)
			e['lat'] = r['lat']
			e['lon'] = r['lon']

			e['next_election_display'] = e['upcoming_election'].strftime('%b %d, %Y')
		except:
			pass	
	cols = l[0].keys()
	maxlen = max([len(i) for i in l])
	print('maxsample ', maxlen )

	maxsample = next(filter(lambda x: len(x) == maxlen ,l ))

	
	print(maxsample)
	rem_list = ['idList','card_id','ne_cicero_link','le_cicero_link','sk','id']
	rms = [maxsample.pop(key) for key in rem_list if key in maxsample]
	print(maxsample)

	with open(filename, 'w', newline='', encoding='utf8') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=maxsample.keys())
		writer.writeheader()

		for data in l:
			#print('here')
			[data.pop(key) for key in rem_list if key in data]
			writer.writerow(data)





def print_table(l, filename, show_status):
	html = """<html><table border="1">
		<tr><th>Date</th><th>Chamber</th><th>Description</th>"""
	if show_status:
		html +=	"<th>Status</th>"
	html += "</tr>"
	for e in l:
		desc = e['ue_remarks']
		html += "<tr><td>{}</td>".format(e['upcoming_election'].strftime('%b %d, %Y'))
		if e['ue_url_1'] != '':
			html += "<td><a href='{}' target='_blank'>{}</a></td>".format(e['ue_url_1'], e['name_formal'])
		else:
			if e['url'] != '':
				html += "<td><a href='{}' target='_blank'>{}</a></td>".format(e['url'], e['name_formal'])
			else:
				html += "<td>{}</td>".format(e['name_formal'])
		html += "<td>{}</td>".format(desc.replace('\\n',' '))
		if show_status:
			html += "<td>{}</td>".format(e['nameList'])	
		html += "</tr>"
	html += "</table></html>"
	
	file = open(OUTPULFOLDERNAME + '/' + filename, "w")
	file.write(html) 


def get_gov_chamber_map():
	cmap = {}
	with open('gov-chamber-map.csv', newline='', encoding='utf8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			cmap[row['name']] = {'chambers':list(set(row['chambers'].replace('{','').replace('}','').split(',')))}
	return cmap 


def get_gov_centroids():
	centroids = {}
	with open('gov-centroids.csv', newline='', encoding='utf8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			centroids[row['name']] = {'lat': float(row['lat']), 'lon':float(row['lon'])}
	return centroids

def get_centroid_lookup():
	gov_chamber_map = get_gov_chamber_map()
	print(len(gov_chamber_map))
	gov_centroids = get_gov_centroids()
	print(len(gov_centroids))
	ds = [gov_centroids, gov_chamber_map]
	d = []
	for k in gov_centroids.keys():
		d.append( [d[k] for d in ds] )
		#d[k] = tuple(d[k] for d in ds)
	dd = []
	for ee in d:	
		dd.append( { **ee[0], **ee[1] } )
	pprint(dd)
	return dd



def main():
	board_data = load_sql_output()


	print( 'len board_data ',  len([i['sk'] for i in board_data]) )
	#print( 'len board_data ',  len(set([i['sk'] for i in board_data])))
	make_output(board_data)


	return

main()
