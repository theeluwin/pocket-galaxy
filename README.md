# Pocket Galaxy

![Luna's Pocket Galaxy](concept.png)

A [Django](https://www.djangoproject.com) + [Vue](https://vuejs.org/)([Vuetify](https://vuetifyjs.com)) boilerplate with minimal JWT authentication.

This project supports:

* JWT-based authentication.
  * refresh token is assumed to be inside the HTTP Only Cookies
* Django's `runserver`-based backend development environment.
* Vue's vite-based frontend development environment.
* nginx for development/production environment, respectively.

All backend related stuffs will use reverse proxy of `/api` (via nginx).

In summary, nginx will

* 80 &rightarrow; URL `/static` &rightarrow; Path `/shared/staticfiles`
* 80 &rightarrow; URL `/media` &rightarrow; Path `/shared/mediafiles`
* 80 &rightarrow; URL `/api` &rightarrow; Proxy 8000 (backend server)
* 80 &rightarrow; URL `/` &rightarrow; Serve frontend
  * In case of development, Proxy 5173 (frontend server)

By default, all logs are stored in `/shared/logfiles` and all DBs are stored in `/shared/dbfiles`.

### Developement

Create `.env.dev` file under `/backend/`. See `/backend/README.md` and `/backend/.env.sample`.

Then, use docker compose.

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

Or, just simply

```bash
./run_dev.sh
```

Then, go to browser's `localhost`.

### Production

Create `.env.prod` file under `/backend/`. See `/backend/README.md` and `/backend/.env.sample`.

Then, we build it in a one docker image (use ECS or somethig).

```bash
docker build -t pocket-galaxy -f Dockerfile.prod .
docker stop pocket-galaxy-container
docker rm pocket-galaxy-container
docker run \
    -d \
    --publish 80:80 \
    --volume ./shared:/shared \
    --env-file ./backend/.env.prod \
    --name pocket-galaxy-container \
    pocket-galaxy
```

Or, just simply

```bash
./run_prod.sh
```

To change the host, edit `/backend/.env` and `/nginx/prod.conf`.

---

For more details, read `README.md` files inside each `/backend/` and `/frontend/`.
