# 🗂️ 프롬프트 버전 관리

처음 작성했던 시스템 프롬프트를 기억하시나요? 첫 번째 프롬프트는 무엇이었고, 두 번째 프롬프트는 왜 마음에 들지 않았나요?

플레이그라운드에서 반복한 실험을 체계적으로 기록하고 비교할 방법이 필요합니다.

이 문제를 해결하는 두 가지 핵심 개념이 **프롬프트 버전 관리**(prompt versioning)와 **프롬프트 레지스트리**(prompt registry)입니다.

## 🎯 프롬프트 버전 관리가 중요한 이유

좋은 프롬프트는 잘 작성된 함수나 컴포넌트와 같습니다. 한 번 제대로 만들었다면 여러 애플리케이션과 사용자가 다시 활용할 수 있어야 합니다.

하지만 GenAI 워크플로에서는 프롬프트 실험이 **기록되지 않고**, **추적하기 어려우며**, **재사용되지 못하는** 경우가 많습니다. 방금 플레이그라운드에서 한 실험도 마찬가지입니다.

이런 방식은 협업을 어렵게 하고, 규모가 커질수록 같은 결과를 재현하기도 힘들게 만듭니다.

프롬프트를 저장하고 애플리케이션에서 불러오는 방법은 여러 가지입니다. 이번 실습에서는 MLflow Prompt Registry를 사용합니다.

## 프롬프트 레지스트리

프롬프트를 Prompt Registry에 저장하고 필요에 따라 메모와 태그를 추가합니다. 애플리케이션은 실행 중에 레지스트리에서 필요한 프롬프트를 가져옵니다.

1. 왼쪽 메뉴에서 `Gen AI studio` > `Prompts`로 이동합니다. 상단에서 **<USER_NAME>-canopy** 프로젝트를 선택하고, 앞에서 가장 좋은 결과를 냈던 요약 프롬프트를 실험 환경에 저장합니다. 운영 환경은 뒤에서 다룹니다. 🤫🤫🤫

    _참고: 곧 플레이그라운드에서 바로 프롬프트를 저장할 수 있게 될 것입니다._

    ![prompt-registry.png](./images/prompt-registry.png)

2. `Create prompt`를 클릭하고 이름을 다음과 같이 지정하세요: `summarization`. 

    ```bash
    summarization
    ```

    아래 예시 중 가장 좋은 결과를 낸 시스템 프롬프트를 붙여넣습니다. 🫶 변경 내용을 알아보기 쉬운 커밋 메시지도 입력한 뒤 `Create`를 클릭합니다.

    (만약 'You do not have permission to access this resource.'라는 에러가 발생한다면, 프로젝트가 `<USER_NAME>-canopy`로 적절하게 선택되어 있는지 확인하세요)

	```
	Write a short version of this.
	```

	```
	Summarize the text in a few sentences.
	```

	```
	Explain the given text as if I'm a 5-year-old.
	```

	```
	Explain the given text using only emojis.
	```

    ![summarization-prompt-1.png](./images/summarization-prompt-1.png)

    이렇게 프롬프트의 첫 번째 버전(Version 1)이 만들어지고 `latest` 태그가 자동으로 붙습니다.

    ![summarization-prompt-2.png](./images/summarization-prompt-2.png)

    이제 시스템 프롬프트를 실제 애플리케이션에서 사용해 보겠습니다. OpenShift 클러스터의 실험 환경에 Canopy를 배포하고 Prompt Registry에서 프롬프트를 가져오도록 구성합니다.

</content>
