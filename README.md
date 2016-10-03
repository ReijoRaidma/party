[![Build Status](https://travis-ci.org/ReijoRaidma/party.svg?branch=master)](https://travis-ci.org/ReijoRaidma/party)

# party
Django REST Framework Testing Project


LIST PARTYS
Returns a array of parties that the current user has access to.

GET http://parties-api.com/api/parties/

Returns json like this:
[
    {
        'is_public': True,
        'url': 'http://127.0.0.1:8000/api/parties/f13d7fae-8f38-468e-832f-5eb2e2fb52ce/',
        'guests': [], 'id': 'f13d7fae-8f38-468e-832f-5eb2e2fb52ce',
        'owner': 'http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/',
        'name': 'Teisipäeva pidu pidu'
    },
]



RETRIEVE A SPECIFIC PARTY

GET http://127.0.0.1:8000/api/parties/f13d7fae-8f38-468e-832f-5eb2e2fb52ce/

Returns json like this:
{
    "id": "f13d7fae-8f38-468e-832f-5eb2e2fb52ce",
    "url": "http://127.0.0.1:8000/api/parties/f13d7fae-8f38-468e-832f-5eb2e2fb52ce/",
    "name": "Teisipäeva pidu pidu",
    "owner": "http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/",
    "is_public": true,
    "guests": []
}



SEARCH PARTIES BY NAME

GET http://127.0.0.1:8000/api/parties/?search=test

Returns json like this:
  [
    {
        "id": "f13d7fae-8f38-468e-832f-5eb2e2fb52ce",
        "url": "http://127.0.0.1:8000/api/parties/f13d7fae-8f38-468e-832f-5eb2e2fb52ce/",
        "name": "Teisipäeva pidu pidu",
        "owner": "http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/",
        "is_public": true,
        "guests": []
    }
]



CREATE PARTY
create account with provided data

POST http://127.0.0.1:8000/api/parties/

example POST request JSON data:
{
'name':'PARTY',
'is_public':'True'
}

Returns json like this:

{
    'is_public': True, 'url': 'http://127.0.0.1:8000/api/parties/f13cb571-f755-4fe9-a856-cde2a40740b2/',
    'guests': [],
    'id': 'f13cb571-f755-4fe9-a856-cde2a40740b2',
    'owner': 'http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/',
    'name': 'lahe'
}



DELETE A SPECIFIC PARTY

DELETE http://127.0.0.1:8000/api/parties/d9f86fa8-e3cf-459f-8347-bbe0864432ab/



LIST GUESTS
Returns a array of Guests

GET http://127.0.0.1:8000/api/guests/

Returns json like this:
[
    {
        "id": "d7aced15-40a4-42ee-b7ca-4f5f9bfc184b",
        "url": "http://127.0.0.1:8000/api/guests/d7aced15-40a4-42ee-b7ca-4f5f9bfc184b/",
        "name": "Külaline 1",
        "birth_date": "2016-09-15",
        "party": "http://127.0.0.1:8000/api/parties/d9f86fa8-e3cf-459f-8347-bbe0864432ab/",
        "owner": "http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/"
    },
]



RETRIEVE A SPECIFIC GUEST

GET http://127.0.0.1:8000/api/guests/d7aced15-40a4-42ee-b7ca-4f5f9bfc184b/

Returns json like this:
{
    "id": "d7aced15-40a4-42ee-b7ca-4f5f9bfc184b",
    "url": "http://127.0.0.1:8000/api/guests/d7aced15-40a4-42ee-b7ca-4f5f9bfc184b/",
    "name": "Külaline 1",
    "birth_date": "2016-09-15",
    "party": "http://127.0.0.1:8000/api/parties/d9f86fa8-e3cf-459f-8347-bbe0864432ab/",
    "owner": "http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/"
}



CREATE GUEST
create account with provided data

POST http://127.0.0.1:8000/api/guests/

example POST request JSON data:
{
    "name": "Test guest",
    "birth_date": "2016-09-15",
    "party": "http://127.0.0.1:8000/api/parties/88a2b80d-95fa-494e-aa0c-65f8a0ce8ef2/"
}

Returns json like this:

{
    "id": "71a1b2a0-efa1-4054-85fd-425148361d40",
    "url": "http://127.0.0.1:8000/api/guests/71a1b2a0-efa1-4054-85fd-425148361d40/",
    "name": "Test guest",
    "birth_date": "2016-09-15",
    "party": "http://127.0.0.1:8000/api/parties/d9f86fa8-e3cf-459f-8347-bbe0864432ab/",
    "owner": "http://127.0.0.1:8000/api/users/afc086d3-9577-4a0b-b075-32cfd8f5e616/"
}



DELETE A SPECIFIC GUEST

DELETE http://127.0.0.1:8000/api/guests/d7aced15-40a4-42ee-b7ca-4f5f9bfc184b/



LIST USERS
Returns a array of users

GET http://127.0.0.1:8000/api/users/

Returns json like this:
[
    {
        "id": "72fee6b6-47cf-486d-aae6-a20aca1c365d",
        "url": "http://127.0.0.1:8000/api/users/72fee6b6-47cf-486d-aae6-a20aca1c365d/",
        "username": "test",
        "first_name": "",
        "last_name": "",
        "email": ""
    },
]



RETRIEVE A SPECIFIC USER

GET http://127.0.0.1:8000/api/users/72fee6b6-47cf-486d-aae6-a20aca1c365d/

Returns json like this:
{
    "id": "72fee6b6-47cf-486d-aae6-a20aca1c365d",
    "url": "http://127.0.0.1:8000/api/users/72fee6b6-47cf-486d-aae6-a20aca1c365d/",
    "username": "test",
    "first_name": "",
    "last_name": "",
    "email": ""
}