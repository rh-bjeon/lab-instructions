# Embeddings 이해하기

RAG는 가장 단순한 형태로 보면, 모델이 더 지능적이고 근거 있는(grounded) 답변을 할 수 있도록 프롬프트에 더 많은 정보를 담아 보내는 것일 뿐입니다.

RAG를 사용하면 프롬프트는 다음과 같은 형태가 될 수 있습니다.

```
You are a helpful, respectful and honest assistant named Canopy built to answer scientific questions.
You will be given a question you need to answer, and a context to provide you with information. You must answer the question based as much as possible on this context.
Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.

Context: {context}
Question: {question}
```

질문(이전에는 시스템 프롬프트만으로 단독으로 전송했던 부분)과 컨텍스트를 함께 보낸다는 점에 주목하세요. 여기서 `{something}`은 질문과 컨텍스트 텍스트(또는 원하는 다른 내용)로 채워질 수 있는 변수를 나타냅니다.

하지만 세상의 모든 텍스트 지식을 컨텍스트로 전부 보낼 수는 없습니다. 사실, 보내는 컨텍스트가 적을수록 응답 속도는 더 빨라집니다. 그래서 가능한 한 적으면서도 의미 있는 컨텍스트를 보낼 방법이 필요합니다.

여기에는 여러 선택지가 있는데, 가장 단순한 것은 키워드 검색이지만, 그 대신 **의미적(semantically)**으로 검색할 수 있다면 어떨까요?

**Embeddings**가 바로 이를 가능하게 해줍니다. embeddings에 대해 배우려면 workbench로 이동해 `experiments\5-rag\1-embeddings.ipynb`를 실행해보세요.

완료했다면, 이러한 embeddings를 어떻게 저장할 수 있는지 알아보기 위해 vector databases로 이동하세요.