import streamlit as st
import ollama
from tavily import TavilyClient

# এআই এর নাম
AI_NAME = "Dream" 

# Tavily API Key
TAVILY_API_KEY = "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"
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ওয়েবসাইট টাইটেল
st.set_page_config(page_title=f"{AI_NAME} AI Agent", page_icon="🤖")
st.title(f"🤖 {AI_NAME} - AI Agent")
st.write("Ask me anything! I can search the web and summarize information.")

# কথোপকথন ইতিহাস রাখা (Streamlit session state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের মেসেজগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ব্যবহারকারীর ইনপুট
if prompt := st.chat_input("Ask your question..."):
    # ব্যবহারকারীর মেসেজ যোগ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই এর রেসপন্স
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Searching the web... 🔎")
        
        try:
            # ১. ইন্টারনেট থেকে তথ্য আনা
            search_result = tavily.search(query=prompt)
            context = "\n".join([res['content'] for res in search_result['results']])
            
            # ২. নির্দেশাবলী (বাংলায় উত্তর দেওয়ার জন্য পরিবর্তিত এবং ইন্ডেন্টেশন ঠিক করা হয়েছে)
            system_instruction = f"You are {AI_NAME}, a friendly AI assistant. " \
                                 f"You must understand and answer in Bengali (বাংলা) if the user asks in Bengali. " \
                                 f"Otherwise, answer in English based on this context: \n{context}"
            
            # কথোপকথন ইতিহাস প্রস্তুত করা
            messages_for_ollama = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                messages_for_ollama.append({"role": msg["role"], "content": msg["content"]})
            
            # ৩. Ollama থেকে উত্তর আনা
            response = ollama.chat(model='llama3', messages=messages_for_ollama)
            ai_response = response['message']['content']
            
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            message_placeholder.markdown(f"Error: {e}")