x () {
    docker run \
        -it \
        --rm \
        --init \
        --env-file .env.dev \
        -v "${PWD}/../shared:/shared" \
        -v "${PWD}:/app" \
        pocket-galaxy-dev-backend \
        "$@"
}

x python manage.py makemigrations
