import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

with open('bearer-token.txt', 'r') as f:
    bearer_token = f.read().strip()
    print("bearer_token :\n", bearer_token)


def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    # username = "elonmusk"
    username = "BillGates"
    
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by/username/{}".format(username)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_user_id(url):
    # get user id
    response = requests.request("GET", url, auth=bearer_oauth,)

    # check the response
    if response.status_code == 200:
        
        print(json.dumps(response.json(), indent=4, sort_keys=True))
        user_id = response.json()['data']['id']
    else:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    
    return user_id

def get_tweets(user_id):
    
    # get user tweets
    # url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
    url = "https://api.twitter.com/2/users/BillGates/tweets"

    response = requests.request("GET", url, auth=bearer_oauth,)
    
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    
    print(json.dumps(response, indent=4, sort_keys=True))


    return response.json()


def main():
    url = create_url()
    print("create_url :", url)

    # get user id
    user_id = get_user_id(url)
    print("user_id :", user_id)

    # # get user tweets
    json_response = get_tweets(user_id)
    print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()