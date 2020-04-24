# fpr2par
Access Archivematica Format Policy Registry ([FPR](https://www.archivematica.org/en/docs/archivematica-1.11/user-manual/preservation/preservation-planning/)) data via a Preservation Actions Registry ([PAR](https://openpreservation.org/events/collaborative-preservation-with-par/)) API

* Clone files and cd to directory:  
  `git clone https://github.com/peterVG/fpr2par && cd fpr2par`  
* Set up virtualenv:  
  `virtualenv venv`  
* Activate virtualenv:  
  `source venv/bin/activate`  
* Install requirements:  
  `pip install -r requirements.txt`
* Change admin password  
  `fpr2par/__init.py__`      
* Export the Flask application environment variable:  
  `export FLASK_APP=run.py`
* To run the application as a local development server:  
  `flask run`  
* Go to `localhost:5000` in a browser to confirm that the app is running
* Otherwise, to run the application on a publicly accessible server:
  `flask run --host=0.0.0.0`
* Go to `[your IP]:5000` in a browser to confirm that the app is running
* Select "Admin" from navigation menu
* Press "Create fpr2par database" button
* Press "Load data from fixtures" button (takes approx 2 mins)
* See instructions further below if you want to load FPR data from your own instance of Archivematica instead of using the default values from the latest release
* Check CLI for import progress
* Return to UI and select "Browse FPR data" menu to view FPR contents
* Select the "PAR API requests" menu to run sample API requests
* Make PAR API requests with your own client:  
  `[your terminal]> curl -X GET "http://[your base URL]/api/par/tools`

![screencap](fpr2par-demo.png)


# Load FPR data from your own instance of Archivematica
* If you are using a Docker deployment of Archivematica, run the following task:  
  `docker-compose run \`  
    `--rm \`  
    `--entrypoint /src/dashboard/src/manage.py \`  
        `archivematica-dashboard \`  
            `dumpdata --output /var/archivematica/sharedDirectory/tmp/fpr2.json fpr`
* Otherwise, run the following task:  
  `sudo su -s /bin/bash archivematica  
   export PYTHONPATH=/usr/lib/archivematica/archivematicaCommon:/usr/share/archivematica/dashboard  
   set -o allexport  
   source /etc/default/archivematica-dashboard  
   set +o allexport  
   /usr/share/archivematica/dashboard/manage.py dumpdata --output /var/archivematica/sharedDirectory/fpr2.json fpr`
* Relace the "fpr2.json" in the "fpr2par/sourceJSON/"" directory with your newly generated fpr2.json file
* From the "Admin" menu, if you've already created a fpr2par database, press the "Delete fpr2par Database" button
* Press the "Create fpr2par database" button
* Press the "Load data from fixtures" button
