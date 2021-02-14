# Pocket Galaxy Backend

볼륨 바인드 할 것들은 기본적으로 모두 `backend/shared/` 아래에 있음:

```bash
backend/
    ...
    shared/
        staticfiles/
        mediafiles/
        logfiles/
        dbfiles/
    ...
```

DBMS는 기본적으로 제공되는 sqlite3를 사용.

## 환경 변수 (필수)

`.env` 파일 예시 (`backend/` 아래에)

```bash
WEB_PORT=8001
DJANGO_SECRET_KEY=django_secret_key123
ALLOWED_HOSTS=localhost,your.domain.com
```

이렇게 하면 최종적으로 저 `WEB_PORT`가 진입점이 되도록 설정됨.

## 개발 환경

개발 환경의 경우, 소스코드가 볼륨 바인드로 연결되어있고 `runserver` 기능을 활용하기 때문에 실시간으로 업데이트됨.

static과 media 모두 자체 서빙 제공.

처음에 뭘 하려고 한다면 아래 순서대로 쭉 진행하면 됨.

### 개발 빌드

```bash
docker-compose --project-directory . -f compose/dev.yml build
```

### 마이그레이션 생성

```bash
docker-compose --project-directory . -f compose/dev.yml run --rm app_dev python manage.py makemigrations
```

### 마이그레이션

```bash
docker-compose --project-directory . -f compose/dev.yml run --rm app_dev python manage.py migrate
```

### 어드민 생성

```bash
docker-compose --project-directory . -f compose/dev.yml run --rm app_dev python manage.py createsuperuser
```

### 개발 실행

```bash
docker-compose --project-directory . -f compose/dev.yml up --build
```

## 배포 환경

이 프로젝트는 배포 환경을 가정하지 않고 있지만 오래 켜두고 싶은 경우, `DEBUG=False`로 돌리고 싶은 경우를 위해서 제공.

소스코드가 도커 이미지 안에 들어가게되고 그럭저럭 안정적으로 구동됨. nginx 사용.

### 배포 빌드

```bash
docker-compose --project-directory . -f compose/prod.yml build
```

### 배포 실행

```bash
docker-compose --project-directory . -f compose/prod.yml up -d --build
```

## 기타 작업

`main.py`를 사용하는 예시. `run.sh` 참고.

참고로 tqdm을 쓰려면 compose로 하면 제대로 출력이 안됨.

```bash
docker run \
    -it \
    --rm \
    --init \
    --env-file .env \
    -v "${PWD}/shared:/shared" \
    -v "${PWD}:/app" \
    pocket-galaxy-back-dev \
    python main.py
```
