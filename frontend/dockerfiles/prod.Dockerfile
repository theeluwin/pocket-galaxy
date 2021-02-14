# build stage
FROM node:lts-alpine AS build-stage
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG API_PREFIX
ARG MEDIA_PREFIX
ENV VUE_APP_API_PREFIX=$API_PREFIX
ENV VUE_APP_MEDIA_PREFIX=$MEDIA_PREFIX
RUN npm run build

# production stage
FROM nginx:stable-alpine AS production-stage
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
