# streamlit_gemini

간단한 Streamlit 기반 챗봇 예제입니다. Google Gemini(또는 해당하는 생성형 AI SDK)를 사용해 어르신 대상의 복지 상담용 채팅 인터페이스를 제공합니다.

## 주요 기능

- 사이드바에서 `질문 요청`을 입력하고 전송하면 챗봇이 응답합니다.
- 대화는 채팅형 UI로 표시되며, `대화 초기화` 버튼으로 대화를 리셋할 수 있습니다.
- 모델 호출 시 항상 '어르신(노년층)을 대상으로 상냥하고 친절한 말투'로 응답하도록 시스템 지침을 프롬프트에 포함합니다.
- 기본 모델: `gemini-2.5-flash` (필요 시 변경 가능)

## 요구사항

- Python 3.8+ (권장: 3.10)
- Streamlit
- Google 생성형 AI SDK (환경에 따라 패키지명이 `google-generativeai`, `genai` 등으로 달라질 수 있음)

예상 패키지 예시(환경에 맞춰 선택하여 설치):

```powershell
pip install streamlit
pip install google-generativeai
# 또는
pip install genai
```

권장: 프로젝트 루트에 `requirements.txt`를 추가해 관리하세요.

## 기술 스택

- 언어: Python 3.8+ (권장: 3.10)
- 웹 UI: Streamlit (간단한 채팅 UI 구성)
- 생성형 AI SDK: Google 생성형 AI SDK(`google-generativeai`, `genai` 등 환경에 맞는 패키지)
- 배포/환경관리: 가상환경(venv 또는 conda), 환경변수 및 Streamlit secrets
- 개발 툴: Git, 텍스트 에디터(예: VS Code)

참고: SDK 패키지명과 초기화 방식은 배포 시점의 패키지 버전이나 배포형에 따라 달라질 수 있으니 사용 중인 SDK 문서를 확인하세요.

## 설정 (GEMINI API 키)

앱은 환경변수 또는 Streamlit secrets에서 `GEMINI_API_KEY` 값을 읽습니다. 간단한 예시로 로컬 개발에서 Streamlit secrets를 사용하는 방법:

1. 프로젝트 루트에 `.streamlit` 폴더를 만들고 `secrets.toml` 파일을 생성합니다.

```
.streamlit/secrets.toml
```

2. `secrets.toml` 내용 예시:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

> 주의: 실제 키는 절대 공개 저장소에 커밋하지 마세요. 배포 시에는 호스팅 제공자의 비밀 관리 기능을 사용하세요.

## 실행 방법 (로컬, Windows cmd)

가상환경 생성(선택):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

필요 패키지 설치:

```cmd
pip install -r requirements.txt
# 또는 개별 설치
pip install streamlit google-generativeai
```

앱 실행:

```cmd
streamlit run app.py
```

브라우저에서 제공된 로컬 URL(보통 http://localhost:8501)을 열면 앱을 사용할 수 있습니다.

## 코드/구성 참고사항

- 사이드바는 모델 '선택'을 제거하고 대신 `질문 요청` 텍스트 입력을 받아 전송하도록 구현되어 있습니다.
- 모델명을 변경하려면 `app.py`에서 `model = "gemini-2.5-flash"` 값을 수정하세요.
- SDK import/초기화 방식은 환경(패키지 버전)에 따라 달라질 수 있으니, `from google import genai`가 실패하면 사용 중인 패키지 문서를 참고해 import 구문을 조정하세요.
- 프롬프트 길이와 토큰 사용량에 주의하세요. 대화 내용이 길어지면 모델 호출 실패나 과도한 비용이 발생할 수 있으니 필요하면 최근 N개의 메시지만 전송하도록 로직을 추가하세요.

## 문제 해결

- ImportError 발생 시: 설치된 패키지 이름과 버전을 확인하고 올바른 SDK를 설치하세요.
- 인증/키 오류: `.streamlit/secrets.toml` 또는 환경변수를 올바르게 설정했는지 확인하세요.



