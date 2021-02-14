runpy () {
    docker run \
        -it \
        --rm \
        --init \
        --workdir /app \
        -v "${PWD}:/app" \
        node:lts-alpine \
        "$@"
}

npm audit fix --force
