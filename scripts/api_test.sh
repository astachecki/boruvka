#!/bin/bash

# register
curl -H "Content-Type: application/json" -X POST -d '{"username":"artur8","password":"secret"}' http://boruvka.local/api/auth/register

#login
curl -H "Content-Type: application/json" -X POST -d '{"username":"artur8","password":"secret"}' http://boruvka.local/api/auth/login


#unauthorized app access
curl -X POST http://boruvka.local/api/hello  

#use app with authorization
curl -H "Authorization: Token mytoken123" -X POST http://boruvka.local/api/hello  
