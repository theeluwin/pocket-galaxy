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

x flake8 .
x coverage run manage.py test
x coverage report -m
