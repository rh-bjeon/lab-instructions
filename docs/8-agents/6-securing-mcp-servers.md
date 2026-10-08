# MCP 서버 보안 적용하기

이제 agent는 강력한 도구들을 갖게 되었습니다 - 캘린더를 읽고, 미팅을 예약하고, 민감한 데이터에 접근할 수 있습니다. 그런데 잠깐... 누가 이 도구들을 사용할 수 있도록 허용되어 있을까요? 지금은 **누구나** MCP 서버에 접근할 수 있습니다!

대학 도서관을 떠올려 보세요. 개가식 서가(open stacks)는 누구에게나 열려 있지만, 희귀 도서 컬렉션은 어떨까요? 학생증을 보여줘야 합니다. MCP 서버도 같은 방식으로 동작합니다 - 누가 문을 두드리고 있는지 확인하기 위해 **OAuth 2.1**을 사용합니다.

## 언제 인증이 필요한가?

[MCP Authorization Guide](https://modelcontextprotocol.io/docs/tutorials/security/authorization#when-should-you-use-authorization)에 따르면, 다음과 같은 경우 보안이 필요합니다.

- **여러 사용자**(multiple users)가 서버에 접근하는 경우 (각자 다른 권한을 가짐)
- **민감한 데이터**(sensitive data)가 관련된 경우 (캘린더, 성적, 개인정보)
- **쓰기 작업**(write operations)이 상태를 변경할 수 있는 경우 (이벤트 생성/삭제)

우리의 calendar MCP 서버는 이 세 가지 항목 모두에 해당합니다! 학생들은 자신의 이벤트만 볼 수 있어야 하며, 무작위 요청이 가짜 미팅을 만들어내는 것도 원하지 않습니다.

## MCP 인증(Authorization) 흐름

OAuth를 활용한 MCP의 토큰 기반 보안이 동작하는 방식은 다음과 같습니다.

![MCP OAuth Flow](images/mcp-auth.png)

**무슨 일이 일어나고 있나요:**

1. 클라이언트가 토큰 없이 MCP 서버에 접근을 시도 → **401 Unauthorized**
2. 클라이언트가 Keycloak으로 인증(사용자 이름 + 비밀번호)
3. Keycloak이 부여된 scope가 담긴 **access token**을 반환
4. 클라이언트가 `Authorization: Bearer <token>`으로 재시도
5. MCP 서버가 **introspection**을 통해 토큰을 검증
6. 유효하다면, 요청이 Calendar API로 진행됨
7. 성공!

핵심은 이것입니다: MCP 서버는 비밀번호를 절대 보지 않습니다. 신뢰할 수 있는 기관(Keycloak)이 발급한 토큰만 검증할 뿐입니다.

## 직접 해보기

워크벤치에서 `8-agents/5-mcp-servers-auth.ipynb` 노트북을 열어 OAuth가 실제로 동작하는 모습을 확인하세요.

## 핵심 요약

| 개념 | 왜 중요한가 |
|---------|----------------|
| **Authentication (인증)** | 유효한 자격 증명을 가진 사용자만 토큰을 받습니다 |
| **Authorization (권한 부여)** | Scope가 어떤 작업이 허용되는지를 제어합니다 |
| **Token Expiration (토큰 만료)** | 토큰은 10분 후 만료되어 노출 범위를 제한합니다 |
| **Centralized Control (중앙 집중 관리)** | Keycloak이 사용자, 클라이언트, 권한을 관리합니다 |

OAuth로 MCP 서버를 보호하면, 무단 접근을 걱정하지 않고도 프로덕션에 agent를 안전하게 배포할 수 있습니다!

---

## 🤔 생각해 볼 질문

MCP 서버는 보안을 적용했습니다... 하지만 이것이 전체 그림일까요? 생각해 보세요: **우리의 agentic 아키텍처에는 또 어떤 공격 표면(attack surface)이 존재할까요?**
