## This project is currently no longer live and maintained
# randoPoll.com
src code: https://github.com/MatchaCrisp/RandoPoll
youtube presentation: https://youtu.be/FFVZm5VO7fM
## Introduction
This is a web application with the goal of publishing a survey every week, alongside the survey results at that particular moment in time.
By: Junyan Ye
From: Toronto, Ontario, Canada

### please visit github link to see full src, and live link to see the app on heroku

## scripts/components

### python
 - flask backend serves as the API in RESTful dev
 - DbWorks class deals with connecting and working with RDBMS

#### app.py
 - /poll serves via GET a JSON file containing current survey results using DbWorks.getPollResMain(curr_date,res_column)
 - /surv serves via GET a JSON file containing current survey questions using DbWorks.getPollSurvMain(curr_date)
 - /submitSurv receives via POST userInput in a JSON file containing PK:poll_id and answers, then uses that to update the database via DbWorks.insertUserInput(userData)

#### DbWorks.py
 Python Class connects to PostgreSQL via psycopg2, all input verified to have no special characters before becoming part of SQL query.
 constructor saves db connector and cursor as instance variables
 destructor closes connection and cursor before destruction
 - dbInfo() method prints database version
 - schema() method prints list of tables in database
 - initializePoll() when given the properly formed JSON updates the database to current week's survey
 - insertUserInput() fetches the survey result table via PK:poll_id and inserts user input if valid
 - initPoll() is only ever used at database initialization to create polls table, which details each weekly poll and their related tables
 - getCur() passes to the asker the cursor to do own query (may delete later)
 - getPollResMain() validates date and column, then fetches the poll result of that week's poll, aggregating the column specified, forming it into correct JSON format
 - getPollSurvMain() validates date, then fetches the poll questions of that week, forming it into correct JSON format

#### config.py
Originally for interpreting a database.ini file into credential needed to log into local postgres server.
Depreciated as heroku postgresql does not work that way

### javascript
 - react does the fetching and dynamic updating
 - d3.js does the interpretation from json-> graph

#### index.js
 - renders react component <App /> to <div id="root" />

#### App.js
 - component contains <header /> and <footer /> and two React components: <Graph /> and <Survey />
 - fetches from RESTful API relevant data such as current poll result/poll questions

#### Graph.js
 - depending on the graph type desired, preprocess and pass the JSON poll results onto another component to render into d3 graph (currently only support vertical bar graphs).
 - displays loading gif when no data is retrieved yet

#### Graphers.js
 - contains the components capable of converting JSON to D3 graph (currently only vertical bar).
 - VBar component appends svg dependent on current viewport size (by using useDim.js hook), from JSON, add graph title, add graph bar with dynamic color scheme and height, add ordinal x-axis scale and numeric y-axis scale, and add tooltip on hover.

#### Survey.js
 - renders an HTML form based on received JSON poll questions
 - posts to RESTful API user input (goes through rudimentary validation first)
 - depending on submission state, either render a loading icon, a thank you message, or the HTML form

#### useDim.js
 - React hook that takes current viewport size and returns a certain x,y for the Grapher to use as svg size

### HTML

#### index.html
 - adds custom flavicon and tab title
 - adds font-awesome library to enable github icon being used as link

### CSS

#### index.scss
 - change box-sizing to be not annoying

#### App.scss
 - contain children in flexbox, flex-direction:column
 - style header/footer

#### Graph.scss
 - set dynamic graph container size (with min/max)

#### Vbargraph.scss
 - sets bargraph hover effect
 - set graph border
 - set horizontal grid lines (are actually just elongated y-axis ticks)

#### Survey.scss
 - set dynamic from container size (with min/max)
 - style form elements to not be ugly
 - custom styling of submit button (tried to imitate Material.UI)
 - custom radio button styling (from CSS-tricks)

patchnotes.md and design.md contains further details

## Technologies
### frontend
- React
- HTML5
- SASS
- D3.js

### backend
- flask
- PostgreSQL

## implemented features
- dynamic graph construction
- real time survey results
- dynamic survey construction
- non-refreshing result POST
- frontend user input validation
- SQL connecting
- proper SQL database schema
- generate GET data from SQL table
- backend user input validation
- insert valid input into database
- submission progress visual cue
- frontend styling
- hosting on heroku

## upcoming (in order)

- admin portal for making surveys
- prevent repeat submission via cookie/social media
- historical polls
- poll sort
- email list sign up
- poll suggestion
- site suggestion
- saving demographic data 
- construct other relevant graphs from demographic data

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

## December 31 2021: v1.0 production

- lifted submissionStatus state up grom survey.js to enable auto refresh poll result
- added auto refresh poll result useeffect for successful form submission
- added custom flavicon

## Jan 6 2022: v1.1.1 poll2

- new coffee vs tea poll
- attempt fix at graph not rendering first time
- code clean up/remove possible security threat of getcur

## Jan 14 2022: v1.1.2 poll2
- skyrim player age poll

## Jan 25 2022 v1.1.3 poll3
- pineapple pizza topping poll
- graceful handling of missing poll
- attempt fix at graph not rendering first time

## May 24 2022 v 1.2.0 revisit & offline
- taken offline
- merge readme&patchnotes
- remove unecessary dependencies
- add comments to react code
- add compatibility tag to index html
- update description