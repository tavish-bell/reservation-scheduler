# Take Home Challenge: Goal Tracking App

## Contents

<!-- vim-markdown-toc GFM -->

- [Setup](#setup)
  - [Install Python dependencies](#install-python-dependencies)
  - [Initialize the database](#initialize-the-database)
  - [Run Flask server](#run-flask-server)
- [File structure](#file-structure)
- [Flask routes](#flask-routes)
  - [`GET` /](#get-)
  - [`POST` /login](#post-login)
    - [Request parameters](#request-parameters)
  - [`POST` /register](#post-register)
    - [Request parameters](#request-parameters-1)
  - [`GET` /goals](#get-goals)
  - [`POST` /goal/new](#post-goalnew)
    - [Request parameters](#request-parameters-2)
  - [`POST` /goal/<goal_id>/edit](#post-goalgoal_idedit)
  - [Request parameters](#request-parameters-3)

<!-- vim-markdown-toc -->

## Setup

Before you begin the setup and installation process below, you'll need to have
the following installed:

- Python 3.0 or above
- PostgreSQL 11

### Install Python dependencies

Create a virtual environment

```
python3 -m venv env

# Alternatively, if you have virtualenv installed
virtualenv env
```

Activate the environment and install dependencies from `requirements.txt`

```
source env/bin/activate
pip3 install -r requirements
```

### Initialize the database

Create a PostgreSQL database called `goals`

```
createdb goals
```

Run this command to create tables and test data

```
python3 model.py --init
```

### Run Flask server

Now you can run the server with

```
python3 server.py
```

The site will be accessible at http://localhost:5000.

## File structure

static/
Contains static assets. Currently only has one CSS file called
`styles.css`
templates/
Jinja2 templates
model.py
Database schema and ORM classes written with SQLAlchemy
server.py
Flask routes

## Flask routes

### `GET` /

Display the homepage

### `POST` /login

Log in a user with their email and password.

#### Request parameters

| Key        | Data Type | Value                    |
| ---------- | --------- | ------------------------ |
| `email`    | string    | The user's email address |
| `password` | string    | The user's password      |

### `POST` /register

Create a new user account

#### Request parameters

| Key        | Data Type | Value                      |
| ---------- | --------- | -------------------------- |
| `email`    | string    | A new user's email address |
| `password` | string    | A new user's password      |

### `GET` /goals

Login required. View the user's dashboard page.

### `POST` /goal/new

Login required. Create a new goal.

#### Request parameters

| Key     | Data Type | Value                             |
| ------- | --------- | --------------------------------- |
| `title` | string    | The title/description of the goal |

### `POST` /goal/<goal_id>/edit

Login required. Edit a goal.

`goal_id` is an integer that's the primary key of the goal you want to edit.

### Request parameters

| Key         | Data Type | Value                                                                                                                            |
| ----------- | --------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `title`     | string    | (optional) The new title for the goal                                                                                            |
| `completed` | string    | (optional) Whether the goal should be marked as complete or incomplete. To mark the goal as complete, set this value to `'true'` |
