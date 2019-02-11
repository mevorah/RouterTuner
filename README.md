# RouterTuner
The motivation for this project is to provide programmatic access to the Cisco E1000 router and any other routers that offer a similar web configuration experience. As a home user, the web portal offers all of the settings I'd be interested in modifying. With that, I was looking for a simpler solution to changing settings than SSHing into the device. This package offers a python library that authenticates and makes changes to the router via web requests.

**Quality Disclaimer:** This project is admittently hacky. It is the result of fooling around during one snowy Seattle afternoon (what will be known as the winter apolocolypse of 2019). The code here is to help others who want to achieve something similar. Contributions are welcomed and encouraged!

## Why is this tricky?
If you google around, you'll find many suggestions for how to interact with a router using python via web requests: https://stackoverflow.com/questions/47085477/python-script-to-communicate-with-router. You'll also find other solutions for authenticating -
1. Using requests.Session()
2. Using http auth

Unfortunately, the process of authenticating into the E1000 is more involved (ugghhh). The following steps happen during authentication into this particular router:
1. User types in router username and password, and hits login
2. Password is encrypted using a nonce (some id) that is injected into the JS by the router and a local JS encryption function
3. The username and encrypted password is passed in a login request to the router
4. A session_id is returned
5. All subsequent requests (to make api calls or move between pages) must include this session_id as a query param

## What does this offer?

**gateway.py** - 
1. Authenticate (generates an encrypted password and retrieves a session_id)
2. Channel changing functionality
3. **TODO:** Other functionality - other basic configuration settings + advanced settings

**tuner.py** -
1. Loops through each channel (1-11), prints the average download speed of **X** speedtests
2. **TODO:** Loop through other settings and tune parameters to achieve the highest download speed

## Wishlist
1. Cron to run script nightly to continuously tune wifi settings
