# Politico-API
The general elections are around the corner, hence it’s a political season. Get into the mood of the season and help build a platform which both the politicians and citizens can use. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

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
| **GET** /offices | Fetch a specific political office record | `api/v1/offices/<int:office_id>` |


## TODO
- [ ] Create tests
- [ ] Integrate with Travis CI
