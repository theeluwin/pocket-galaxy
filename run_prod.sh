docker build -t pocket-galaxy -f Dockerfile.prod .
docker stop pocket-galaxy-container
docker rm pocket-galaxy-container
docker run \
    -d \
    --publish 80:80 \
    --volume ./shared:/shared \
    --env-file ./backend/.env.prod \
    --name pocket-galaxy-container \
    pocket-galaxy
