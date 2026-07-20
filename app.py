# import requests
# import streamlit as st

# BACKEND_URL = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="Sapphire Codebase Assistant",
#     page_icon="💎",
#     layout="wide",
# )

# st.markdown("""
# <style>

# .block-container{
#     max-width:1100px;
#     padding-top:2rem;
#     padding-bottom:2rem;
# }

# h1{
#     font-size:2.5rem;
# }

# .stButton>button{
#     width:100%;
#     height:48px;
#     border-radius:12px;
#     font-weight:600;
# }

# .stFileUploader{
#     border-radius:12px;
# }

# [data-testid="stMetric"]{
#     border:1px solid #333;
#     border-radius:12px;
#     padding:12px;
# }

# div[data-testid="stChatMessage"]{
#     border-radius:12px;
# }

# </style>
# """, unsafe_allow_html=True)


# # ------------------------
# # Session State
# # ------------------------

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "indexed" not in st.session_state:
#     st.session_state.indexed = False

# if "stats" not in st.session_state:
#     st.session_state.stats = None


# # ------------------------
# # Header
# # ------------------------

# st.title("💎 Sapphire Codebase Assistant")

# st.caption(
#     "Local Embeddings • ChromaDB • Gemini 2.5 Flash"
# )

# st.divider()


# # ------------------------
# # Upload
# # ------------------------

# st.subheader("📁 Upload Repository")

# uploaded_file = st.file_uploader(
#     "Choose a ZIP repository",
#     type=["zip"],
# )

# if uploaded_file is not None:

#     if st.button("Index Repository"):

#         with st.spinner("Indexing repository..."):

#             response = requests.post(
#                 f"{BACKEND_URL}/upload",
#                 files={
#                     "file": (
#                         uploaded_file.name,
#                         uploaded_file,
#                         "application/zip",
#                     )
#                 },
#             )

#         if response.status_code == 200:

#             data = response.json()

#             st.session_state.indexed = True
#             st.session_state.stats = data

#             st.success("Repository indexed successfully!")

#         else:

#             st.error("Indexing failed.")

#             try:
#                 st.json(response.json())
#             except Exception:
#                 st.text(response.text)


# # ------------------------
# # Metrics
# # ------------------------

# if st.session_state.stats:

#     st.divider()

#     c1, c2 = st.columns(2)

#     with c1:
#         st.metric(
#             "Files",
#             st.session_state.stats["files"],
#         )

#     with c2:
#         st.metric(
#             "Chunks",
#             st.session_state.stats["chunks"],
#         )


# # ------------------------
# # Chat
# # ------------------------

# if st.session_state.indexed:

#     st.divider()

#     st.subheader("💬 Chat")

#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     question = st.chat_input(
#         "Ask anything about the repository..."
#     )

#     if question:

#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": question,
#             }
#         )

#         with st.chat_message("user"):
#             st.markdown(question)

#         with st.chat_message("assistant"):

#             placeholder = st.empty()

#             with st.spinner("Thinking..."):

#                 response = requests.post(
#                     f"{BACKEND_URL}/chat",
#                     json={
#                         "message": question,
#                     },
#                 )

#             if response.status_code == 200:

#                 answer = response.json()["answer"]

#                 placeholder.markdown(answer)

#                 st.session_state.messages.append(
#                     {
#                         "role": "assistant",
#                         "content": answer,
#                     }
#                 )

#             else:

#                 placeholder.error("Backend error.")

#                 try:
#                     st.json(response.json())
#                 except Exception:
#                     st.text(response.text)

# else:

#     st.info(
#         "Upload a repository to start chatting."
#     )


import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Sapphire Codebase Assistant",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"]{
    font-family:'Space Grotesk',sans-serif;
}
.stApp{
    background:
      radial-gradient(circle at top,#18213f 0%,#0b0d14 30%,#050608 100%);
    color:#fff;
}
.block-container{
    max-width:1150px;
    padding-top:2rem;
}
section[data-testid="stSidebar"]{
    background:#0d1019;
    border-right:1px solid #24273a;
}
.card{
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    padding:18px;
    backdrop-filter:blur(12px);
    margin-bottom:15px;
}
.stButton>button{
    width:100%;
    border-radius:14px;
    height:48px;
    background:#6E6BFF;
    color:white;
    border:none;
    font-weight:600;
}
.stTextInput input{
    border-radius:12px!important;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "indexed" not in st.session_state:
    st.session_state.indexed=False
if "stats" not in st.session_state:
    st.session_state.stats=None

with st.sidebar:
    st.markdown("## 💎 Sapphire")
    st.caption("AI Codebase Assistant")
    if st.session_state.stats:
        st.metric("Files", st.session_state.stats.get("files",0))
        st.metric("Chunks", st.session_state.stats.get("chunks",0))
    if st.button("🧹 New Chat"):
        st.session_state.messages=[]

st.title("💎 Sapphire Codebase Assistant")
st.caption("Local Embeddings • ChromaDB • Gemini 2.5 Flash")

tab1, tab2 = st.tabs(["📦 Upload ZIP","🔗 GitHub Repository"])

with tab1:
    uploaded = st.file_uploader("Repository ZIP", type=["zip"])
    if uploaded and st.button("Index ZIP Repository"):
        with st.spinner("Indexing repository..."):
            r=requests.post(
                f"{BACKEND_URL}/upload",
                files={"file":(uploaded.name,uploaded,"application/zip")}
            )
        if r.status_code==200:
            st.session_state.stats=r.json()
            st.session_state.indexed=True
            st.success("Repository indexed successfully.")
        else:
            st.error(r.text)

with tab2:
    url=st.text_input(
        "Public GitHub Repository",
        placeholder="https://github.com/owner/repository"
    )
    if st.button("Index GitHub Repository"):
        if not url:
            st.warning("Enter a repository URL.")
        else:
            with st.spinner("Cloning and indexing repository..."):
                r=requests.post(
                    f"{BACKEND_URL}/github",
                    json={"url":url}
                )
            if r.status_code==200:
                st.session_state.stats=r.json()
                st.session_state.indexed=True
                st.success("Repository indexed successfully.")
            else:
                try:
                    st.error(r.json())
                except Exception:
                    st.error(r.text)

st.divider()

if st.session_state.indexed:
    st.subheader("💬 Chat")

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    q=st.chat_input("Ask anything about the repository...")
    if q:
        st.session_state.messages.append({"role":"user","content":q})
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            holder=st.empty()
            with st.spinner("Thinking..."):
                r=requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message":q}
                )
            if r.status_code==200:
                ans=r.json()["answer"]
                holder.markdown(ans)
                st.session_state.messages.append(
                    {"role":"assistant","content":ans}
                )
            else:
                holder.error("Backend error.")
else:
    st.info("Upload a ZIP or index a public GitHub repository to begin.")
