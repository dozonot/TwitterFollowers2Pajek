# TwitterFriendship2Pajek

Get followers and friends, and generate friendships.net file.

![sample_image](https://user-images.githubusercontent.com/31640715/50738602-19551700-1219-11e9-90c9-f21097cec315.png)

## Prerequiests

```
pip install requests_oauthlib
```

or

```
pip3 install requests_oauthlib
```

## Usage

```
$ ./getFriendship.py --help
usage: getFollowers.py [-h] -u USER

Get followers and friends, and generate friendships.net file.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  <Required> Twitter user name(screen_name) to acquire.
                        (example : @dozonot => "dozonot")
```

## Install

```
git clone https://github.com/dozonot/.TwitterFriendship2Pajek.git
cd TwitterFriendship2Pajek
cat << EOF | tee ./config.py
CONSUMER_KEY = "xxx"        # Replace your API keys
CONSUMER_SECRET = "xxx"     # Replace your API keys
ACCESS_TOKEN = "xxx"        # Replace your API keys
ACCESS_TOKEN_SECRET = "xxx" # Replace your API keys
EOF
pip install requests_oauthlib
```

## Tested environment
Python 3.6.7 
[GCC 8.2.0] on linux

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[dozonot](https://github.com/dozonot)
