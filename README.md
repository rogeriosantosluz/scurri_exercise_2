# Scurri Exercise #2
Write a library that supports validating and formatting postcodes for the UK. 

The details of which postcodes are valid and which are the parts they consist of can be found at https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting. 

The API that this library provides is your choice. 


Please make sure you write the library yourself and the API is then to use the library that you created. 
Ensure there are functions in order to format. 
Show all tests written so our engineer can see your thought process. 


* python3 -m pip install --upgrade pip
* python3 -m venv env(PS> virtualenv env)
* source env/bin/activate (PS> .\env\Scripts\activate.bat)
* pip3 install -r requirements.txt
* export FLASK_ENV=development
* export set FLASK_APP=app.webapp (PS> $env:FLASK_APP="webapp")
* python3 -m flask run --host=0.0.0.0 (PS> flask run)

#Tests

* coverage run -m pytest
* coverage report -m

#Heroku Deploy