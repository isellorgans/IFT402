IFT 402 Capstone Project 
----- PROTOTYPE -----
Members: John Krause Austen Scarville, Sam Hughel, Tareq Ajhaf
APPLICATION NAME: TBD

-----NOTES-----
Application is developed in three separate layers for the moment. They are:

----------------LAYER 1-----------------

1. DJANGO APPLICATION START UP (JK)
	- Applicaton created
	- MySQL Database connected
	- Manage.py / Settings.py properly configured
	- Django URL's set to be managed by application
 	- View.py established for application page rendering
	- Templates created (placeholder)for reusability, including sample HTML forms
	- Models.py POST interaction with forms complete, form information is pushed to database. 

----------------LAYER 2-----------------

2. API / DJANGO INTERACTION (SH)
	- TEST application created
	- MySQL Database connected, test tables created from query. 
	- Settings.py configured
	- Dota 2 (game) API python wrapper installed and imported (https://pypi.python.org/pypi/dota2api/1.3.2)
	- Application interaction with game API
	- Match details and profile details succesfully taken from API, stored as Python DICT object.
	--- WORK IN PROGRESS ---
	- SQL INSERT of Python dictionary object into existing SQL table (ALMOST THERE)

----------------LAYER 3-----------------

3. HTML FRONT END (TA + AS)
	- HTML HOME PAGE 
	- HTML LEAGUE CREATION
	- HTML JOIN LEAGUE (potentially a modular box in the future)
	- HTML REGISTER VERIFY (potentially a modular box in the future)
------------------------------------------------------------------------------------------
---NOTES CONT.---

The above application parts will be pushed to our project repository under a separate -LAYERS_PROTOTYPE- branch for our records.
Priority #1 immediatley following the prototype due date is to converge all three layers into one MASTER branch and begin proper version control. 

THIS TASK WAS DELAYED because prelimiary tasks needed to be completed. These include: 
1. SHARED / HOSTED DATABASE SET UP, CONFIGURED, AND CONNECTED
2. DJANGO VIEWS AND TEMPLATES CONFIGURED AND READY TO ACCEPT HTML PAGES PROPERLY 
	(otherwise we would have a bunch of broken pages, and we want them working during developement).

**AFTER PRELIM. TASKS ARE COMPLETED, THE CONVERGED MASTER BRANCH WILL BE VERSION 0.4**
			(combination of initial layers 1-3).

