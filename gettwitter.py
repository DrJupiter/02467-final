##
from requests_oauthlib import OAuth1Session
import os
import json
import pandas as pd
import numpy as np

# To set your enviornment variables in your terminal run the following line:
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get("CONSUMER_KEY") #does not work
consumer_secret = os.environ.get("CONSUMER_SECRET") #does not work, set manually

##

df = pd.read_csv('2022-03-14_1.csv', sep='\s+')

##
temp = []
list_of_lists = []
for count, id in enumerate(df.values):
    temp.append(str(id[0]))
    if count % 100 == 99:
        temp = ",".join(temp)
        list_of_lists.append(temp)
        temp = []

##



##
# You can adjust ids to include a single Tweets
# Or you can add to up to 100 comma-separated IDs



##
df = pd.DataFrame()
for i in range(len(list_of_lists)):
    params = {"ids": list_of_lists[i], "tweet.fields": "text,author_id,context_annotations,created_at,entities,id,in_reply_to_user_id,lang,public_metrics,referenced_tweets,source"}
    # Tweet fields are adjustable.
    # Options include: #"attachments,author_id,context_annotations,conversation_id,created_at, entities,id,in_reply_to_user_id,lang,promoted_metrics,public_metrics,referenced_tweets,source,text"
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    if i ==0:
        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)


        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.get(
        "https://api.twitter.com/2/tweets", params=params
    )

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

    if len(df) == 0:
        df = pd.DataFrame.from_dict(json_response['data'])
    else:
        new_df = pd.DataFrame.from_dict(json_response['data'])
        new_df.index += (len(df))
        df = pd.concat([df, new_df], axis=0)
##

df.to_csv("test.csv")
