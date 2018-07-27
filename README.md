[![Build Status](https://travis-ci.org/koechkevin/myDiary.svg?branch=challenge3)](https://travis-ci.org/koechkevin/myDiary)
# Diary

Diary is a set of API endpoints that uses databases to store data implemented in PostgreSQL 

### Set up the environment
This platform APIs is built on flask python framework.
You must have python installed preferably version 3 and have PostgreSQL installed to test the files

Clone the repository and checkout to branch challenge3
```sh
https://github.com/koechkevin/myDiary.git
```
In the path ``` api/v2/models.py ```, make the changes on the line that corresponds to your database connection. The application will create tables for you.

Create a virtual environment on the directory that the cloned repository resides in
I used this command to create a virtual environment

```sh
py -3 -m venv venv
```
Activate the virtual environment
```sh
venv\Scripts\activate
```
```sh
pip install flask
```
Install requirements.txt file

```sh
pip install requirements
```
### Run the application

```sh
python myDiary_dataStructures.py
```
### APIs Endpoints

**`GET "/api/v2"`** *home page*

**`POST /api/v2/users/register`**    *Register user. Takes in a json object with keys as fname,lname,username,password,cpassword,email*

**`POST  /api/v2/users/login`**  *Login. Takes in a json object with keys as username and password*

**`POST /api/v1/entries`** *Post Entry. takes in a json object with key as comment provided you are logged in*

**`GET  /api/v2/entries`** *Get all entries made by user on session*

**`GET /api/v2/entries/<int:entryId>`** *Get an Entry with corresponding entryID*

**`PUT /api/v2/entries/<int:entryId>`** *Update an Entry takes in jsonified dict with comment as key*

**`DELETE /api/v2/entries/<int:entryId>`** *Delete an Entry of corresponding ID*

**`GET /api/v2/users/register`** *Get account details of user on session*

**`GET /api/v2/users/logout`** *Gets user on session out of session*