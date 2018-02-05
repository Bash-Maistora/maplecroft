#Setup

1. Create virtual env with Python 3
2. install dependencies from requirements file
3. Run the server with python manage.py runserver


I tried to keep the implementation simple and straightforward. Getting input from user the view creates oauth request and retrieves tweets from twitter api. Then parses the response and uses simple set matching find countries mentioned in the tweets. Then the tweets are rendered in the template and the map is generated with Google Maps Api.