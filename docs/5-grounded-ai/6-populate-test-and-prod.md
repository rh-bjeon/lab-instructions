# ⚙️ KFP Pipelines로 RAG 자동화하기

여러분의 document intelligence RAG 시스템은 노트북에서는 잘 동작하지만, 많은 문서를 처리해야 할 때는 어떻게 될까요?
수동 실행은 확장이 어렵고, RDU에는 신뢰할 수 있고 항시 사용 가능한 지능형 문서 처리가 필요합니다.

## 🔍 KFP Pipelines (다시) 소개

이제 **Kubeflow Pipelines (KFP)**를 사용해 여러분의 실험적인 RAG 시스템을, 복잡한 학술 문서를 대규모로 자동 처리할 수 있는 production급 플랫폼으로 전환하겠습니다.

## 🏗️ Document Intelligence RAG Pipeline 아키텍처

지금까지 작업해온, 그리고 자동화하고자 하는 현재 아키텍처는 다음과 같습니다.
특히 새로운 문서가 우리의 vector database로 들어가는 상단 부분을 자동화하려고 합니다.

![Pipeline Architecture](images/rag4.png)

## 스토리지 환경 준비하기

1. 기존의 MinIO를 문서 저장소로 사용하되, 문서를 위한 버킷이 하나 더 필요합니다. `genaiops-gitops/toolings/minio/config.yaml`을 아래와 같이 업데이트하세요:

   ```yaml
   ---
   chart_path: charts/minio
   buckets:
     - name: pipeline
     - name: test-results
     - name: documents # 👈 이것을 추가하세요
   ```

2. 이 변경사항을 커밋합시다!

   ```bash
   cd /opt/app-root/src/genaiops-gitops
   git pull
   git add .
   git commit -m  "🪣 ADD - document bucket 🪣"
   git push
   ```

3. 이제 RDU의 여러 프로그램에 대한 교육계획서(syllabus)를 수집(ingest)해보겠습니다! 다른 교육계획서를 다운로드하고 싶다면 RDU 웹사이트로 이동하세요. 가지고 있던 것을 그대로 사용해도 괜찮습니다. 이 파일을 MinIO의 `documents` 버킷에 업로드하겠습니다.

   [🌲 Redwood Digital University 웹사이트](https://rdu-website-ai501.<CLUSTER_DOMAIN>)

4. [MinIO instance](https://minio-ui-<USER_NAME>-toolings.<CLUSTER_DOMAIN>)로 이동해 자격 증명으로 로그인하세요.

5. `Object Browser`에서 `documents` 버킷으로 이동해 다운로드한 PDF를 드롭하세요.

   ![minio-upload-pdf.gif](./images/minio-upload-pdf.gif)

   ![trash-gif](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG5ia3k0bWdiNWNiMDB4cWhid20yYWc2endsdm12aHZ2aHJmdnQwZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ytSUKYKGw054uqCHpP/giphy.gif)

6. 이제 수집(ingest)할 문서가 준비되었으니, 이를 vector database로 옮길 document ingestion pipeline을 만들어봅시다!

## 🎯 Document Ingestion Pipeline 실행하기

또 다른 pipeline을 실행할 시간입니다!

1. RAG pipeline이 `backend/rag-pipeline/kfp_pipeline.py`에 있는 `backend` 저장소를 clone하세요.

    ```bash
    cd /opt/app-root/src/
    git clone https://<USER_NAME>:<PASSWORD>@gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend.git
    ```

   이것이 여러분의 문서 처리 pipeline입니다. 이 pipeline은 다음을 수행합니다:
   - Docling에 연결합니다
   - 문서를 처리합니다
   - vector database에 연결합니다
   - 처리된 문서를 데이터베이스에 추가합니다

   이 처리 과정의 많은 부분은 pipeline 코드 하단 근처에서 볼 수 있는 아래의 설정/argument들을 기반으로 합니다. 이전과 동일한 작업을 수행하되 이제는 자동화되었다는 점을 빠르게 확인해보세요:

    <div class="highlight" style="background: #f7f7f7; overflow-x: auto; padding: 8px;">
    <pre><code class="language-python"> 
   arguments = {
        "minio_secret_name": "documents", 
        "minio_bucket_name": "documents",  
        "embedding_model": "sentence-transformers/nomic-ai/nomic-embed-text-v1.5",
        "embedding_dimension": 768,
        "chunk_size_tokens": 512,
        "vector_provider": "milvus",
        "docling_service": "http://docling-v0-7-0-predictor.ai501.svc.cluster.local:5001",
        "processing_timeout": 180,
        "llama_stack_url": "http://llama-stack-service:8321",            # We will update these values later
        "prod_llama_stack_url": "http://llama-stack-service-prod:8321",  # We will update these values later
        "model_id": "llama32",
        "temperature": 0.0,
        "max_tokens": 4096,
        "vector_db_id": "docling_vector_db_genaiops",  
        "test_vector_db_alias": "latest" 
    }
   </code></pre>
   </div>

2. 이를 `<USER_NAME>-toolings` 네임스페이스에서 실행하도록 export하여 test와 prod를 가리키게 해봅시다.
   pipeline을 export하려면 다음을 실행해 컴파일하세요.
   ```bash
   cd /opt/app-root/src/backend/rag-pipeline
   python kfp_pipeline.py
   ```
   `backend/rag-pipeline` 폴더 아래에 `document-intelligence-rag.yaml`이라는 파일이 생성됩니다. 이를 로컬 머신으로 다운로드하세요.
   

3. OpenShift AI로 이동해 `<USER_NAME>-toolings` 프로젝트로 들어가세요. 그 안에서 `Pipelines`로 이동해 `Import pipeline`을 클릭합니다.

   ![import-pipeline](images/import-pipeline.png)

4. pipeline에 `Document Ingestion`과 같은 적절한 이름을 지어주고, 방금 다운로드한 yaml 파일을 업로드하세요.

   ![imported-pipeline.png](./images/imported-pipeline.png)

5. 제대로 동작하는지 확인하기 위해 먼저 임시로(ad-hoc) 실행해봅시다. pipeline 화면에서 `Actions`를 누르고 `Create run`을 클릭하세요.

   ![doc-ingest-run.png](./images/doc-ingest-run.png)

6. 실행에 `Ingest physics syllabus`와 같은 이름을 지어주세요. 아래로 스크롤하면 몇 가지 파라미터가 있습니다. Llama Stack 값들을 아래와 같이 변경해야 합니다:

   **llama_stack_url**: `http://llama-stack-service.<USER_NAME>-test.svc.cluster.local:8321`

   **prod_llama_stack_url**: `http://llama-stack-service.<USER_NAME>-prod.svc.cluster.local:8321`


   다음과 같은 모습이어야 합니다:

   ![llama-stack-url](images/llama-stack-url.png)

7.  `Create run`을 눌러 pipeline 실행을 시작하세요 🏃‍♀️

8.  OpenShift AI에서 pipeline의 진행 상황을 모니터링할 수 있습니다.

   ![Pipeline Monitoring](images/rag9.png)

   실행이 완료되기까지 약 5~6분 정도 걸립니다.

9.  궁금한 분들을 위해, 각 단계를 클릭하면 입력, 출력, 로그에 대한 정보를 확인할 수 있습니다:

   ![Pipeline Monitoring](images/rag10.png)

10. 완료되면 Attu에서 새로운 collection을 확인할 수 있습니다. 한번 확인해보세요:
   ```
   https://milvus-test-attu-<USER_NAME>-test.<CLUSTER_DOMAIN>
   ```

   ![attu-new-collections.png](./images/attu-new-collections.png)

### 여러분이 만든 것

🎉 **축하합니다!** 이제 여러분은 test와 production 데이터베이스에 대규모로 문서를 수집(ingest)할 수 있는, production에 사용할 수 있는 문서 처리 pipeline을 갖게 되었습니다.

이제 다음 섹션으로 이동해 애플리케이션 안에서 RAG 기능을 활성화해봅시다! 🚀 
