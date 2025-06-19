# from
FROM node:24-alpine3.21
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"

# prepare
WORKDIR /app

# install packages
COPY package*.json ./
RUN npm install

# copy sources (`src/` should be bound)
COPY . .

# run
CMD ["npm", "run", "dev"]
