# RPO N4

University assignment involving the implementation of an app using Python (Flask + Pillow) and full Dockerization of the project, including build and run instructions.

## Run with Docker

Build image:

```bash
docker build -t meme-generator .
```

```
docker run -p 5000:5000 meme-generator
```

or

```
docker-compose up --build
```

To open in browser:

http://localhost:5000
