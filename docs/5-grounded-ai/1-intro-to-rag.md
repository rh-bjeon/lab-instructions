# Playground에서 RAG 사용해보기

RAG를 사용하면 답변을 특정 정보에 "근거(ground)"하게 만들어, 모델이 환각(hallucinating)을 일으키지 않고 해당 정보를 기반으로 답변하도록 유도할 수 있습니다.

이는 프롬프트와 함께 추가 정보/컨텍스트를 함께 전송하고, 어떤 질문에든 답변하기 전에 먼저 그 정보를 참고하도록 하는 추가 지시사항을 더함으로써 이루어집니다.

직접 해봅시다!

가장 먼저, 우리(RDU)가 웹사이트를 가지고 있다는 사실을 아셨나요? 한번 확인해보세요: [https://rdu-website-ai501.<CLUSTER_DOMAIN>/](https://rdu-website-ai501.<CLUSTER_DOMAIN>/)

"Academic Excellence" 섹션에서 프로그램들을 둘러보고, 마음에 드는 프로그램의 "Learn More" 링크를 클릭해 교육계획서(syllabus)를 다운로드해보세요. 프로그램 페이지에 들어가면 "Download Program Info Sheet (PDF)"를 클릭해 다운로드할 수 있습니다! 이제 이 내용에 대해 LLM에게 질문해볼 것입니다 ;)

1. OpenShift AI Dashboard > Gen AI studio > Playground로 이동한 뒤, 프로젝트가 <USER_NAME>-canopy로 선택되어 있는지 확인합니다.

    ![playground](./images/playground.png)

2. `What is the total credits in Biotechnology program in Redwood Digital University?`와 같이 (여러분이 선택한 과목에 맞게) 질문을 던져보세요.

    ![ask-question](./images/ask-question.png)

    그다지 구체적이거나 정확한 답변이 나오지 않죠? 이제 이를 고쳐봅시다!

3. Knowledge 탭으로 이동해 RAG를 켜고, 앞서 RDU 웹사이트에서 다운로드한 PDF를 추가합니다.

    chunk length와 overlap을 얼마로 설정할지 묻는 모달이 나타납니다. 이것들이 무엇인지는 나중에 다시 다루겠지만, 매우 중요한 설정이므로 기억해두세요.

    기본 chunk 설정을 그대로 두고 `Upload`를 누릅니다.

    ![upload-doc](./images/upload-doc.png)

    참고: 50%에서 멈춘 것처럼 보이면 몇 분 정도 기다렸다가 페이지를 새로고침하세요. 새로고침 후 Knowledge 탭으로 가면 업로드된 파일로 표시되어 있을 것입니다.

4. 업로드가 끝날 때까지 기다린 뒤 같은 질문을 다시 해보세요. 이번에는 더 나은 답변을 얻으셨나요? 여러분이 제공한 PDF에 ✨ 근거를 둔(grounded) ✨ 응답이 나오는 것을 확인할 수 있을 것입니다 :)

RAG가 실제로 동작하는 모습을 확인했으니, 이제 이를 Canopy에 구현해봅시다. 이를 위해 RAG basics로 이동해 `embeddings`가 어떻게 동작하는지 알아보겠습니다.