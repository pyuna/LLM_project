import os
import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, ChatMessage



# OpenAI API 키 설정 (환경 변수나 다른 안전한 방법으로 설정하는 것이 좋습니다)
# openai.api_key = 'your-api-key-here'

# Streamlit 앱 제목
st.set_page_config(page_title="MY LLM Project", page_icon=":bookmark_tabs:")
st.title('Studying English')

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key 👇", key="chatbot_api_key", type="password")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # 사용자가 선택할 수 있는 옵션들
    with st.sidebar:
        options = ['Vocabulary', 'Synonyms', 'Grammar', 'Composition', 'Conversation']
        captions = ["Meaning and example", "Synonyms and usage conditions", "Check the grammar is correct", "Composition for input",
                    "Role-Playing practice"]
        choice = st.radio("Select an avtivity.", options, captions = captions, index=None)
        # choice = st.selectbox('Select an activity:', options)

    # LangChain의 ChatOpenAI 모델 설정
    chat = ChatOpenAI(model="gpt-4")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # 사용자 질문 입력
    if choice == 'Vocabulary':
        user_question = st.text_input("Enter a word to get its definition and example sentence:")
        if user_question:
            prompt = f"Provide a definition and example sentence for the word: {user_question}"
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=prompt)
            ]
            response = chat(messages)
            st.write("Definition and Example:")
            st.write(response.content.strip())

    elif choice == 'Synonyms':
        user_question = st.text_input("Enter a word to find its synonyms and their usage:")
        if user_question:
            prompt = f"Provide synonyms for the word '{user_question}' and explain the context in which each synonym is used."
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=prompt)
            ]
            response = chat(messages)
            st.write("Synonyms and Usage:")
            st.write(response.content.strip())

    elif choice == 'Grammar':
        user_question = st.text_area("Enter a sentence for grammar check:")
        if user_question:
            prompt = f"Correct the grammar of this sentence: {user_question}"
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=prompt)
            ]
            response = chat(messages)
            st.write("Check the grammar:")
            st.write(response.content.strip())

    elif choice == 'Composition':
        user_question = st.text_area("Enter a topic to get a writing prompt:")
        if user_question:
            prompt = f"Provide a writing prompt for this topic: {user_question}"
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=prompt)
            ]
            response = chat(messages)
            st.write("Writing Prompt:")
            st.write(response.content.strip())
    
    elif choice == 'Conversation':
        with st.sidebar:
            role_options = ['Customer', 'Waiter', 'Hotel Receptionist', 'Job Interviewer']
            user_role = st.selectbox('Choose your role:', role_options)
        user_message = st.chat_input("Your message:")

        # if st.button('Send'):
        if user_role == 'Customer':
            system_prompt = "You are a waiter in a restaurant."
        elif user_role == 'Waiter':
            system_prompt = "You are a customer in a restaurant."
        elif user_role == 'Hotel Receptionist':
            system_prompt = "You are a guest booking a room at a hotel."
        else:
            system_prompt = "You are a candidate attending a job interview."

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": system_prompt}
            ]

        if user_message:
            st.session_state.messages.append({"role": "user", "content": user_message})
            with st.chat_message("user"):
                st.markdown(user_message)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in chat.stream(st.session_state.messages):
                    full_response += (response.content or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
