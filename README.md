# newsletter-upcoming-elections 

## Steps to create newsletter upcoming elections map

First time only
do: $git clone https://github.com/cicero-data/newsletter-upcoming-elections
this will create a copy of the newsletter-upcoming-elections folder/repo

1. run sql script in pgadmin <br/>
    1a. export results as csv <br/>
	1b. save csv in sql-script-output/ folder <br/>
	1c. inspect csv, if you see chambers where "upcoming election" == NULL
		A. either fix the election in Cicero and rerun the sql script
		B. or remove the row from the csv

2. update variables in gentable_local_sql.py and run it <br/>
	2a. SQL_FILEPATH should be the path the file saved in step 1b <br/>
	2b. OUTPUTFOLDERNAME should be a folder where the script will write output <br/>
    2c. create 2 folders corresponding to OUTPUTFOLDERNAME in the project directory:  <br/>
    2022-3-22-output-tables and 2022-3-22-output-tables-geooutput <br/>
	2c. EMAIL_DATE should be the date the email will be sent <br/>
	2d. TODAY should be today's date <br/>
	2e. run gentable_local_sql.py

3. convert script output to geojson <br/>
	3a. open 2022-3-22-output-tables-geooutput/upcoming.csv <br/>
	3b. remove duplicate elections in same locale (i.e. combine Mayor and City Council to one row) <br/>
	3c. use csv2geojson to convert csv (https://github.com/mapbox/csv2geojson) (e.g. ex. $csv2geojson upcoming-dedupe.csv > 3-2022-upcoming-elections.geojson)

4. upload geojson to github as gist <br/>
	4a. go to your github account, create a new secret gist, give it a useful title like "3-2022-upcoming-elections.geojson" <br/>
	4b. paste the geojson contents into the gist body, dont upload the file <br/>
	4c. in step 5 you will click the "raw" button on the gist and grab the url to paste into the map code in index.html

5. create new copy of index.html <br/>
	5a. the master copy of index.html that gets published lives in the folder newsletter-upcoming-elections/ <br/>
	5b. it is good to keep a copy for each time we publish the map, i.e. map-3-2022/index.html <br/>
	5c. in index.html change the title of the map (look for div class="header-subtitle") <br/>
	5d. also in index.html, change the url pointed to by "data" in the "elections" source to the gist url from step 4 <br/>
	5e. to inspect index.html, right click and select "open with firefox", this will open the file in your browser 

6. update and push <br/>
	6a. Once index.html looks good locally, put the file in newsletter-upcoming-elections/ (the github repo) <br/>
	6b. run $git status to make sure the changes (should be just 2 lines) look alright <br/>
	6b.1. you may need to run $git add <upcoming_elections.csv> to add changes <br/>
	6c. run $git commit -m 'march 2022 map' to commit the update <br/>
	6d. run $git push origin master to push the update to the cicero data repo <br/>
	6e. inspect the github pages url https://cicero-data.github.io/newsletter-upcoming-elections/ <br/>
	6f. we usually post a screenshot of the map in the newsletter, so take a screenshot and save it as a png and jpg