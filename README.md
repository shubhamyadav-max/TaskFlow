# TaskFlow

Flask task manager, containerised with Docker.

## Run with Docker Compose
```bash
docker compose up --build -d
```
Open http://localhost:5000 (change the host port with `HOST_PORT=8080 docker compose up -d`).

Stop: `docker compose down`

## Run with plain Docker
```bash
docker build -t taskflow .
docker run -d --name taskflow -p 5000:5000 taskflow
```

## Run the tests in Docker
```bash
docker compose --profile test run --rm test
```

## Run locally without Docker
```bash
pip install -r requirements-dev.txt
python app.py        # http://127.0.0.1:5000
pytest
```

## Notes
- Tasks are stored in memory, so they reset when the container restarts.
  Because of this the container runs gunicorn with **1 worker + 4 threads**;
  more workers would each hold a different task list.
- Health endpoint: `/health` (used by the Docker HEALTHCHECK).
