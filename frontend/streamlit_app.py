import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Interview Coach", layout="wide")
st.title("🚀 AI Interview Coach")


def safe_json(res):
    try:
        return res.json()
    except:
        st.error("❌ Backend not returning JSON")
        st.text(res.text)
        return None


menu = st.sidebar.selectbox(
    "Select Mode",
    ["Chat", "Upload PDF", "MCQ", "Coding", "Interview", "Weak Areas"]
)


# ------------------ UPLOAD ------------------ #
if menu == "Upload PDF":
    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file and st.button("Upload"):
        res = requests.post(f"{API}/upload/", files={"file": file})
        data = safe_json(res)

        if data:
            st.success(data.get("message") or data.get("error"))


# ------------------ CHAT ------------------ #
elif menu == "Chat":
    q = st.text_input("Ask question")

    if st.button("Ask"):
        res = requests.get(f"{API}/ask/", params={"query": q})
        st.write("Status:", res.status_code)

        data = safe_json(res)

        if data:
            st.success(data.get("response") or data.get("error"))


# ------------------ MCQ ------------------ #
elif menu == "MCQ":
    topic = st.text_input("Enter topic")

    if st.button("Generate MCQs"):
        res = requests.get(f"{API}/mcq/", params={"topic": topic})
        data = safe_json(res)

        if data:
            st.text(data.get("quiz") or data.get("error"))


# ------------------ CODING ------------------ #
elif menu == "Coding":
    topic = st.text_input("Enter topic")

    if st.button("Generate Coding Question"):
        res = requests.get(f"{API}/coding/", params={"topic": topic})
        data = safe_json(res)

        if data:
            st.code(data.get("question") or data.get("error"))


# ------------------ INTERVIEW ------------------ #
elif menu == "Interview":
    if "q" not in st.session_state:
        st.session_state.q = None

    if st.button("Start Interview"):
        res = requests.get(f"{API}/interview/start")
        data = safe_json(res)

        if data:
            st.session_state.q = data.get("question")

    if st.session_state.q:
        st.write(st.session_state.q)
        ans = st.text_input("Your Answer")

        if st.button("Next"):
            res = requests.get(f"{API}/interview/next", params={"answer": ans})
            data = safe_json(res)

            if data:
                st.session_state.q = data.get("response")


# ------------------ WEAK AREAS ------------------ #
elif menu == "Weak Areas":
    if st.button("Analyze"):
        res = requests.get(f"{API}/weak/")
        data = safe_json(res)

        if data:
            st.write(data.get("weak_topics") or data.get("error"))