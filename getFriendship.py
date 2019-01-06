#!/usr/bin/env python3
import sys, json, config, argparse
from retry import retry
from requests_oauthlib import OAuth1Session

def auth():
    CK  = config.CONSUMER_KEY
    CS  = config.CONSUMER_SECRET
    AT  = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET
    return OAuth1Session(CK, CS, AT, ATS)

@retry(tries=3, delay=300)
def request_twitter_api(api, url, params):
    try:
        res = api.get(url, params = params)
        if res.status_code == 200:
            print("Success.")
            return res
        elif res.status_code == 429:
            print("Error: {}, Too many requests".format(res.status_code))
            print("This script sleeps for 300 seconds and then retries.")
            raise TooManyRequests('Too many requests Twitter APIs')
        else:
            print("Error: {}".format(res.status_code))
            sys.exit()
    except TooManyRequests as e:
        print(type(e))

def find_all_followers(api, user):
    url    = "https://api.twitter.com/1.1/followers/list.json"
    cursor = -1
    followers_dict = {}
    followers_dict[user] = []
    while True:
        params = {
            'screen_name' : user,
            'count'       : 200,
            'cursor'      : cursor,
            'skip_status' : 'true'
            }
        print("Get {}'s followers.".format(user))
        res = request_twitter_api(api, url, params)
        text = json.loads(res.text)
        for follower in text['users']:
            followers_dict[user].append(follower['screen_name'])
        
        cursor = text['next_cursor']
        if cursor == 0:
            return followers_dict

def find_all_friends(api, user):
    url    = "https://api.twitter.com/1.1/friends/list.json"
    cursor = -1
    friends_dict = {}
    friends_dict[user] = []
    while True:
        params = {
            'screen_name' : user,
            'count'       : 200,
            'cursor'      : cursor,
            'skip_status' : 'true'
            }
        print("Get {}'s frineds.".format(user))
        res = request_twitter_api(api, url, params)
        text = json.loads(res.text)
        for friend in text['users']:
            friends_dict[user].append(friend['screen_name'])
        
        cursor = text['next_cursor']
        if cursor == 0:
            return friends_dict

def merge_ff(merge_list, followers_dict, friends_dict, user):
    for follower in followers_dict[user]:
        if follower in merge_list:
            continue
        else:
            merge_list.append(follower)
    for friend in friends_dict[user]:
        if friend in merge_list:
            continue
        else:
            merge_list.append(friend)
    return merge_list

def friend_arc(f, merge_list, arc_dict, node):
    n1 = merge_list.index(node) + 1
    for u in arc_dict[node]:
        n2 = merge_list.index(u) + 1
        f.write('{} {}\n'.format(n1, n2))

def follower_arc(f, merge_list, arc_dict, node):
    n1 = merge_list.index(node) + 1
    for u in arc_dict[node]:
        n2 = merge_list.index(u) + 1
        f.write('{} {}\n'.format(n2, n1))

def create_friendship(followers_dict, friends_dict, user):
    with open("friendships.net", mode='w') as f:
        # Add Vertice record.
        merge_list = [user]
        merge_list = merge_ff(merge_list, followers_dict, friends_dict, user)
        for friend in friends_dict[user]:
            merge_list = merge_ff(merge_list, followers_dict, friends_dict, friend)
        for follower in followers_dict[user]:
            merge_list = merge_ff(merge_list, followers_dict, friends_dict, friend)
        f.write('*Vertices {}\n'.format(len(merge_list)))
        vertice = 1

        for u in merge_list:
            f.write('{} "{}"\n'.format(vertice, u))
            vertice += 1

        # Add Arcs record.
        f.write("*Arcs\n")
        friend_arc(f, merge_list, friends_dict, user)
        follower_arc(f, merge_list, followers_dict, user)
        for friend in friends_dict[user]:
            friend_arc(f, merge_list, friends_dict, friend)
        for follower in followers_dict[user]:
            follower_arc(f, merge_list, followers_dict, friend)


            for friend in friends_dict[user]:
                n1 = merge_list.index(user) + 1
                n2 = merge_list.index(friend) + 1
                f.write('{} {}\n'.format(n1, n2))
            for u in followers_dict[user]:
                n1 = merge_list.index(u) + 1
                n2 = merge_list.index(user) + 1
                f.write('{} {}\n'.format(n1, n2))
    print("friendships.net created")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      prog="getFriendship.py",
      description='Get followers and friends, and generate friendships.net file.'
    )
      
    parser.add_argument("-u",
                        "--user",
                        type=str,
                        required=True,
                        help='<Required> Twitter user name(screen_name) to acquire. (example : @dozonot => "dozonot")'
    )

    args  = parser.parse_args()
    user  = args.user
    api   = auth()
    followers_dict = {}
    friends_dict   = {}

    followers_dict.update(find_all_followers(api, user))
    friends_dict.update(find_all_friends(api, user))
    for friend in friends_dict[user]:
        followers_dict.update(find_all_followers(api, friend))
        friends_dict.update(find_all_friends(api, friend))

    create_friendship(followers_dict, friends_dict, user)
