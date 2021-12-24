# dailypoll.com

## goal
Establish a full-functioning web app capable of asking user for a poll via form, and also display result/current progress of poll after successful submission

## technologies
### Frontend
react.js for dynamic webpage (flask-react integration?)
d3.js for data visualization
html5
sass

### Backend
Flask framework
PostgreSQL RDBMS (python postgres integration?)

## core features
### Frontend
Sleek/responsive one page site
html form capable of submitting and prelim sanitizing user input via POST
svg displaying current polling result 

### Backend
complete sanitization and validation of user input from POST
handle valid submission by updating database
handle invalid submission gracefully
return current poll result via GET

## additional features
### Frontend
visual cue for submission in progress
dynamic update svg/form submission
additional form data (age group, gender), and relevant additional graphs
guest/login feature (login via common socia media platforms)
saving repeat data (age group, gender) via cookie/login id
prevent repeat submission via cookie/login id
email list sign up
poll suggestion
site suggestion
poll history
poll sorting (tags)
auto new poll page everyday



