import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")

def _init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}
        ]

def _get_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def _generate_reply(client, model, prompt):
    # 단순히 전체 대화(또는 필요한 프롬프트)를 전달해 응답을 생성합니다.
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    # SDK 응답 객체에서 text 속성이 있는 경우 반환, 없으면 전체 객체 문자열화
    return getattr(response, "text", str(response))

def main():
    _init_session()

    st.title("어르신 복지 상담 챗봇")

    client = _get_client()
    if client is None:
        st.error("GEMINI_API_KEY가 설정되어 있지 않습니다. Streamlit secrets에 GEMINI_API_KEY를 추가하세요.")
        st.info("설정 예: .streamlit/secrets.toml 에 `GEMINI_API_KEY = \"your_api_key\"` 추가")
        return

    # 사이드바: 모델 선택과 초기화
    model = st.sidebar.selectbox("모델 선택", ["gemini-2.5-flash", "gemini-1.0"], index=0)
    if st.sidebar.button("대화 초기화"):
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}]

    # 이전 메시지 렌더링
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # 사용자 입력 처리
    user_input = st.chat_input("메시지를 입력하세요...")
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 모델에 전달할 프롬프트 구성 (간단하게 전체 대화 텍스트로 연결)
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

        with st.spinner("응답 생성 중..."):
            try:
                reply_text = _generate_reply(client, model, prompt)
            except Exception as e:
                reply_text = f"오류가 발생했습니다: {e}"

        # 어시스턴트 메시지 추가 및 화면 갱신
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
        st.experimental_rerun()

if __name__ == '__main__':
    main()
