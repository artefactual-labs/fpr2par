# fpr2par
Migrate Archivematica Format Policy Registry ([FPR](https://www.archivematica.org/en/docs/archivematica-1.11/user-manual/preservation/preservation-planning/)) data to a Preservation Actions Registry ([PAR](https://openpreservation.org/events/collaborative-preservation-with-par/)) API

* Clone files and cd to directory:  
  `git clone https://github.com/peterVG/fpr2par && cd fpr2par`  
* Set up virtualenv:  
  `virtualenv venv`  
* Activate virtualenv:  
  `source venv/bin/activate`  
* Install requirements:  
  `pip install -r requirements.txt`   
* Create database:  
  `python create_fpr_db.py`      
* Run (on localhost, port 5000):  
  `export FLASK_APP=run.py`  
  `flask run`  
* Go to `localhost:5000` in browser to confirm that app is running
* Go to `localhost:5000/add_fpr_data` to load FPR data
* Check CLI for import progress
