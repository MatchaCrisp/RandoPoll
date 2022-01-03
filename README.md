# randoPoll.com
src code: https://github.com/MatchaCrisp/RandoPoll
live url: https://rando-poll.herokuapp.com/
youtube presentation: https://youtu.be/FFVZm5VO7fM
## Introduction
This is a web application with the goal of publishing a survey every week, alongside the survey results at that particular moment in time.
By: Junyan Ye
From: Toronto, Ontario, Canada

### !important! this submission does not have a good chunk of code originally contained in the folders build and node_modules due to submission being too large
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

## upcoming (in order)
- hosting on heroku
- admin portal for making surveys
- prevent repeat submission via cookie/social media
- historical polls
- poll sort
- email list sign up
- poll suggestion
- site suggestion
- saving demographic data 
- construct other relevant graphs from demographic data
