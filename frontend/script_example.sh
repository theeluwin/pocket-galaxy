x () {
    docker run \
        -it \
        --rm \
        --init \
        -v "${PWD}:/app" \
        pocket-galaxy-dev-frontend \
        "$@"
}

x npm audit fix
