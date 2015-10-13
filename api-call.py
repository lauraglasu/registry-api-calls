#!/usr/bin/python

import argparse
import urllib.error
import urllib.request
import requests
from requests.auth import HTTPBasicAuth

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_www_authenticate_header(api_url):
    try:
        resp = urllib.request.urlopen(api_url)
        response = (resp.read())
    except urllib.error.HTTPError as error:
        response = (error.info()['Www-Authenticate'])
    return ( response )

def get_token(user, password, service, scope, realm):
    data = {"scope":scope, "service":service, "account":user}
    r = requests.post(realm, auth=HTTPBasicAuth(user, password), data=data)
    token=find_between( (str(r.content)), 'token":"', '"' )
    return ( token )

def get_result(api_url, token):
    r = requests.get(api_url, headers={'Authorization':'Bearer ' + token})
    return (r.content)

def main():

    if ( args.user and args.password and args.api_url ):
        #get the Www-Authenticate header
        params=(get_www_authenticate_header(args.api_url))

        #parse the params required for the token
        if ( params ):
            realm=find_between( params, 'realm="', '"' )
            service=find_between( params, 'service="', '"' )
            scope=find_between( params, 'scope="', '"' )

            # retrieve token
            token = get_token(args.user, args.password, service, scope, realm)

            # Do the API call as an authenticated user
            print ( "Response:" )
            print (get_result(args.api_url, token))
        else:
            print ( "404 Not Found" )


    else:
        # Print usage message in case arguments are missing
        parser.print_help()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--api_url')
    args = parser.parse_args()

    main()
