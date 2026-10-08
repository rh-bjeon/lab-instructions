# Module 5 - The Library

> AI에게 기억하는 법을 가르치는 것은 도서관 카드를 쥐어주는 것과 같습니다. 외부 지식에 접근할 수 없다면, 가장 뛰어난 모델조차도 학습 당시 배운 것에만 한정됩니다. RAG를 사용하면, 여러분의 AI는 여러분이 제공하는 어떤 문서든 찾아보고, 그로부터 배우고, 추론할 수 있습니다 📚

# 🧑‍🍳 모듈 소개

이 모듈은 기본적인 AI 상호작용과, 여러분의 특정 문서 및 지식 베이스로부터 학습하고 기억할 수 있는 지능형 시스템 사이의 간극을 메워줍니다. Retrieval Augmented Generation (RAG)이 어떻게 정적인 AI 모델을 강의 자료, 기관 문서, 학생 제출물을 참조할 수 있는 동적인 assistant로 바꾸어주는지 알아보게 될 것입니다.

RDU에서는, 교육자와 학생들이 방대한 양의 학술 콘텐츠와 상호작용할 수 있도록 Canopy를 구축하고 있습니다. RAG는 이를 가능하게 하는 기술로, 여러분의 문서를 검색하고 질의할 수 있는 지식으로 변환하여 모든 AI 상호작용을 향상시킵니다.

# 🖼️ 큰 그림
![big-picture-rag](images/big-picture-rag.jpg)

# 🔮 학습 성과

* RAG가 무엇이며 AI에게 여러분의 강의 자료에 대한 접근 권한을 어떻게 부여하는지 이해합니다
* Open GenAI Stack (OGX)으로 vector database를 배포하고 RAG 시스템을 구축합니다
* Docling을 사용해 복잡한 PDF와 문서를 처리합니다
* 출처를 인용하는 지능형 교육용 assistant를 만듭니다
* GitOps를 사용해 production에 사용할 수 있는 지식 시스템을 배포합니다

![LLS RAG Pic](images/rag0.png ':size=50%')

# 🔨 이 모듈에서 사용하는 도구들

* **[Open GenAI Stack, 이전 이름 Llama Stack](https://ogx-ai.github.io/)** - 생성형 AI 애플리케이션을 구축하기 위한 오픈소스 프레임워크
* **OGX RAG APIs**: retrieval-augmented 애플리케이션을 구축하기 위한 3계층 아키텍처
* **Milvus Vector Database**: 의미 기반 검색(semantic search)과 retrieval을 위한 고성능 vector database
* **Docling**: PDF 분석과 콘텐츠 추출을 위한 고급 문서 처리 pipeline
* **RAG Tools**: 문서 수집(ingestion), chunking, 쿼리 기능
* **Vector IO & KeyValue IO**: 서로 다른 데이터 유형을 위한 저수준 스토리지 인터페이스
* **OpenShift & Helm Charts**: 개발 및 production 환경에 RAG 인프라를 배포하기 위한 도구
* **Enhanced Canopy**: 여러분의 교육용 AI assistant로, 이제 메모리와 문서 인식 기능을 갖추었습니다