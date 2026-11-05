# Playground에서 RAG 사용해보기

RAG를 사용하면 모델이 특정 정보를 근거로 답변하도록 만들 수 있습니다. 관련 자료를 함께 제공하므로 근거 없는 답변, 즉 환각(hallucination)을 줄일 수 있습니다.

RAG는 프롬프트에 관련 정보와 컨텍스트를 추가하고, 모델이 답변하기 전에 그 내용을 참고하도록 지시하는 방식으로 동작합니다.

직접 해봅시다!

먼저 RDU 웹사이트를 확인해 보세요: [https://rdu-website-ai501.<CLUSTER_DOMAIN>/](https://rdu-website-ai501.<CLUSTER_DOMAIN>/)

`Academic Excellence` 섹션에서 프로그램을 둘러보고 관심 있는 프로그램의 `Learn More`를 클릭합니다. 프로그램 페이지에서 `Download Program Info Sheet (PDF)`를 선택해 교육계획서(syllabus)를 다운로드합니다. 잠시 뒤 이 문서의 내용을 LLM에 질문합니다. ;)

1. OpenShift AI Dashboard > Gen AI studio > Playground로 이동한 뒤, 프로젝트가 <USER_NAME>-canopy로 선택되어 있는지 확인합니다.

    ![playground](./images/playground.png)

2. `What is the total credits in Biotechnology program in Redwood Digital University?`와 같이 (여러분이 선택한 과목에 맞게) 질문을 던져보세요.

    ![ask-question](./images/ask-question.png)

    구체적이거나 정확한 답변을 얻기 어렵습니다. 이제 RAG로 개선해 보겠습니다.

3. Knowledge 탭으로 이동해 RAG를 켜고, 앞서 RDU 웹사이트에서 다운로드한 PDF를 추가합니다.

    청크 길이(chunk length)와 중첩(overlap)을 설정하는 창이 나타납니다. 뒤에서 자세히 다루지만 RAG 품질에 큰 영향을 주는 중요한 설정입니다.

    기본 chunk 설정을 그대로 두고 `Upload`를 누릅니다.

    ![upload-doc](./images/upload-doc.png)

    참고: 50%에서 멈춘 것처럼 보이면 몇 분 정도 기다렸다가 페이지를 새로고침하세요. 새로고침 후 Knowledge 탭으로 가면 업로드된 파일로 표시되어 있을 것입니다.

4. 업로드가 끝날 때까지 기다린 뒤 같은 질문을 다시 해보세요. 이번에는 더 나은 답변을 얻으셨나요? 여러분이 제공한 PDF에 ✨ 근거를 둔(grounded) ✨ 응답이 나오는 것을 확인할 수 있을 것입니다 :)

RAG의 효과를 확인했으니 이제 Canopy에 구현하겠습니다. 다음 장에서는 RAG의 기초가 되는 `embedding`의 동작 원리를 알아봅니다.
