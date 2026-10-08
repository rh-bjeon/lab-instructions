# Vector Databases - Milvus

이제 embeddings가 무엇인지 알았으니, 이를 어딘가에 저장하고 검색할 수 있어야 하는데, 가능하면 로컬에만 저장하는 방식은 피하는 것이 좋습니다.
이를 위해 고성능 오픈소스 **Vector Database**인 Milvus를 사용하겠습니다 (이전 장에서 보았듯이 embeddings는 벡터이므로 vector database와 완벽하게 맞아떨어집니다).
Vector database는 수백만 개의 벡터를 효율적으로 저장하고 검색할 수 있도록 최적화되어 있습니다.

## Milvus 사용하기

1. Milvus를 사용하기 전에, 먼저 우리 Canopy 프로젝트 안에 배포해보겠습니다.

    OpenShift console -> Helm -> Releases로 이동한 뒤 (`<USER_NAME>-canopy` 프로젝트에 있는지 확인하세요) -> Create Helm Release를 눌러 Milvus를 배포합니다.

    yaml 화면이 보이면 설정을 바꿀 필요 없이 다시 `Create`를 누릅니다.

    ![deploy-milvus](./images/deploy-milvus.png)

2. Milvus가 완전히 배포될 때까지 기다립니다.
    Milvus와 함께 **Attu**라는 것도 함께 배포되는 것을 볼 수 있습니다. Attu는 Milvus의 프런트엔드로, Milvus에 저장된 벡터들을 browse할 때 사용할 수 있습니다.
    열어서 어떤 모습인지 확인해보세요.

    ![open-attu](./images/open-attu.png)

3. Attu에 로그인하려면 다음 Address와 Database를 사용하세요:
    - Milvus Address: `http://milvus.<USER_NAME>-canopy.svc.cluster.local:19530`
    - Database: `default`

    ![attu](./images/attu.png)

    약속하건대, 곧 훨씬 더 흥미로운 모습을 보게 될 것입니다!

4. workbench로 이동해 `experiments/5-rag/2-vector-databases.ipynb` 노트북을 실행해보세요.

노트북을 마쳤다면, 더 복잡한 문서와 형식을 처리하는 방법을 알려주는 [Docling](4-docling.md)에 대해 계속 배워볼 수 있습니다.
