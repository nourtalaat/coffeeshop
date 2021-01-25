# Coffee Shop Full Stack

## Introduction

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development

This project is written in 2 parts, a front-end and a back-end each using a different tech stack such as:

#### Front-end:

The front-end is mainly written in Ionic with the help of NodeJS.

Pre-requisites include:
* NodeJS
* Ionic

To install all of them at once, simply `cd` into the `frontend` directory and using your terminal execute `npm install`, afterwards you'd be ready to use `ionic serve` to start the front-end server.

By default the front-end runs on [localhost:8100](http://localhost:8100). 

[View the README.md within ./frontend for more details.](./frontend/README.md)

#### Back-end:

The back-end is mainly written in Flask/Python.

Pre-requisites include mainly:
* Flask
* Flask-Cors
* Flask-SQLAlchemy
* Jinja2
* python-jose
* SQLAlchemy
* Werkzeug

To install all of them at once, simply `cd` into the `backend` directory and using your terminal execute `pip install -r requirements.txt`

Afterwards you'd be ready to set the environment variables to start the Flask app, this depends on which OS you're on and which command-line environment you're using:

* Windows using CMD:
    * `set FLASK_APP=api.py`
    * `set FLASK_ENV=development`
    * `flask run`

* Windows using PS:
    * `$env:FLASK_APP='api.py'`
    * `$env:FLASK_ENV='development'`
    * `flask run`

* Unix using Bash (e.g. Linux and MacOS):
    * `export FLASK_APP=api.py`
    * `export FLASK_ENV=development`
    * `flask run`

By default the back-end runs on `localhost:5000`, but the back-end doesn't serve an index page so if you visit that link nothing will show up.

## API Endpoints

Base URL: `localhost:5000`

* `GET /drinks`:
    * Description: Retrieves all drinks from the database in the `short` representation
	* Authorization: N/A
    * Parameters: N/A
    * Response: 
		```bash
		{
			'success': true,
			'drinks': [
						{
							'id': int,
							'title': str,
							'recipe': list
						},
						...
					  ]
		}
		```

* `GET /drinks-detail`:
    * Description: Retrieves all drinks from the database in the `long` representation
	* Authorization: Requires user with the `get:drinks-detail` permission
    * Parameters: N/A
    * Response: 
		```bash
		{
			'success': true,
			'drinks': [
						{
							'id': int,
							'title': str,
							'recipe': json
						},
						...
					  ]
		}
		```

* `POST /drinks`:
    * Description: Adds a drink to the database
	* Authorization: Requires user with the `post:drinks` permission
    * Parameters:
		* `title`:
			* Usage: JSON
			* Type: str
			* Default: N/A
		* `recipe`:
			* Usage: JSON
			* Type: JSON
			* Default: N/A
			* Format:
				```bash
				{
					'name': str,
					'color': str,
					'parts': int
				}
				```
    * Response: 
		```bash
		{
			'success': true,
			'drinks': [
						{
							'id': int,
							'title': str,
							'recipe': json
						}
					  ]
		}
		```

* `PATCH /drinks/<id>`:
    * Description: Updates a drink in the database
	* Authorization: Requires user with the `patch:drinks` permission
    * Parameters:
		* `title`:
			* Usage: JSON
			* Type: str
			* Default: N/A
		* `recipe`:
			* Usage: JSON
			* Type: JSON
			* Default: N/A
			* Format:
				```bash
				{
					'name': str,
					'color': str,
					'parts': int
				}
				```
    * Response: 
		```bash
		{
			'success': true,
			'drinks': [
						{
							'id': int,
							'title': str,
							'recipe': json
						}
					]
		}
		```

* `DELETE /drinks/<id>`:
    * Description: Deletes a drink from the database
	* Authorization: Requires user with the `delete:drinks` permission
    * Parameters:
		* `id`:
			* Usage: URL Parameter
			* Type: int
			* Default: N/A
    * Response: 
		```bash
		{
			'success': true,
			'delete': int
		}
		```

## Expected Responses

Aside from the response formats shown above which will return in the case of a successful request, there are a number of responses that return on erroneous responses with which you should be familiar:

* 400, Bad Request:
    * Description: You'll receive this response when the request you submit is invalid (has invalid parameters or malformed request)
    * Status Code: 400
    * Message: `Bad Request`
    * Response:
		```bash
		{
			'success': false,
			"error": 400,
			"message": "bad request"
		}
		```

* 401, Unauthorized:
    * Description: You'll receive this response when the request you submit could not be authorized (due to a missing or an invalid token)
    * Status Code: 401
    * Message: `Unauthorized`
    * Response:
		```bash
		{
			'success': false,
			"error": 401,
			"message": "unauthorized"
		}
		```

* 403, Bad Request:
    * Description: You'll receive this response when the request you submit is forbidden (has insufficient permissions)
    * Status Code: 403
    * Message: `Forbidden`
    * Response:
		```bash
		{
			'success': false,
			"error": 403,
			"message": "forbidden"
		}
		```

* 404, Not Found:
    * Description: You'll receive this response when the request you submit is requesting a resource that does not exist
    * Status Code: 404
    * Message: `Not Found`
    * Response:
		```bash
		{
			'success': false,
			"error": 404,
			"message": "not found"
		}
		```

* 405, Method Not Allowed:
    * Description: You'll receive this response when the request you submit has an unallowed method
    * Status Code: 405
    * Message: `Method Not Allowed`
    * Response:
		```bash
		{
			'success': false,
			"error": 405,
			"message": "method not allowed"
		}
		```

* 422, Unprocessable Entity:
    * Description: You'll receive this response when you try to process a resource in an invalid way 
    * Status Code: 422
    * Message: `Unprocessable`
    * Response:
		```bash
		{
			'success': false,
			"error": 422,
			"message": "unprocessable"
		}
		```

## Testing

A number of tests are included in the `Postman` collection in the file `backend_test.postman_collection.json` inside the `backend` directory.

To run them simply import the file in `Postman` and running them.

## Authors

Your friendly neighborhood software developer, Nour A. Talaat.