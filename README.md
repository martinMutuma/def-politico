# Politico-API

[![Build Status](https://travis-ci.org/martinMutuma/def-politico.svg?branch=develop)](https://travis-ci.org/martinMutuma/def-politico)
[![Coverage Status](https://coveralls.io/repos/github/martinMutuma/def-politico/badge.svg)](https://coveralls.io/github/martinMutuma/def-politico)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5dfc74de9408456384dbd2102d07cf08)](https://app.codacy.com/app/martinMutuma/def-politico?utm_source=github.com&utm_medium=referral&utm_content=martinMutuma/def-politico&utm_campaign=Badge_Grade_Settings)

The general elections are around the corner, hence it’s a political season. Get into the mood of the season and help build a platform which both the politicians and citizens can use. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## Hosting
The Politico API is hosted on Heroku. You can access it at [Premier voting](https://premier-voting.herokuapp.com)

## Requirements
- [VS code](https://code.visualstudio.com/)
- [Python 3.x](https://www.python.org/)
- [Postman](https://www.getpostman.com/downloads/)
- [Postgres](https://www.postgresql.org/)

<details><summary>Installation</summary>
<p>

#### installation steps

- clone the git repo
```
$ git clone https://github.com/martinMutuma/def-politico.git
```
- cd into the project directory
```
$ cd def-politico
```
- create the virtual environment and activate it
```
$ python3 -m venv env
$ source env/bin/activate
```
- create the virtual environment and activate it
```
$ python3 -m venv env
$ source env/bin/activate
```
- install dependencies
```
$ pip install -r requirements.txt
```
- Run the app
``` $ flask run ```

</p>
</details>


<p></p>
<p></p>

## Version 2
| **Endpoint**                                  | **Functionality**                               | **Route**                                       |
| ---                                           | ---                                             | ---                                             |
| **POST** /auth/signup/                        | Register user to the database                   | `api/v2/auth/signup/`                           |
| **POST** /auth/login/                         | Login to the system                             | `api/v2/auth/login/`                            |
| **POST** /auth/reset                          | Reset password                                  | `api/v2/auth/reset`                             |
| **POST** /parties                             | Creates a political party                       | `/api/v2/parties/`                              |
| **GET** /parties/`<int:party-id>`             | Gets a specific political party                 | `/api/v2/parties/<int:party_id>`                |
| **GET** /parties                              | Gets all political parties                      | `/api/v2/parties/`                              |
| **PATCH** /parties/`<party-id>`/name          | Edit the name of a specific political party.    | `/api/v2/parties/<int:party-id>/<string:name>` |
| **DELETE** /parties/`<party-id>`              | Delete a political party                        | `/api/v2/parties/<int:party-id>` |
| **POST** /offices                             | Create a political office.                      | `/api/v2/offices/`                              |
| **GET** /offices                              | Fetch all political offices records             | `api/v2/offices/`                               |
| **GET** /offices/`<int:office_id>`            | Fetch a specific political office record        | `api/v2/offices/<int:office_id>`                |
| **PATCH** /offices/`<office_id>`/name         | Edit the name of a specific political Office.   | `/api/v2/offices/<int:office_id>/name`          |
| **POST** /office/`<int:office_id>`/register/  | Register a political candidate                  | `api/v2/office<int:office_id>/register`      |
| **POST** /votes/                              | Cast a vote                                     | `api/v2/votes/`                                 |
| **GET**/api/v2/office/`<int:office_id>`/result| Get election results for specific office        | `/api/v2/office/<int:office_id>/result`        |
| **GET** /api/v2/users                         | Get list of users                               | `/api/v2/users`                                 |

## Version 1
| **Endpoint**                                    | **Functionality**                               | **Route**                                                       |
| ---                                             | ---                                             | ---                                                             |
| **POST** /parties                               | Creates a political party                       | `/api/v1/parties/`                                              |
| **GET** /parties/`<int:party-id>`               | Gets a specific political party                 | `/api/v1/parties/<int:party_id>`                  |
| **GET** /parties                                | Gets all political parties                      | `/api/v1/parties/`                                              |
| **PATCH** /parties/`<party-id>`/name            | Edit the name of a specific political party.    | `/api/v1/parties/<int:party-id>/<string:name>`    |
| **DELETE** /parties/`<party-id>`                | Delete a political party                        | `/api/v1/parties/<int:party-id>`                  |
| **POST** /offices                               | Create a political office.                      | `/api/v1/offices/`                                              |
| **GET** /offices                                | Fetch all political offices records             | `api/v1/offices/`                                               |
| **GET** /offices/`<int:office_id>`              | Fetch a specific political office record        | `api/v1/offices/<int:office_id>`                 |
| **POST** /register/                             | Register user to the database                   | `api/v1/register/`                                              |
| **POST** /candidates/                           | Create a political candidate                    | `api/v1/candidates/`                                            |
| **POST** /votes/                                | Cast a vote                                     | `api/v1/votes/`                                                 |
| **GET** /votes/user/`<int:user-id>`             | Get all votes by a specific user                | `api/v1/votes/user/<int:user-id>`                   |
| **GET** /votes/candidate/`<int:candidate-id>`   | Get all votes for specific candidate            | `api/v1/votes/canidate/<int:candidate-id>`              |
| **GET** /votes/office/`<int:office-id>`         | Get all votes for a specific office             | `api/v1/votes/office/<int:office-id>`                 |

## Authors / Creators
[Bedan Kamau](https://github.com/bedann)

[Tevin Thuku](https://github.com/Tevinthuku)

[Brian Misocho](https://github.com/misocho)

[Benson Njungé](https://github.com/bencyn)

[Antony Muriithi](https://github.com/justMuriithi)

[Trevor](https://github.com/kburudi)

[Martin Mutuma](https://github.com/martinMutuma)