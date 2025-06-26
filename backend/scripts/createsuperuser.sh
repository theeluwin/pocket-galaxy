x () {
    docker run \
        -it \
        --rm \
        --init \
        --env-file .env \
        -v "${PWD}/../shared:/shared" \
        -v "${PWD}:/app" \
        pocket-galaxy-dev-backend \
        "$@"
}

x python manage.py createsuperuser
