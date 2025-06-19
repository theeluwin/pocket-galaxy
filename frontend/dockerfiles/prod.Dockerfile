# build stage
FROM node:24-alpine3.21 AS build-stage
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG API_PREFIX
ARG MEDIA_PREFIX
ENV VITE_API_PREFIX=$API_PREFIX
ENV VITE_MEDIA_PREFIX=$MEDIA_PREFIX
RUN npm run build

# production stage
FROM nginx:1.28.0-alpine-slim AS production-stage
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY misc/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
