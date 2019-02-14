# Politico-API
[![Build Status](https://travis-ci.org/bedann/Politico-API.svg?branch=develop)](https://travis-ci.org/bedann/Politico-API)
[![Coverage Status](https://coveralls.io/repos/github/bedann/Politico-API/badge.svg?branch=develop)](https://coveralls.io/github/bedann/Politico-API?branch=develop&kill_cache=1")
[![Maintainability](https://api.codeclimate.com/v1/badges/27c29affb516fca1c66b/maintainability)](https://codeclimate.com/github/bedann/Politico-API/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9e8482450e2c433db8a78376915840cf)](https://app.codacy.com/app/bedann/Politico-API?utm_source=github.com&utm_medium=referral&utm_content=bedann/Politico-API&utm_campaign=Badge_Grade_Dashboard)

The general elections are around the corner, hence it’s a political season. Get into the mood of the season and help build a platform which both the politicians and citizens can use. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## Hosting
The Politico API is hosted on Heroku. You can access it at [Kura Yangu](https://kurayangu.herokuapp.com)

## Requirements
- [VS code](https://code.visualstudio.com/)
- [Python 3.x](https://www.python.org/)
- [Postman](https://www.getpostman.com/downloads/)

<details><summary>Installation</summary>
<p>

#### installation steps

- clone the git repo
```
$ git clone https://github.com/bedann/Politico-API.git
```
- cd into the project directory
```
$ cd Politico-API
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


  | **Endpoint** | **Functionality** | **Route** |
| --- | --- | --- |
| **POST** /parties | Creates a political party | `/api/v1/parties/` |
| **GET** /parties/`<int:party-id>` | Gets a specific political party | `/api/v1/parties/<int:party_id>` |
| **GET** /parties | Gets all political parties | `/api/v1/parties/` |
| **PATCH** /parties/`<party-id>`/name | Edit the name of a specific political party. | `/api/v1/parties/<int:party-id>/<string:name>` |
| **DELETE** /parties/`<party-id>` | Delete a political party | `/api/v1/parties/<int:party-id>` |
| **POST** /offices | Create a political office. | `/api/v1/offices/` |
| **GEt** /offices | Fetch all political offices records | `api/v1/offices/` |
| **GET** /offices/`<int:office_id>` | Fetch a specific political office record | `api/v1/offices/<int:office_id>` |
| **POST** /register/ | Register user to the database | `api/v1/register/` |
| **POST** /candidates/ | Create a political candidate | `api/v1/candidates/` |
| **POST** /votes/ | Cast a vote | `api/v1/votes/` |
| **GET** /votes/user/`<int:user-id>` | Get all votes by a specific user | `api/v1/votes/user/<int:user-id>` |
| **GET** /votes/candidate/`<int:candidate-id>` | Get all votes for specific candidate | `api/v1/votes/canidate/<int:candidate-id>` |
| **GET** /votes/office/`<int:office-id>` | Get all votes for a specific office | `api/v1/votes/office/<int:office-id>` |


## Author
[Bedan Kamau](https://github.com/bedann)

