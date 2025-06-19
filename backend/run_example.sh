x () {
    docker run \
        -it \
        --rm \
        --init \
        --env-file .env \
        -v "${PWD}/shared:/shared" \
        -v "${PWD}:/app" \
        pocket-galaxy-back-dev \
        "$@"
}

x python script_example.py
