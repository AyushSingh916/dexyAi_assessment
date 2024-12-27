import streamlit as st
import requests

FLASK_BACKEND_URL = "http://127.0.0.1:5000"

st.title("Wellfound Message Manager")

thread_url = st.text_input("Enter the Wellfound message thread URL", placeholder="https://wellfound.com/jobs/messages/966605550")

response_message = st.text_area("Enter your message", placeholder="Type your message here...")

def get_all_messages(thread_url):
    try:
        response = requests.get(f"{FLASK_BACKEND_URL}/display_conversation", params={"thread_url": thread_url})
        if response.status_code == 200:
            result = response.json()
            conversation_info = result.get("conversation")
            messages_info = result.get("messages")

            if conversation_info and messages_info:
                return conversation_info, messages_info
            else:
                st.error("Failed to fetch conversation data.")
                return None, None
        else:
            st.error(f"Backend error: {response.text}")
            return None, None
    except requests.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None, None

if thread_url.strip():
    conversation_info, messages_info = get_all_messages(thread_url)
    if conversation_info and messages_info:
        st.subheader("Conversation Info:")
        st.write(conversation_info)

        st.subheader("Message Thread:")
        st.write(messages_info)
    else:
        st.info("No messages found or unable to fetch messages.")

if st.button("Send Message"):
    if not thread_url.strip() or not response_message.strip():
        st.error("Thread URL and message cannot be empty.")
    else:
        try:
            payload = {
                "thread_url": thread_url,
                "response": response_message
            }
            response = requests.post(f"{FLASK_BACKEND_URL}/send_message", json=payload)
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    st.success("Message sent successfully!")
                    st.write(result.get("data"))
                else:
                    st.error(f"Failed to send message: {result.get('error')}")
            else:
                st.error(f"Backend error: {response.text}")
        except requests.RequestException as e:
            st.error(f"Connection error: {str(e)}")
