#!/usr/bin/env python3
import sys, json, config, argparse
from requests_oauthlib import OAuth1Session

def auth():
    CK  = config.CONSUMER_KEY
    CS  = config.CONSUMER_SECRET
    AT  = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET
    return OAuth1Session(CK, CS, AT, ATS)

def find_followers(api, user):
    url    = "https://api.twitter.com/1.1/followers/list.json"
    count  = 200
    cursor = -1
    followers_dict = {}
    followers_dict[user] = []
    while True:
        params = {
            'screen_name' : user,
            'count'       : count,
            'cursor'      : cursor,
            'skip_status' : 'true'
            }
        req = api.get(url, params = params)
        if req.status_code == 200:
            res = json.loads(req.text)
            for follower in res['users']:
                followers_dict[user].append(follower['screen_name'])
        else:
            print("Error: %d" % req.status_code)
            sys.exit()
        
        cursor = res['next_cursor']
        if cursor == 0:
            return followers_dict

def find_friends(api, user):
    url    = "https://api.twitter.com/1.1/friends/list.json"
    count  = 200
    cursor = -1
    friends_dict = {}
    friends_dict[user] = []
    while True:
        params = {
            'screen_name' : user,
            'count'       : count,
            'cursor'      : cursor,
            'skip_status' : 'true'
            }
        req = api.get(url, params = params)
        if req.status_code == 200:
            res = json.loads(req.text)
            for friend in res['users']:
                friends_dict[user].append(friend['screen_name'])
        else:
            print("Error: %d" % req.status_code)
        
        cursor = res['next_cursor']
        if cursor == 0:
            return friends_dict

def merge_ff(followers_list, friends_list):
    merge_list = [user]
    merge_list = merge_list + followers_list
    for friend in friends_list:
        if friend in followers_list:
            continue
        else:
            merge_list.append(friend)
    return merge_list

def create_friendship(followers_dict, friends_dict, user):
    with open("friendships.net", mode='w') as f:
        # Add Vertice record.
        merge_list = merge_ff(followers_dict[user], friends_dict[user])
        f.write('*Vertices {}\n1 "{}"\n'.format(len(merge_list), user))
        vertice = 2

        for follower in followers_dict[user]:
            f.write('{} "{}"\n'.format(vertice, follower))
            vertice += 1

        for friend in friends_dict[user]:
            # Add only those who do not duplicate.
            if friend in followers_dict[user]:
                continue
            else:
                f.write('{} "{}"\n'.format(vertice, friend))
                vertice += 1
        
        # Add Arcs record.
        f.write("*Arcs\n")
        for follower in followers_dict[user]:
            arc = merge_list.index(follower) + 1
            f.write('{} 1\n'.format(arc))
        for friend in friends_dict[user]:
            arc = merge_list.index(friend) + 1
            f.write('1 {}\n'.format(arc))
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

    followers_dict.update(find_followers(api, user))
    friends_dict.update(find_friends(api, user))
    create_friendship(followers_dict, friends_dict, user)
