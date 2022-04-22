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

# How to call the app locally

Postman is the better option since it doesn't replace the "space" by "%20"

![alt text](https://github.com/rogeriosantosluz/scurri_exercise_2/blob/main/app/tests/postman.png?raw=true)

But you can also test using any browser in these two endpoint:

http://localhost:5000/verify_postcode?postcode=BB10 2BF

![alt text](https://github.com/rogeriosantosluz/scurri_exercise_2/blob/main/app/tests/chrome_1.png?raw=true)

or

http://localhost:5000/postcodes/BB10%202BF

![alt text](https://github.com/rogeriosantosluz/scurri_exercise_2/blob/main/app/tests/chrome_2.png?raw=true)

# Tests

* coverage run -m pytest
* coverage report -m

There is a massive test called test_massive_validation that tests more than 100.000 postcodes 
(csv files from https://www.ordnancesurvey.co.uk/business-and-government/products/code-point-open.html) 
and takes a long time to run. 
Please uncomment lines 137-140 in the file scurri_exercise_2/app/tests/test_exercise_2.py if you wish to run that test.

# Heroku Deploy
* heroku login
* heroku create scurri-exercise-2-app
* git push heroku master / git push heroku HEAD:master
* heroku config:set SECRET_KEY=scurri_892840328239048
* heroku logs --tail