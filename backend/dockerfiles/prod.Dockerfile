# from
FROM python:3.9-slim
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"

# need git
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# envs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# prepare
RUN mkdir -p /shared && \
    mkdir -p /shared/staticfiles && \
    mkdir -p /shared/mediafiles && \
    mkdir -p /shared/logfiles && \
    mkdir -p /shared/dbfiles && \
    mkdir -p /app
WORKDIR /app

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY . .

# run
EXPOSE 8000
CMD ["./scripts/start_prod.sh"]
