# Soda vendor

### Summary 

:small_blue_diamond: [Requirements](#Requirements)

:small_blue_diamond: [Installing dependencies (not Docker)](#Installing-dependencies)

:small_blue_diamond: [Configuring Environment (not Docker)](#Configuring-environment)

:small_blue_diamond: [Running application](#Running-application)

:small_blue_diamond: [Endpoints](#Endpoints)

## Requirements

### Python (3.13)
- Go to python.org ([here](https://www.python.org/downloads/)) and download Python version 3.13. (if using Python, is needed some modifications)

Or

### Docker (Recommended)
- Go to docker.com ([here](https://www.docker.com/)) and download. (You just need to go to ([running]((#Running-application)))

## Installing dependencies

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
pip install python-dotenv
```


## Configuring Environment
  Before running application, you need to configure environment to add some information
  - First, create a `.env` file to store `DB_url` and your `OPENAI_API_KEY`. Example
```env
DB_URL=sqlite:///./infra/data/soda_vendor.db
OPENAI_API_KEY=super-secret-openai-key
```
  - Go to, `models/engine.py` module and then add the following configuration:
```python
  from dotenv import load_dotenv
  load_dotenv()
```

## Running application

### Docker
```sh
docker-compose infra/docker-compose.yml up –build
or
docker-compose infra/docker-compose.yml up # if already built
```

### Python
```sh
  python core.app:app
  or
  python core.app:app --reload # if wanna hot reload
```
## Endpoints

***POST /soda/chat***

Get user`s prompt, extract his intention and act based on this intention. Responsible to manipulate soda information.

```json
{
  "prompt": "string"
}
```


***POST /transaction/chat***

Get user`s prompt, extract his intention and act based on this intention. Responsible to manipulate transaction information.
User just can read informations about transactions

```json
{
  "prompt": "string"
}
```
