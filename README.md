# Cache for Artifacts MMO
## Features
currently caches
- maps
- monsters
- items
- resources

Should return exactly the same data format(barring some bug)
Provides a request based way of marking specific endpoints as invalid
Provides Non Paginated endpoints that still allow querying
## Setup
1. setup a python 3.12 virtual environment
`python 3.12 -m venv .venv`
`.venv/bin/activate`
2. install requirements
`python3.12 -m pip install -r requirements.txt`
3. Create database 
`python3.12 src/environment.py`
4. Put your API key in the file `data/apikey`
5. Run FastAPI Server using either
`fastapi dev src/server.py`
`fastapi run src/server.py`
