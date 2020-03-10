*** Settings ***
Documentation  Harbor BATs
Resource  ../../resources/APITest-Util.robot
Resource  ../../resources/Docker-Util.robot
Library  ../../apitests/python/library/Harbor.py  ${SERVER_CONFIG}
Library  OperatingSystem
Library  String
Library  Collections
Library  requests
Library  Process
Default Tags  APIDB

*** Variables ***
${SERVER}  ${ip}
${SERVER_URL}  https://${SERVER}
${SERVER_API_ENDPOINT}  ${SERVER_URL}/api
&{SERVER_CONFIG}  endpoint=${SERVER_API_ENDPOINT}  verify_ssl=False

# TODO the cases commented by "###" can be uncommented after implementing the repository python library based on new API

*** Test Cases ***
Test Case - Push Cnab Bundle
    Harbor API Test  ./tests/apitests/python/test_push_cnab_bundle.py

