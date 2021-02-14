# Pocket Galaxy

![Luna's Pocket Galaxy](concept.png)

아주 간단한 개인용, 혹은 내부용 툴을 만들어야하는데 이왕이면 웹이 편하죠?

그럴때를 위해 만들어둔 [django](https://www.djangoproject.com/)와 vue([vuetify](https://vuetifyjs.com/en/))로 이뤄진 boilerplate 입니다.

각 폴더에 있는 설명서대로 실행을 시키면 일단 당장 뭔가가 돌아갑니다. 거기서부터 슥슥 수정해서 사용하면 끝~

로그인 기능 정도는 있지만 API도 그렇고 전반적으로 보안은 전혀 없다고 봐도 됨.

사용 예시: 이미지 한 1,000장 정도 라벨링을 해야하는데 UI가 있으면 편할것 같고 둘이서 나눠서 작업하고 싶을때. 근데 웹사이트 초기 세팅이 귀찮을때.

AWS 같은데에 올리고 싶다면 API 보안 설정 좀 더 해야하고 (drf 참고) DB도 외부로 빼야하고 ECS에 백, 프론트 나눠서 각각 올리는걸 추천.
