# newsletter-upcoming-elections 

Steps to create newsletter upcoming elections map

First time only
do: $git clone https://github.com/cicero-data/newsletter-upcoming-elections
this will create a copy of the newsletter-upcoming-elections folder/repo

1. run sql script in pgadmin
	1a. export results as csv
	1b. save csv in sql-script-output/ folder
	1c. inspect csv, if you see chambers where "upcoming election" == NULL
		A. either fix the election in Cicero and rerun the sql script
		B. or remove the row from the csv

2. update variables in gentable_local_sql.py and run it
	2a. SQL_FILEPATH should be the path the file saved in step 1b
	2b. OUTPUTFOLDERNAME should be a folder where the script will write output
		A. create 2 folders corresponding to OUTPUTFOLDERNAME in the project directory
			1. 2022-3-22-output-tables
			2. 2022-3-22-output-tables-geooutput
	2c. EMAIL_DATE should be the date the email will be sent
	2d. TODAY should be today's date
	2e. run gentable_local_sql.py

3. convert script output to geojson
	3a. open 2022-3-22-output-tables-geooutput/upcoming.csv
	3b. remove duplicate elections in same locale (i.e. combine Mayor and City Council to one row)
	3c. use csv2geojson to convert csv (https://github.com/mapbox/csv2geojson)
		A. ex. $csv2geojson upcoming-dedupe.csv > 3-2022-upcoming-elections.geojson

4. upload geojson to github as gist
	4a. go to your github account, create a new secret gist, give is a useful title like "3-2022-upcoming-elections.geojson"
	4b. paste the geojson contents into the gist body, dont upload the file
	4c. in step 5 you will click the "raw" button on the gist and grab the url to paste into the map code in index.html

5. create new copy of index.html
	5a. the master copy of index.html that gets published lives in the folder newsletter-upcoming-elections/
		A. this folder is the github repo
	5b. it is good to keep a copy for each time we publish the map
		A. ie. map-3-2022/index.html
	5c. in index.html change the title of the map (look for <div class="header-subtitle">)
	5d. also in index.html, change the url pointed to by "data" in the "elections" source to the gist url from step 4
	5e. to inspect index.html, right click and select "open with firefox", this will open the file in your browser 

6. update and push
	6a. Once index.html looks good locally, put the file in newsletter-upcoming-elections/ (the github repo)
	6b. run $git status to make sure the changes (should be just 2 lines) look alright
	6b.1. you may needd to run $git add <upcoming_elections.csv> to add changes
	6c. run $git commit -m 'march 2022 map' to commit the update
	6d. run $git push origin master to push the update to the cicero data repo
	6e. inspect the github pages url https://cicero-data.github.io/newsletter-upcoming-elections/
	6f. we usually post a screenshot of the map in the newsletter, so take a screenshot and save it as a png and jpg