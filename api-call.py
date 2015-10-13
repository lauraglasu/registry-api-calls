#!/usr/bin/python
import sys
import os

# Get the script arguments
user=str(sys.argv[1])
password=str(sys.argv[2])
http_request=str(sys.argv[3])

# Get the parameters required for the token
http_response=os.popen( "curl -sIL "+http_request ).read()
for line in http_response.splitlines(True):
    if line.startswith("Www"):
        params=line

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

realm=find_between( params, 'realm="', '"' )
service=find_between( params, 'service="', '"' )
scope=find_between( params, 'scope="', '"' )

# Get the token
token=os.popen( "curl -s -u " + user + ":" + password + ' -d "service=' + service + '" -d "scope=' + scope + '" -d "account=' + user + '" '+ realm ).read()
token_value=find_between( token, '{"token":"', '"}' )

#Do the request as an authenticated user
print ( os.popen( 'curl -sH "Authorization: Bearer ' + token_value + '" ' + http_request ).read() )
