import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# --- সেটিংস ---
st.set_page_config(page_title="Dream AI Agent")
st.title("Dream AI Agent")
st.write("Ask me anything! I can search the web and summarize information.")

# --- API Keys (সরাসরি বসানো হয়েছে - পরীক্ষার জন্য) ---
# নিরাপদ ব্যবহারের জন্য Streamlit Secrets ব্যবহার করুন।
gemini_api_key = "AIzaSyC2kY_Da5TtxDWCxoV8kVrTGklgnTI7FVA"
tavily_api_key = "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"

# --- Client Setup ---
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')
tavily_client = TavilyClient(api_key=tavily_api_key)

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # 1. Tavily Search
        search_results = tavily_client.search(query=prompt, search_depth="advanced")
        context = search_results["results"]

        # 2. Gemini for Summarization
        prompt_with_context = f"Based on the following context, answer the user's question: {prompt}\n\nContext:\n{context}"
        response = model.generate_content(prompt_with_context)
        
        full_response = response.text
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})