runpy () {
    docker run \
        -it \
        --rm \
        --init \
        --env-file .env \
        -v "${PWD}/shared:/shared" \
        -v "${PWD}:/app" \
        pocket-galaxy-back-dev \
        python "$@"
}

runpy main.py
