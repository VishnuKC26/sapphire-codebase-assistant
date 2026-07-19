# # import requests
# # import streamlit as st

# # BACKEND_URL = "http://127.0.0.1:8000"

# # st.set_page_config(
# #     page_title="Sapphire Codebase Assistant",
# #     page_icon="💎",
# #     layout="wide",
# # )

# # st.markdown("""
# # <style>

# # .block-container{
# #     max-width:1100px;
# #     padding-top:2rem;
# #     padding-bottom:2rem;
# # }

# # h1{
# #     font-size:2.5rem;
# # }

# # .stButton>button{
# #     width:100%;
# #     height:48px;
# #     border-radius:12px;
# #     font-weight:600;
# # }

# # .stFileUploader{
# #     border-radius:12px;
# # }

# # [data-testid="stMetric"]{
# #     border:1px solid #333;
# #     border-radius:12px;
# #     padding:12px;
# # }

# # div[data-testid="stChatMessage"]{
# #     border-radius:12px;
# # }

# # </style>
# # """, unsafe_allow_html=True)


# # # ------------------------
# # # Session State
# # # ------------------------

# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # if "indexed" not in st.session_state:
# #     st.session_state.indexed = False

# # if "stats" not in st.session_state:
# #     st.session_state.stats = None


# # # ------------------------
# # # Header
# # # ------------------------

# # st.title("💎 Sapphire Codebase Assistant")

# # st.caption(
# #     "Local Embeddings • ChromaDB • Gemini 2.5 Flash"
# # )

# # st.divider()


# # # ------------------------
# # # Upload
# # # ------------------------

# # st.subheader("📁 Upload Repository")

# # uploaded_file = st.file_uploader(
# #     "Choose a ZIP repository",
# #     type=["zip"],
# # )

# # if uploaded_file is not None:

# #     if st.button("Index Repository"):

# #         with st.spinner("Indexing repository..."):

# #             response = requests.post(
# #                 f"{BACKEND_URL}/upload",
# #                 files={
# #                     "file": (
# #                         uploaded_file.name,
# #                         uploaded_file,
# #                         "application/zip",
# #                     )
# #                 },
# #             )

# #         if response.status_code == 200:

# #             data = response.json()

# #             st.session_state.indexed = True
# #             st.session_state.stats = data

# #             st.success("Repository indexed successfully!")

# #         else:

# #             st.error("Indexing failed.")

# #             try:
# #                 st.json(response.json())
# #             except Exception:
# #                 st.text(response.text)


# # # ------------------------
# # # Metrics
# # # ------------------------

# # if st.session_state.stats:

# #     st.divider()

# #     c1, c2 = st.columns(2)

# #     with c1:
# #         st.metric(
# #             "Files",
# #             st.session_state.stats["files"],
# #         )

# #     with c2:
# #         st.metric(
# #             "Chunks",
# #             st.session_state.stats["chunks"],
# #         )


# # # ------------------------
# # # Chat
# # # ------------------------

# # if st.session_state.indexed:

# #     st.divider()

# #     st.subheader("💬 Chat")

# #     for message in st.session_state.messages:

# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# #     question = st.chat_input(
# #         "Ask anything about the repository..."
# #     )

# #     if question:

# #         st.session_state.messages.append(
# #             {
# #                 "role": "user",
# #                 "content": question,
# #             }
# #         )

# #         with st.chat_message("user"):
# #             st.markdown(question)

# #         with st.chat_message("assistant"):

# #             placeholder = st.empty()

# #             with st.spinner("Thinking..."):

# #                 response = requests.post(
# #                     f"{BACKEND_URL}/chat",
# #                     json={
# #                         "message": question,
# #                     },
# #                 )

# #             if response.status_code == 200:

# #                 answer = response.json()["answer"]

# #                 placeholder.markdown(answer)

# #                 st.session_state.messages.append(
# #                     {
# #                         "role": "assistant",
# #                         "content": answer,
# #                     }
# #                 )

# #             else:

# #                 placeholder.error("Backend error.")

# #                 try:
# #                     st.json(response.json())
# #                 except Exception:
# #                     st.text(response.text)

# # else:

# #     st.info(
# #         "Upload a repository to start chatting."
# #     )

# import requests
# import streamlit as st

# BACKEND_URL = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="Sapphire",
#     page_icon="◆",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ==========================================================
# # Design tokens
# # ----------------------------------------------------------
# # Background   #0A0F1C  (deep indigo-black, "the mine")
# # Panel        #121A2C  (glass panel base)
# # Panel line   #24304A  (hairline borders)
# # Sapphire     #2E6BFF  (primary accent, gem body)
# # Sapphire lt  #6FA0FF  (highlights / hover)
# # Gold         #E3B34C  (facet glint — used sparingly)
# # Text hi      #EAEEF7
# # Text lo      #7C8AA6
# #
# # Display face : Space Grotesk (geometric, cut-stone angularity)
# # Body face    : Inter
# # Utility/mono : JetBrains Mono (stats, file counts, code refs)
# #
# # Signature element: a faceted "gem-cut" corner — a clipped
# # diagonal notch on cards, bubbles and the uploader — echoing a
# # cut sapphire, used once per surface, never stacked or overused.
# # ==========================================================

# st.markdown("""
# <link rel="preconnect" href="https://fonts.googleapis.com">
# <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

# <style>

# :root{
#     --bg: #0A0F1C;
#     --panel: #121A2C;
#     --panel-2: #16203572;
#     --line: #24304A;
#     --sapphire: #2E6BFF;
#     --sapphire-lt: #6FA0FF;
#     --gold: #E3B34C;
#     --text-hi: #EAEEF7;
#     --text-lo: #7C8AA6;
# }

# /* ---- kill Streamlit chrome ---- */
# #MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"],
# [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display:none !important; }
# .stDeployButton { display:none !important; }

# html, body, [data-testid="stAppViewContainer"]{
#     background:
#         radial-gradient(1200px 600px at 12% -10%, #17264a55 0%, transparent 60%),
#         radial-gradient(900px 500px at 100% 0%, #1a1f3a55 0%, transparent 55%),
#         var(--bg) !important;
#     font-family:'Inter', sans-serif;
#     color: var(--text-hi);
# }

# [data-testid="stAppViewContainer"] > .main{
#     padding-top: 0 !important;
# }

# .block-container{
#     max-width: 900px;
#     padding-top: 3.5rem;
#     padding-bottom: 3rem;
# }

# ::selection{ background: var(--sapphire); color:#fff; }

# /* ---- scrollbar ---- */
# ::-webkit-scrollbar{ width:8px; height:8px; }
# ::-webkit-scrollbar-thumb{ background:var(--line); border-radius:8px; }
# ::-webkit-scrollbar-track{ background:transparent; }

# /* ---- headings ---- */
# h1, h2, h3 { font-family:'Space Grotesk', sans-serif !important; color:var(--text-hi) !important; letter-spacing:-0.01em; }

# /* ---- hero mark ---- */
# .sph-hero{
#     display:flex; align-items:center; gap:18px;
#     margin-bottom: 6px;
# }
# .sph-mark{
#     width:46px; height:46px; flex:0 0 auto;
#     background: linear-gradient(155deg, var(--sapphire-lt), var(--sapphire) 55%, #14245e);
#     clip-path: polygon(50% 0%, 100% 30%, 82% 100%, 18% 100%, 0% 30%);
#     box-shadow: 0 0 0 1px #ffffff14 inset, 0 8px 24px -8px #2e6bff88;
# }
# .sph-title{
#     font-family:'Space Grotesk', sans-serif;
#     font-size: 2.1rem;
#     font-weight:700;
#     line-height:1.1;
#     margin:0;
# }
# .sph-sub{
#     font-family:'JetBrains Mono', monospace;
#     font-size: 0.78rem;
#     letter-spacing: 0.06em;
#     text-transform: uppercase;
#     color: var(--text-lo);
#     margin-top:4px;
# }
# .sph-sub span{ color: var(--gold); }

# .sph-divider{
#     height:1px;
#     background: linear-gradient(90deg, var(--line), transparent 80%);
#     margin: 1.8rem 0 1.6rem 0;
#     border:none;
# }

# /* ---- section eyebrow ---- */
# .sph-eyebrow{
#     font-family:'JetBrains Mono', monospace;
#     font-size:0.72rem;
#     letter-spacing:0.12em;
#     text-transform:uppercase;
#     color: var(--sapphire-lt);
#     margin-bottom: 0.6rem;
#     display:flex; align-items:center; gap:8px;
# }
# .sph-eyebrow::before{
#     content:"";
#     width:6px; height:6px;
#     background: var(--sapphire-lt);
#     clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
#     display:inline-block;
# }

# /* ---- glass panel wrapper (faceted corner) ---- */
# [data-testid="stFileUploaderDropzone"]{
#     background: var(--panel-2) !important;
#     border: 1px solid var(--line) !important;
#     border-radius: 4px 4px 4px 4px;
#     clip-path: polygon(0 0, calc(100% - 22px) 0, 100% 22px, 100% 100%, 0 100%);
#     backdrop-filter: blur(10px);
# }
# [data-testid="stFileUploaderDropzone"] button{
#     background: transparent !important;
#     border: 1px solid var(--sapphire) !important;
#     color: var(--sapphire-lt) !important;
#     border-radius: 6px !important;
# }
# [data-testid="stFileUploaderDropzoneInstructions"] svg{ display:none; }
# [data-testid="stFileUploaderDropzoneInstructions"] span{ color: var(--text-hi) !important; font-family:'Inter'; }
# [data-testid="stFileUploaderDropzoneInstructions"] small{ color: var(--text-lo) !important; }

# /* uploaded file row */
# [data-testid="stFileUploaderFile"]{
#     background: var(--panel) !important;
#     border: 1px solid var(--line) !important;
#     border-radius: 8px !important;
# }

# /* ---- buttons ---- */
# .stButton>button{
#     width:100%;
#     height:46px;
#     border-radius:8px;
#     font-family:'Space Grotesk', sans-serif;
#     font-weight:600;
#     letter-spacing:0.01em;
#     background: linear-gradient(155deg, var(--sapphire-lt), var(--sapphire) 70%);
#     border: none;
#     color: #fff;
#     box-shadow: 0 6px 20px -8px #2e6bffaa;
#     transition: transform .15s ease, box-shadow .15s ease;
# }
# .stButton>button:hover{
#     transform: translateY(-1px);
#     box-shadow: 0 10px 26px -8px #2e6bffcc;
#     color:#fff;
# }
# .stButton>button:active{ transform: translateY(0px); }

# /* ---- metrics ---- */
# [data-testid="stMetric"]{
#     background: var(--panel-2);
#     border:1px solid var(--line);
#     border-radius: 10px;
#     padding: 16px 18px !important;
#     backdrop-filter: blur(10px);
# }
# [data-testid="stMetricLabel"]{
#     font-family:'JetBrains Mono', monospace !important;
#     font-size:0.72rem !important;
#     letter-spacing:0.08em;
#     text-transform:uppercase;
#     color: var(--text-lo) !important;
# }
# [data-testid="stMetricValue"]{
#     font-family:'Space Grotesk', sans-serif !important;
#     color: var(--text-hi) !important;
# }

# /* ---- alerts ---- */
# [data-testid="stAlert"]{
#     background: var(--panel-2) !important;
#     border: 1px solid var(--line) !important;
#     border-radius: 8px !important;
#     color: var(--text-hi) !important;
#     font-family:'Inter';
# }

# /* ---- chat ---- */
# div[data-testid="stChatMessage"]{
#     background: var(--panel) !important;
#     border: 1px solid var(--line) !important;
#     border-radius: 4px;
#     padding: 4px 6px;
# }
# div[data-testid="stChatMessage"]:has(> [data-testid="stChatMessageAvatarUser"]){
#     background: linear-gradient(155deg, #16203a, #121a2c) !important;
#     clip-path: polygon(0 0, 100% 0, 100% 100%, 18px 100%, 0 calc(100% - 18px));
#     border-color: #2e6bff55 !important;
# }
# div[data-testid="stChatMessage"]:has(> [data-testid="stChatMessageAvatarAssistant"]){
#     clip-path: polygon(0 0, 100% 0, 100% calc(100% - 18px), calc(100% - 18px) 100%, 0 100%);
# }
# [data-testid="stChatMessageContent"] p{
#     color: var(--text-hi);
#     font-family:'Inter';
# }

# [data-testid="stChatInput"]{
#     background: var(--panel-2) !important;
#     border: 1px solid var(--line) !important;
#     border-radius: 10px !important;
# }
# [data-testid="stChatInput"] textarea{
#     color: var(--text-hi) !important;
#     font-family:'Inter' !important;
# }

# /* spinner text */
# .stSpinner > div{ color: var(--text-lo) !important; font-family:'JetBrains Mono', monospace; font-size:0.8rem; }

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
# # Hero
# # ------------------------

# st.markdown("""
# <div class="sph-hero">
#     <div class="sph-mark"></div>
#     <div>
#         <p class="sph-title">Sapphire</p>
#         <p class="sph-sub">Codebase Assistant · <span>local embeddings</span> · ChromaDB · Gemini 2.5 Flash</p>
#     </div>
# </div>
# <hr class="sph-divider">
# """, unsafe_allow_html=True)


# # ------------------------
# # Upload
# # ------------------------

# st.markdown('<div class="sph-eyebrow">01 — Upload repository</div>', unsafe_allow_html=True)

# uploaded_file = st.file_uploader(
#     "Choose a ZIP repository",
#     type=["zip"],
#     label_visibility="collapsed",
# )

# if uploaded_file is not None:

#     if st.button("Index repository"):

#         with st.spinner("Indexing repository…"):

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

#             st.success("Repository indexed successfully.")

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

#     st.markdown('<div class="sph-eyebrow" style="margin-top:1.8rem;">Index summary</div>', unsafe_allow_html=True)

#     c1, c2 = st.columns(2)

#     with c1:
#         st.metric("Files", st.session_state.stats["files"])

#     with c2:
#         st.metric("Chunks", st.session_state.stats["chunks"])


# # ------------------------
# # Chat
# # ------------------------

# if st.session_state.indexed:

#     st.markdown('<hr class="sph-divider">', unsafe_allow_html=True)
#     st.markdown('<div class="sph-eyebrow">02 — Ask the codebase</div>', unsafe_allow_html=True)

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     question = st.chat_input("Ask anything about the repository…")

#     if question:

#         st.session_state.messages.append({"role": "user", "content": question})

#         with st.chat_message("user"):
#             st.markdown(question)

#         with st.chat_message("assistant"):

#             placeholder = st.empty()

#             with st.spinner("Thinking…"):

#                 response = requests.post(
#                     f"{BACKEND_URL}/chat",
#                     json={"message": question},
#                 )

#             if response.status_code == 200:

#                 answer = response.json()["answer"]

#                 placeholder.markdown(answer)

#                 st.session_state.messages.append({"role": "assistant", "content": answer})

#             else:

#                 placeholder.error("Backend error.")

#                 try:
#                     st.json(response.json())
#                 except Exception:
#                     st.text(response.text)

# else:
#     st.markdown('<hr class="sph-divider">', unsafe_allow_html=True)
#     st.info("Upload and index a repository to start chatting.")


import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Sapphire",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# Design plan — space theme
# ----------------------------------------------------------
# Subject: a tool that reads a codebase and lets you talk to it.
# Metaphor: mission control charting an unknown system.
#   repository  -> a star chart, unplotted
#   chunking    -> plotting / charting the stars
#   embeddings  -> the chart itself (what lets you navigate it)
#   chat        -> opening a channel to mission control
#
# Palette
#   #05060F void          page background
#   #0B0F1E / #0F1428     panel surfaces
#   #232C4A line          hairlines
#   #8B6CFF nebula        primary accent
#   #A78BFF nebula-lt     highlight / glow
#   #F2C568 gold          markers, used sparingly (instrument-panel accent)
#   #EDEFFA text-hi
#   #8A90B4 text-lo
#
# Type
#   Display : Space Grotesk (a literal fit here, kept restrained)
#   Body    : Inter
#   Utility : JetBrains Mono — telemetry, counters, step index
#
# Layout
#   Same rail structure as before (it's a real fixed sequence:
#   chart the repo, then open a channel) — restyled as instrument
#   markers instead of gem facets.
#
# Signature
#   A hand-built constellation mark in the hero: nodes connected
#   by lines, one node pulses gently (twinkle). Behind everything,
#   a deterministic tiled starfield at low opacity plus one soft
#   nebula glow — restraint kept by not layering more than that.
#
# Lessons carried over from the last build (avoid regressions):
#   - No position:fixed background layers (they get clipped inside
#     Streamlit's own scroll container) — paint backgrounds directly
#     on stAppViewContainer instead.
#   - No height:100% flex hacks on rail markers — use min-height.
#   - Every custom text class is prefixed with its tag (p.sph-x) and
#     !important, so it always outranks Streamlit's own more-specific
#     built-in paragraph selectors.
# ==========================================================

STAR_TILE = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300' viewBox='0 0 300 300'>"
    "<circle cx='97.1' cy='45.3' r='0.6' fill='white' opacity='0.3'/>"
    "<circle cx='160.8' cy='109.7' r='0.6' fill='white' opacity='0.89'/>"
    "<circle cx='64.4' cy='25.8' r='1.2' fill='white' opacity='0.3'/>"
    "<circle cx='27.2' cy='127.4' r='1.6' fill='white' opacity='0.34'/>"
    "<circle cx='67.0' cy='188.2' r='0.6' fill='white' opacity='0.65'/>"
    "<circle cx='119.0' cy='292.9' r='0.6' fill='white' opacity='0.64'/>"
    "<circle cx='40.0' cy='125.7' r='1.6' fill='white' opacity='0.33'/>"
    "<circle cx='92.5' cy='244.8' r='0.8' fill='white' opacity='0.32'/>"
    "<circle cx='171.4' cy='56.4' r='0.6' fill='white' opacity='0.63'/>"
    "<circle cx='18.8' cy='17.9' r='0.8' fill='white' opacity='0.6'/>"
    "<circle cx='159.5' cy='233.2' r='1.2' fill='white' opacity='0.66'/>"
    "<circle cx='136.0' cy='89.9' r='0.8' fill='white' opacity='0.74'/>"
    "<circle cx='73.2' cy='172.3' r='1.6' fill='white' opacity='0.6'/>"
    "<circle cx='103.0' cy='134.7' r='1.6' fill='white' opacity='0.94'/>"
    "<circle cx='35.4' cy='125.4' r='1.0' fill='white' opacity='0.36'/>"
    "<circle cx='146.7' cy='11.8' r='0.6' fill='white' opacity='0.79'/>"
    "<circle cx='171.9' cy='262.6' r='1.0' fill='white' opacity='0.49'/>"
    "<circle cx='105.1' cy='149.0' r='1.2' fill='white' opacity='0.3'/>"
    "<circle cx='28.1' cy='81.0' r='0.6' fill='white' opacity='0.29'/>"
    "<circle cx='210.4' cy='194.1' r='1.2' fill='white' opacity='0.45'/>"
    "<circle cx='115.7' cy='200.6' r='0.6' fill='white' opacity='0.91'/>"
    "<circle cx='106.6' cy='183.3' r='1.2' fill='white' opacity='0.29'/>"
    "<circle cx='230.5' cy='38.8' r='0.8' fill='white' opacity='0.53'/>"
    "<circle cx='275.0' cy='149.0' r='0.8' fill='white' opacity='0.56'/>"
    "<circle cx='164.8' cy='265.0' r='1.2' fill='white' opacity='0.85'/>"
    "<circle cx='83.5' cy='124.6' r='1.0' fill='white' opacity='0.73'/>"
    "<circle cx='114.1' cy='69.2' r='0.6' fill='white' opacity='0.37'/>"
    "<circle cx='69.6' cy='70.0' r='1.2' fill='white' opacity='0.83'/>"
    "<circle cx='54.7' cy='84.6' r='0.8' fill='white' opacity='0.54'/>"
    "<circle cx='110.8' cy='169.9' r='0.8' fill='white' opacity='0.73'/>"
    "<circle cx='154.6' cy='185.3' r='0.6' fill='white' opacity='0.57'/>"
    "<circle cx='261.3' cy='285.6' r='1.6' fill='white' opacity='0.52'/>"
    "<circle cx='119.7' cy='31.1' r='1.2' fill='white' opacity='0.29'/>"
    "<circle cx='20.2' cy='62.6' r='0.8' fill='white' opacity='0.33'/>"
    "<circle cx='180.2' cy='30.7' r='1.6' fill='white' opacity='0.36'/>"
    "<circle cx='30.4' cy='109.1' r='0.6' fill='white' opacity='0.3'/>"
    "<circle cx='62.4' cy='112.9' r='1.0' fill='white' opacity='0.92'/>"
    "<circle cx='180.7' cy='142.2' r='0.6' fill='white' opacity='0.84'/>"
    "<circle cx='297.9' cy='139.8' r='1.2' fill='white' opacity='0.47'/>"
    "<circle cx='43.2' cy='224.9' r='1.0' fill='white' opacity='0.59'/>"
    "<circle cx='207.6' cy='154.9' r='0.8' fill='white' opacity='0.92'/>"
    "<circle cx='158.5' cy='44.0' r='1.6' fill='white' opacity='0.89'/>"
    "<circle cx='227.4' cy='89.4' r='0.6' fill='white' opacity='0.74'/>"
    "<circle cx='78.3' cy='110.0' r='0.8' fill='white' opacity='0.5'/>"
    "<circle cx='66.8' cy='162.5' r='1.6' fill='white' opacity='0.48'/>"
    "<circle cx='66.9' cy='243.5' r='0.8' fill='white' opacity='0.81'/>"
    "<circle cx='245.5' cy='222.0' r='0.8' fill='white' opacity='0.39'/>"
    "<circle cx='147.8' cy='219.3' r='0.6' fill='white' opacity='0.8'/>"
    "<circle cx='141.7' cy='58.1' r='1.6' fill='white' opacity='0.92'/>"
    "<circle cx='134.2' cy='281.1' r='1.0' fill='white' opacity='0.92'/>"
    "<circle cx='109.4' cy='66.1' r='0.8' fill='white' opacity='0.58'/>"
    "<circle cx='101.3' cy='144.8' r='1.6' fill='white' opacity='0.84'/>"
    "<circle cx='143.8' cy='195.9' r='0.6' fill='white' opacity='0.83'/>"
    "<circle cx='36.0' cy='116.6' r='0.8' fill='white' opacity='0.58'/>"
    "<circle cx='53.6' cy='236.7' r='1.0' fill='white' opacity='0.31'/>"
    "</svg>"
)

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>

:root{{
    --void:#05060F;
    --panel:#0F1428;
    --panel-2:#10152a80;
    --line:#232C4A;
    --nebula:#8B6CFF;
    --nebula-lt:#A78BFF;
    --gold:#F2C568;
    --text-hi:#EDEFFA;
    --text-lo:#8A90B4;
}}

#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {{ display:none !important; }}
.stDeployButton {{ display:none !important; }}

html, body {{ background: var(--void) !important; }}

/* Starfield + nebula glow painted directly on the container — no
   fixed-position layers, which can get clipped inside Streamlit's
   own scroll container and hide content below the fold. */
[data-testid="stAppViewContainer"]{{
    background:
        radial-gradient(900px 500px at 82% -6%, #8B6CFF22 0%, transparent 60%),
        radial-gradient(700px 420px at 6% 30%, #5FD9E814 0%, transparent 55%),
        url("{STAR_TILE}"),
        var(--void);
    background-size: auto, auto, 300px 300px, auto;
    background-repeat: no-repeat, no-repeat, repeat, no-repeat;
    font-family:'Inter', sans-serif;
    color: var(--text-hi);
}}
[data-testid="stAppViewContainer"] > .main{{ padding-top:0 !important; }}

.block-container{{ max-width: 880px; padding-top: 3.2rem; padding-bottom: 3rem; }}

::selection{{ background: var(--nebula); color:#fff; }}
::-webkit-scrollbar{{ width:8px; }}
::-webkit-scrollbar-thumb{{ background:var(--line); border-radius:8px; }}
::-webkit-scrollbar-track{{ background:transparent; }}

h1,h2,h3 {{ font-family:'Space Grotesk', sans-serif !important; color:var(--text-hi) !important; }}

/* Baseline: any markdown paragraph not explicitly styled still
   reads clearly on this background rather than falling back to
   Streamlit's own default color. */
[data-testid="stMarkdownContainer"] p{{ color: var(--text-hi) !important; font-family:'Inter', sans-serif !important; }}

/* ---------------- hero ---------------- */
p.sph-kicker{{
    font-family:'JetBrains Mono', monospace !important;
    font-size:0.72rem !important; letter-spacing:0.22em !important; text-transform:uppercase !important;
    color: var(--gold) !important;
    margin: 0 0 10px 0 !important;
}}
.sph-hero{{ display:flex; align-items:center; justify-content:space-between; gap:24px; }}
p.sph-title{{
    font-family:'Space Grotesk', sans-serif !important;
    font-size: clamp(2.4rem, 5vw, 3.4rem) !important;
    font-weight:700 !important; letter-spacing:-0.02em !important; line-height:1 !important;
    margin:0 0 10px 0 !important;
    color: var(--text-hi) !important;
}}
p.sph-desc{{ color:var(--text-lo) !important; font-size:0.95rem !important; max-width:36ch; line-height:1.55 !important; }}
.sph-desc b{{ color:var(--text-hi) !important; font-weight:600 !important; }}

.sph-mark{{ width:112px; height:112px; flex:0 0 auto; }}
.sph-mark .twinkle{{ animation: twinkle 2.6s ease-in-out infinite; transform-origin: center; }}
.sph-mark .twinkle.d2{{ animation-delay: .7s; }}
.sph-mark .twinkle.d3{{ animation-delay: 1.4s; }}
@keyframes twinkle{{
    0%, 100% {{ opacity:0.35; transform:scale(0.85); }}
    50%      {{ opacity:1;    transform:scale(1.15); }}
}}

.sph-divider{{ height:1px; background:linear-gradient(90deg, var(--line), transparent 85%); margin:2rem 0 1.7rem 0; border:none; }}

/* ---------------- rail / step markers ---------------- */
.sph-step-marker{{
    width:30px; height:30px;
    display:flex; align-items:center; justify-content:center;
    font-family:'JetBrains Mono', monospace; font-size:0.7rem; font-weight:500;
    color:var(--gold);
    border: 1px solid var(--gold);
    border-radius: 50%;
    margin-top: 2px;
    box-shadow: 0 0 0 3px #05060F, 0 0 0 4px #f2c56833;
}}
.sph-rail-line{{
    width:1px; min-height:70px;
    background: linear-gradient(var(--line), transparent);
    margin: 8px auto 0 auto;
}}
p.sph-step-label{{
    font-family:'JetBrains Mono', monospace !important; font-size:0.72rem !important;
    letter-spacing:0.14em !important; text-transform:uppercase !important; color:var(--nebula-lt) !important;
    margin-bottom:2px !important;
}}
p.sph-step-title{{ font-family:'Space Grotesk', sans-serif !important; font-size:1.15rem !important; font-weight:600 !important; margin:0 0 4px 0 !important; color:var(--text-hi) !important; }}
p.sph-step-copy{{ color:var(--text-lo) !important; font-size:0.88rem !important; margin-bottom:14px !important; }}

/* ---------------- uploader ---------------- */
[data-testid="stFileUploaderDropzone"]{{
    background: var(--panel-2) !important;
    border: 1px dashed var(--line) !important;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}}
[data-testid="stFileUploaderDropzone"] button{{
    background: transparent !important; border:1px solid var(--nebula) !important;
    color: var(--nebula-lt) !important; border-radius:6px !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] svg{{ display:none; }}
[data-testid="stFileUploaderDropzoneInstructions"] span{{ color:var(--text-hi) !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] small{{ color:var(--text-lo) !important; }}
[data-testid="stFileUploaderFile"]{{ background:var(--panel) !important; border:1px solid var(--line) !important; border-radius:8px !important; }}

/* ---------------- buttons ---------------- */
.stButton>button{{
    width:100%; height:46px; border-radius:8px; border:none;
    font-family:'Space Grotesk', sans-serif; font-weight:600;
    background: linear-gradient(155deg, var(--nebula-lt), var(--nebula) 70%);
    color:#fff; box-shadow: 0 6px 20px -8px #8b6cffaa;
    transition: transform .15s ease, box-shadow .15s ease;
}}
.stButton>button:hover{{ transform: translateY(-1px); box-shadow: 0 10px 26px -8px #8b6cffcc; color:#fff; }}

/* ---------------- readout (custom stat row, replaces st.metric) ---------------- */
.sph-readout{{
    display:flex; gap:1px; background:var(--line);
    border:1px solid var(--line); border-radius:10px; overflow:hidden;
    margin-top:6px;
}}
.sph-readout-cell{{ flex:1; background:var(--panel); padding:14px 18px; }}
.sph-readout-cell .n{{
    font-family:'JetBrains Mono', monospace !important; font-size:1.6rem !important; color:var(--text-hi) !important; line-height:1 !important;
}}
.sph-readout-cell .l{{
    font-family:'JetBrains Mono', monospace !important; font-size:0.68rem !important; letter-spacing:0.1em !important;
    text-transform:uppercase !important; color:var(--text-lo) !important; margin-top:6px !important;
}}

/* ---------------- alerts ---------------- */
[data-testid="stAlert"]{{ background:var(--panel-2) !important; border:1px solid var(--line) !important; border-radius:8px !important; color:var(--text-hi) !important; }}

/* ---------------- chat ---------------- */
div[data-testid="stChatMessage"]{{ background:transparent !important; border:none !important; padding:6px 0 !important; gap:10px; }}
[data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"]{{ display:none !important; }}

div[data-testid="stChatMessage"]:has(> [data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"]{{
    background: var(--panel-2);
    border-left: 2px solid var(--gold);
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin-left: auto;
    max-width: 78%;
}}
div[data-testid="stChatMessage"]:has(> [data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"]{{
    background: var(--panel-2);
    border-left: 2px solid var(--nebula);
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    max-width: 78%;
}}
[data-testid="stChatMessageContent"] p{{ color:var(--text-hi) !important; }}

[data-testid="stChatInput"]{{ background:var(--panel-2) !important; border:1px solid var(--line) !important; border-radius:10px !important; }}
[data-testid="stChatInput"] textarea{{ color:var(--text-hi) !important; }}

.stSpinner > div{{ color:var(--text-lo) !important; font-family:'JetBrains Mono', monospace; font-size:0.8rem; }}

</style>
""", unsafe_allow_html=True)


# ------------------------
# Session State
# ------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "stats" not in st.session_state:
    st.session_state.stats = None


# ------------------------
# Hero — a constellation mark, hand-built, with a gentle twinkle
# ------------------------

st.markdown("""
<p class="sph-kicker">Codebase intelligence, charted like a sky</p>
<div class="sph-hero">
    <div>
        <p class="sph-title">Sapphire</p>
        <p class="sph-desc">
            Upload a repository and <b>we chart it</b> — every file
            plotted and embedded locally — then open a channel so you
            can ask mission control anything, answered by Gemini 2.5 Flash.
        </p>
    </div>
    <svg class="sph-mark" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <g stroke="#8B6CFF" stroke-width="1" opacity="0.55">
            <line x1="24" y1="88" x2="52" y2="40"/>
            <line x1="52" y1="40" x2="88" y2="30"/>
            <line x1="52" y1="40" x2="70" y2="82"/>
            <line x1="88" y1="30" x2="70" y2="82"/>
            <line x1="24" y1="88" x2="70" y2="82"/>
        </g>
        <circle class="twinkle" cx="24" cy="88" r="3.2" fill="#A78BFF"/>
        <circle class="twinkle d2" cx="52" cy="40" r="4" fill="#F2C568"/>
        <circle class="twinkle d3" cx="88" cy="30" r="2.6" fill="#A78BFF"/>
        <circle class="twinkle" cx="70" cy="82" r="3.4" fill="#A78BFF"/>
        <circle class="twinkle d2" cx="52" cy="40" r="9" fill="#F2C568" opacity="0.18"/>
    </svg>
</div>
<hr class="sph-divider">
""", unsafe_allow_html=True)


# ------------------------
# Step 01 — Upload
# ------------------------

rail_col, content_col = st.columns([1, 11])

with rail_col:
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center;">
        <div class="sph-step-marker">01</div>
        <div class="sph-rail-line"></div>
    </div>
    """, unsafe_allow_html=True)

with content_col:
    st.markdown("""
    <p class="sph-step-label">Uncharted</p>
    <p class="sph-step-title">Upload a repository</p>
    <p class="sph-step-copy">A zipped codebase. We'll chart it into indexed points before you ask anything.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a ZIP repository",
        type=["zip"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:

        if st.button("Chart repository"):

            with st.spinner("Plotting the chart…"):

                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/zip",
                        )
                    },
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.indexed = True
                st.session_state.stats = data

                st.success("Repository charted.")

            else:

                st.error("Charting failed.")

                try:
                    st.json(response.json())
                except Exception:
                    st.text(response.text)

    if st.session_state.stats:
        st.markdown(f"""
        <div class="sph-readout">
            <div class="sph-readout-cell">
                <div class="n">{st.session_state.stats["files"]}</div>
                <div class="l">Files read</div>
            </div>
            <div class="sph-readout-cell">
                <div class="n">{st.session_state.stats["chunks"]}</div>
                <div class="l">Points charted</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ------------------------
# Step 02 — Chat
# ------------------------

if st.session_state.indexed:

    st.markdown('<div style="height:1.8rem;"></div>', unsafe_allow_html=True)

    rail_col2, content_col2 = st.columns([1, 11])

    with rail_col2:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center;">
            <div class="sph-step-marker">02</div>
        </div>
        """, unsafe_allow_html=True)

    with content_col2:
        st.markdown("""
        <p class="sph-step-label">Channel open</p>
        <p class="sph-step-title">Ask mission control</p>
        <p class="sph-step-copy">Every answer is read off the chart above — nothing outside the map.</p>
        """, unsafe_allow_html=True)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask anything about the repository…")

        if question:

            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):

                placeholder = st.empty()

                with st.spinner("Receiving signal…"):

                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={"message": question},
                    )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    placeholder.markdown(answer)

                    st.session_state.messages.append({"role": "assistant", "content": answer})

                else:

                    placeholder.error("Backend error.")

                    try:
                        st.json(response.json())
                    except Exception:
                        st.text(response.text)

else:
    st.markdown('<div style="height:1.8rem;"></div>', unsafe_allow_html=True)
    st.info("Chart a repository above to open a channel.")