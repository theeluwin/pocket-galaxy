docker build -t pocket-galaxy -f Dockerfile.prod .
docker stop pocket-galaxy-container
docker rm pocket-galaxy-container
docker run \
    -d \
    -p 80:80 \
    -v ./shared:/shared \
    --name pocket-galaxy-container \
    pocket-galaxy
