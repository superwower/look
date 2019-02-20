# Server for face attendance taking app

## Setup

Copy setting file `config.sample.cfg` to `instance` directory and specify the filename when you run the server.

```bash
mkdir -p instance
cp config.sample.cfg instance/config.cfg
FLASK_APP="look:create_app('config.cfg')" pipenv run flask run -h 0.0.0.0
```

## Configuration

- `COLLECTION_ID`
  collection id of Rekognition to search for faces

- `ATTENDANCE_SERVICE_ENDPOINT`:
  endpoint for the attendance taking server
