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

    # 사이드바: 모델 선택 대신 '질문 요청' 입력창 제공
    question_request = st.sidebar.text_area("질문 요청", help="어르신이 하실 질문을 입력하세요.")
    if st.sidebar.button("질문 전송"):
        qr = question_request.strip()
        if qr:
            # 사용자 메시지로 추가
            st.session_state.messages.append({"role": "user", "content": qr})

            # 모델에 전달할 프롬프트 구성 (어르신 대상 상냥한 말투 포함)
            system_instruction = (
                "당신은 어르신(노년층)을 대상으로 상냥하고 친절한 말투로 응답하는 상담 도우미입니다. "
                "존댓말을 사용하고, 천천히, 친절하게 설명하세요. 어려운 용어는 쉬운 말로 풀어 설명하고, "
                "한 번에 한 가지 정보를 제공하며 배려심 있고 공손한 표현을 사용하세요."
            )
            conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            prompt = system_instruction + "\n\n" + conversation_text

            with st.spinner("응답 생성 중..."):
                try:
                    # 고정 모델명을 사용하여 요청(필요시 변경 가능)
                    reply_text = _generate_reply(client, "gemini-2.5-flash", prompt)
                except Exception as e:
                    reply_text = "죄송합니다. 응답을 생성할 수 없습니다."
                    st.exception(e)

            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            st.experimental_rerun()

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

        # 모델에 전달할 프롬프트 구성
        # 어르신을 위한 상냥하고 친절한 말투를 유지하도록 시스템 지침을 프롬프트 앞에 추가합니다.
        system_instruction = (
            "당신은 어르신(노년층)을 대상으로 상냥하고 친절한 말투로 응답하는 상담 도우미입니다. "
            "존댓말을 사용하고, 천천히, 친절하게 설명하세요. 어려운 용어는 쉬운 말로 풀어 설명하고, "
            "한 번에 한 가지 정보를 제공하며 배려심 있고 공손한 표현을 사용하세요."
        )
        conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        prompt = system_instruction + "\n\n" + conversation_text

        with st.spinner("응답 생성 중..."):
            try:
                reply_text = _generate_reply(client, model, prompt)
            except Exception as e:
                reply_text = f"오류가 발생했습니다: {e}"

        # 어시스턴트 메시지 추가 및 화면 갱신
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
        st.rerun()

if __name__ == '__main__':
    main()
