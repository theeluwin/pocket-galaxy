docker build -t pocket-galaxy -f Dockerfile.prod .
docker stop pocket-galaxy-container 2>/dev/null || true
docker rm pocket-galaxy-container 2>/dev/null || true
docker run \
    -d \
    --publish 80:80 \
    --volume ./shared:/shared \
    --env-file ./backend/.env.prod \
    --name pocket-galaxy-container \
    pocket-galaxy
