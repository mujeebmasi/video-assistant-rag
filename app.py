import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from core.rag_engine import ask_question
from main import run_the_goated_pipeline

load_dotenv(override=True)

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #07111f 0%, #0b1728 55%, #f4f7fb 55%, #f4f7fb 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero {
            padding: 2rem 2rem 1.5rem 2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(12, 24, 44, 0.96), rgba(28, 50, 86, 0.92));
            color: white;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .hero h1 {
            margin-bottom: 0.35rem;
            font-size: 3rem;
            line-height: 1;
        }
        .hero p {
            margin: 0;
            opacity: 0.88;
            font-size: 1.02rem;
        }
        .panel {
            padding: 1.25rem 1.25rem 0.75rem 1.25rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
            margin-bottom: 1rem;
        }
        .metric-card {
            padding: 1rem;
            border-radius: 18px;
            background: linear-gradient(180deg, #ffffff, #f7fafc);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }
        .small-label {
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.75rem;
            color: #64748b;
            margin-bottom: 0.25rem;
        }
        .streamlit-expanderHeader {
            font-weight: 700;
        }
        div[data-testid="stChatInput"] textarea {
            border-radius: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>AI Meeting Assistant</h1>
        <p>Turn a video, audio file, or YouTube link into a transcript, summary, tasks, decisions, and a chat-ready RAG assistant.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "source_path" not in st.session_state:
    st.session_state.source_path = None

with st.sidebar:
    st.header("Input")
    source_type = st.radio(
        "Choose source type",
        ["YouTube URL", "Upload file", "Local file path"],
        index=0,
    )

    source_value = None
    temp_file_path = None

    if source_type == "YouTube URL":
        source_value = st.text_input(
            "Paste the YouTube link",
            placeholder="https://www.youtube.com/watch?v=...",
        )
    elif source_type == "Upload file":
        uploaded_file = st.file_uploader(
            "Upload an audio or video file",
            type=["mp3", "wav", "m4a", "mp4", "webm", "mov", "ogg", "flac"],
        )
        if uploaded_file is not None:
            suffix = Path(uploaded_file.name).suffix or ".wav"
            temp_dir = Path(tempfile.gettempdir()) / "ai_meeting_assistant"
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_file_path = temp_dir / uploaded_file.name
            with open(temp_file_path, "wb") as file_handle:
                file_handle.write(uploaded_file.getbuffer())
            source_value = str(temp_file_path)
            st.caption(f"Saved to: {temp_file_path}")
    else:
        source_value = st.text_input(
            "Local file path",
            placeholder=r"D:\path\to\meeting.mp4",
        )

    run_button = st.button("Run analysis", use_container_width=True)
    clear_button = st.button("Clear results", use_container_width=True)

    st.markdown("---")
    st.subheader("What you get")
    st.write("Transcript")
    st.write("Summary")
    st.write("Action items")
    st.write("Decisions")
    st.write("Questions")
    st.write("Chat with the transcript")

if clear_button:
    st.session_state.result = None
    st.session_state.messages = []
    st.session_state.source_path = None
    st.rerun()

if run_button:
    if not source_value:
        st.error("Add a YouTube link, upload a file, or provide a local path first.")
    else:
        with st.spinner("Processing source, transcribing, and building the RAG chain..."):
            try:
                st.session_state.result = run_the_goated_pipeline(source_value)
                st.session_state.source_path = source_value
                st.session_state.messages = []
                st.success("Analysis complete.")
            except Exception as exc:
                st.session_state.result = None
                st.error(f"Pipeline failed: {exc}")

result = st.session_state.result

if result:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Transcript Preview")
        st.write(result["transcript"][:4000])
    with col2:
        st.subheader("Quick Stats")
        st.markdown(
            '<div class="metric-card"><div class="small-label">Source</div><div>{}</div></div>'.format(
                "Uploaded file" if source_type == "Upload file" else source_type
            ),
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    metric_cols = st.columns(4)
    metric_cols[0].metric("Title", "Ready")
    metric_cols[1].metric("Summary", "Ready")
    metric_cols[2].metric("Tasks", "Ready")
    metric_cols[3].metric("RAG", "Ready")

    tab_summary, tab_tasks, tab_decisions, tab_questions = st.tabs(
        ["Summary", "Action Items", "Decisions", "Questions"]
    )

    with tab_summary:
        st.markdown("### Title")
        st.write(result["title"])
        st.markdown("### Summary")
        st.write(result["summary"])

    with tab_tasks:
        st.markdown("### Actionable Items")
        st.write(result["actionable_items"])

    with tab_decisions:
        st.markdown("### Decisions")
        st.write(result["decisions"])

    with tab_questions:
        st.markdown("### Questions")
        st.write(result["questions"])

    st.markdown("---")
    st.subheader("Chat with the meeting transcript")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_question = st.chat_input("Ask anything about the transcript")
    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(result["rag_chain"], user_question)
                st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Run an analysis to generate the transcript, summary, and chat assistant.")
