# Pocket Galaxy

![Luna's Pocket Galaxy](concept.png)

A [Django](https://www.djangoproject.com) + [Vue](https://vuejs.org/)([Vuetify](https://vuetifyjs.com)) boilerplate with minimal JWT authentication.

Read `README.md` files inside each `backend/` and `frontend/`

This project supports:

* JWT-based authentication.
  * refresh token is assumed to be inside the HTTP Only Cookies
* Django's `runserver`-based backend development environment.
  * with static and media files serving
* NGINX + Gunicorn setup for backend production.
  * thus, abling local test for the production environment.
* Vue's vite-based frontend development environment.
* NGINX setup for frontend production.
  * thus, abling local test for the production environment.
