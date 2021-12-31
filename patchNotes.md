# Patch Notes

"Transparency is the foundation to greatness, and all quotes on the internet are to be believed." - Genghis Khan

## December 25 2021: Christmas woes
One of the most disappointing feeling, is when you recognize your biggest weakness, yet it still creeps up on you and destroys you. My fear of failure often keeps me locked from making decent progress on any project. This is often despite me logically knowing that once I start, I can do it. Before I know it, I am days away from years end and somehow not even a quarter through my project.

previous to this, main difficulty was not knowing the ordinal axis in d3, resulting in numerous unnecessary lines of code to achieve the same result. 
- resolved levitating y axis (wrong padding subtracted)
- removed line-based gridlines, added tick-based gridlines
- installed react-hook-form
- data structure of survey data revised 1 
- dynamic construction of form (INCOMPLETE, suspect wrong interpretation of survey data structure)

## December 26 2021: Cakes
Holiday seasons are often the busiest, even during the pandemic. Being a hermit with most of his daily vitamin D quota fulfilled via supplements, I still exchanged many holiday greetings and gifts. Weather wasn't too bad either, overall a good day.
A lot of trial and error today, trying to figure out the most intuitive and yet most information packed way to have the data
finished POST to backend, coupled with simple frontend validation

- resolved no form generated (wrong interpretation of survey data structure)
- revised data structure 2 (to include necessary data per input)
- revised data structure 3 (revise to a name-based object form instead of input id, making it per question)
- revised data structure 4 (included a required attribute for the input)
- added frontend data validation
- added simple submission lock (useless upon refresh)
- added POST to flask backend
- TODO: refactor/cleanup

## December 27 2021: Yer a lizard, 'arry
Time flies like Harry on a broomstick
The api splitting paves way for fetching only needed data in cases such as user already submitted, therefore does not need survey data
reduces number of lines of code in /poll making it easier to read

- split /poll api into 3: 
 - /poll (for only poll result at time of fetch)
 - /surv (for survey questions)
 - /submitSurv (POST, for user submission)
- added pollId to datapack so user submission can be properly entered
- start db connection to postgres

## December 28 2021: SQL
How to store data of unknown format well into a RDBMS?
Current solution: lump it into a JSON and just dump it in!

- implement dbworks class as postgresql connector
- stored all sensitive information in separate ini file (updated gitignore)
- implemented dbworks methods that dynamically create needed tables and rows (to be tested)
- TODO: gather table/row creating methods in dbworks into one
- TODO: finish dbworks insert user input method
- TODO: use actual data from SQL instead of dummy in app.py

## December 29 2021: SQL yet again
injection attacks and psycopg2...
First problem was py strings being double quoted when directly referenced (solved with tuple)
Second problem was single quoted column/tablenames (solved with AsIs)
Third was trying to think where SQL injections might happen

- gathered all initializing poll methods into one DbWorks.initializePoll()
- tested and fixed all parsing issues by using psycopg2.extensions.AsIs for queries that need no quotes
- patched all locations of possible SQL injection by ways of regex/psycopg2.extensions.quote_ident
- working DbWorks.insertUserInput()
- TODO: finally use actual SQL data in app.py

## December 30 2021: v0.5 MVP
found a bug in vbar that traced back to me not thinking through how d3.scale() works. It defines the max and min of x/y
based on the size of the canvas and the given dataset. Meaning for a barchart, the returned value does not denote height, it denotes
the starting drawing point of the bars.

- finished DbWorks.getPollResMain() to return a well-formed package of data for flask backend
- finished DbWorks.getPollSurvMain() to return a well-formed pckage of data for flask backend
- tweaked DbWorks.insertUserInput()
- linked flask fully to postgres through psycopg2
- added frontend styling
- installed sass