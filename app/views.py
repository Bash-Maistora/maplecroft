from django.shortcuts import render, get_object_or_404
from .models import Country
import oauth2
import json


class Tweet:

    def __init__(self, text):
        self.text = text


CONSUMER_KEY = 'Uv9QdHwZgw8EgRca8w7eiZfkY'

CONSUMER_SECRET = 'NNIg9wdOY0mRvMgj9F0fI0Xkcy32ug0L8JZOO6vgCNwYawrwmc'

API_KEY = 'AIzaSyBHOL7KfllfAwOUc7awt66RM6LSxKhyVA8'


def oauth_req(url, key, secret, http_method='GET', http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, headers=http_headers)
    return resp, content


def index(request):
    if request.method == 'POST':
        number = request.POST.get('tweets')
        r, content = oauth_req('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=maplecroftrisk&count={}'.format(number),
         '2902126301-vgYmKmzitvMk3BsvlDMxxyrsQmCie6YsUOTMVUG', '7Z26k1Rnxkts05dVw1rEXn62voxNlROF2FQznhYv51iI3')

        if r['status'] == '200':
            results = json.loads(content.decode('utf-8', 'ignore'))
            tweets = [Tweet(result['text']) for result in results]
            countries = {c.name for c in Country.objects.all()}
            codes = {c.code.replace('', '.')[1:] for c in Country.objects.all() if c.code}
            mapped = []
            for tweet in tweets:
                words = set(tweet.text.split())
                match = words & countries
                if match:
                    country = Country.objects.get(name=list(match)[0])
                    tweet.country = country.name
                    tweet.longitude = int(country.longitude)
                    tweet.latitude = int(country.latitude)
                    mapped.append(tweet)
                match = words & codes
                if match:
                    country = Country.objects.get(code=list(match)[0].replace('.', ''))
                    tweet.country = country.name
                    tweet.longitude = int(country.longitude)
                    tweet.latitude = int(country.latitude)
                    mapped.append(tweet)

            return render(request, 'home.html', {'tweets': tweets, 'API': API_KEY, 'mapped': mapped})
        else:
            error = 'Failed to access Twitter API! {}'.format(r['status'])
            return render(request, 'home.html', {'error': error})

    return render(request, 'home.html')
