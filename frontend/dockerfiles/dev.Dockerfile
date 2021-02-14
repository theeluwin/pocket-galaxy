# from
FROM node:lts-alpine
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"

# prepare
WORKDIR /app

# install packages
COPY package*.json ./
RUN npm install

# copy sources (`src/` should be bound)
COPY . .

# run
CMD ["npm", "run", "serve"]
