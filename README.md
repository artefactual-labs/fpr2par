# fpr2par
Access Archivematica Format Policy Registry ([FPR](https://www.archivematica.org/en/docs/archivematica-1.11/user-manual/preservation/preservation-planning/)) data via a Preservation Actions Registry ([PAR](https://openpreservation.org/events/collaborative-preservation-with-par/)) API

Use the instructions below to install your own copy of fpr2par or try an online copy at [http://parcore.dev.archivematica.org:5000/](http://parcore.dev.archivematica.org:5000/).

![screencap](fpr2par-demo.png)

# Installation instructions
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
* fpr2par is built using the [Python Flask](https://www.fullstackpython.com/flask.html) framework. Export the Flask application environment variable:  
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

# Load FPR data from your own instance of Archivematica
* If you are using a Docker deployment of Archivematica, run the following task:  
  `docker-compose run \`  
    `--rm \`  
    `--entrypoint /src/dashboard/src/manage.py \`  
        `archivematica-dashboard \`  
            `dumpdata --output /var/archivematica/sharedDirectory/tmp/fpr2.json fpr`
* Otherwise, run the following task:  
  `sudo su -s /bin/bash archivematica`  
  `export PYTHONPATH=/usr/lib/archivematica/archivematicaCommon:/usr/share/archivematica/dashboard`  
  `set -o allexport`  
  `source /etc/default/archivematica-dashboard`  
  `set +o allexport`  
  `/usr/share/archivematica/dashboard/manage.py dumpdata --output /var/archivematica/sharedDirectory/fpr2.json fpr`
* Relace the "fpr2.json" in the "fpr2par/sourceJSON/"" directory with your newly generated fpr2.json file
* Note that there are two small issues with the FPR source JSON: [Issue #36](https://github.com/artefactual-labs/fpr2par/issues/36) and [Issue #37](https://github.com/artefactual-labs/fpr2par/issues/37). You will have to make the following fixes to your fpr2.json file: [Fix 1](https://github.com/artefactual-labs/fpr2par/commit/4da49425bb221239fd52c80d1abe483c583d463b) and [Fix 2](https://github.com/artefactual-labs/fpr2par/commit/aa081885776e2373f924f42b6de5326bd55641da)
* From the "Admin" menu, if you've already created a fpr2par database, press the "Delete fpr2par Database" button
* Press the "Create fpr2par database" button
* Press the "Load data from fixtures" button

# Run tests to validate fpr2par against PAR JSON schema
* From the "fpr2par" project root directory, change to the "fpr2par" application directory  
  `cd fpr2par`  
* Run Pytest tests  
  `python -m pytest`
