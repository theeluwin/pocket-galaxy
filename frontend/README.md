# Pocket Galaxy Frontend

로그인 하는 부분, 리스트 받아서 보여주는 부분까지 기본으로 탑재되어있음.

보통 혼자 쓸 때엔 리스트 필터링이라던가 갤러리던가 하는 부분까지 같이 쓰지만.. 여기서부턴 vue를 써서 각자 알아서 만들어야하는 부분이므로..

토큰 관리를 하다 말아서 가끔 최상위 URL로 들어가서 직접 로그아웃 해야하는? 그런 상황이 종종 나옴 이런..

## 환경 변수 (필수)

`.env` 파일 예시 (`frontend/` 아래에)

```bash
WEB_PORT=8002
API_PREFIX=http://localhost:8001/api
MEDIA_PREFIX=http://localhost:8001/media
```

## 개발 환경

보면 내부의 port랑 외부의 port가 같은데, 이거 webpack 디버그 모드에서 일치해야해서 그런거임 (브라우저 console에서 계속 소켓 에러 뜸). 양해 바람.

`frontend/src/` 폴더부터 볼륨 바인드 되어있음. 개발모드라서 실시간으로 업데이트됨.

### 개발 빌드

```bash
docker-compose --project-directory . -f compose/dev.yml build
```

### 개발 실행

```bash
docker-compose --project-directory . -f compose/dev.yml up --build
```

## 배포 환경

이 프로젝트는 배포 환경을 가정하지 않고 있지만 오래 켜두고 싶은 경우를 위해서 제공.

빌드가 끝난 파일들이 도커 이미지 안에 들어가게되고 그럭저럭 안정적으로 구동됨. nginx 사용.

### 배포 빌드

```bash
docker-compose --project-directory . -f compose/prod.yml build
```

### 배포 실행

```bash
docker-compose --project-directory . -f compose/prod.yml up -d --build
```

## NPM 관련

개발 환경도 `frontend/src/` 아래에서부터만 바인드 되어있기 때문에 `package.json` 같은걸 수정하려면 별도로 run을 해줘야함. `run.sh` 참고.

```bash
runpy () {
    docker run \
        -it \
        --rm \
        --init \
        --workdir /app \
        -v "${PWD}:/app" \
        node:lts-alpine \
        "$@"
}

npm audit fix --force
```
