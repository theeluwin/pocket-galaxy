# Pocket Galaxy / Frontend

Basic features like login and displaying the list are included by default.

Usually, when using it individually, you might also use things like list filtering or gallery views.
However, from this point on, you'll need to implement those yourself using Vue and Vuetify.

See [blitz-quiz](https://github.com/theeluwin/blitz-quiz) for the use case.

## Development Environment

Install packages for local development environment.

```bash
npm install
```

Note that the folder `./src/` is volume-bound. Since it's in development mode, changes are reflected in real time.

### Build Development Image

Only needed for the first time and when packages change.

```bash
./scripts/build.sh
```

### Modifying Packages

In the development environment, only the `./src/` folder is volume-bound.
So if you want to modify things like `./package.json`, you'll need to run a separate container.
See `./script_example.sh` for reference.

### Where to start?

Most of the time, your primary focus will be on the `./src/` directory. You can safely ignore the other parts for now.

### Run Development Server

See the root `/README.md`.

## Production Environment

See the root `/README.md`.
