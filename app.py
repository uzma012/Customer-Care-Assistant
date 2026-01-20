
from assistant import ChatAssistant
from assistant.indexer import Indexer
import streamlit as st
from datetime import datetime
from io import BytesIO
from pathlib import Path
from ingestion import loader
from extraction import extractor
from generator import json_generator, pdf_generator
from dotenv import load_dotenv
load_dotenv()

def initialize():
    if "index_loaded" not in st.session_state:
        indexer = Indexer()
        indexer.build_index_from_json("output/intake_payload.json")
        st.session_state.index_loaded = True
        
json_file_path = Path("output/intake_payload.json")
pdf_file_path = Path("output/intake_summary.pdf")

st.set_page_config(page_title="Transcript Processor", layout="wide")
st.title("📄 Transcript Processor")

if "step" not in st.session_state:
    st.session_state.step = 1

# STEP 1 — Upload Page
if st.session_state.step == 1:
    st.header("Step 1: Upload or Paste Transcript")

    if json_file_path.is_file():
        if st.button("💬 Chat with AI Assistant"):
            st.session_state.step = 5
            st.rerun()
    
    uploaded_file = st.file_uploader("Upload transcript (TXT)", type=["txt"])
    pasted_text = st.text_area("Or paste transcript here", height=150)

    if uploaded_file:
        uploaded_bytes = uploaded_file.read()
        try:
            text = uploaded_bytes.decode("utf-8")
        except:
            text = uploaded_bytes.decode("latin-1")

        st.session_state["input_text"] = text
        st.success("File uploaded!")

    elif pasted_text.strip():
        st.session_state["input_text"] = pasted_text
        st.info("Text pasted.")

    if st.button("Next →", disabled="input_text" not in st.session_state):
        st.session_state.step = 2
        st.rerun()


# STEP 2 — Extract Text


elif st.session_state.step == 2:
    st.header("Step 2: Extract Text")

    st.subheader("Uploaded Text")
    st.text_area("Preview", st.session_state["input_text"], height=180)

    if st.button("Extract Text"):
        extracted = extractor.extract_text(st.session_state["input_text"])
        st.session_state["extracted_text"] = extracted
        st.success("Text extracted!")

    if "extracted_text" in st.session_state:
        st.subheader("Extracted Text")
        st.text_area("Extracted Content", st.session_state["extracted_text"], height=200)

        if st.button("Next →"):
            st.session_state.step = 3
            st.rerun()

    if st.button("← Back"):
        st.session_state.step = 1
        st.rerun()


# STEP 3 — Generate JSON + PDF

elif st.session_state.step == 3:
    st.header("Step 3: Generate JSON & PDF Summary")

    if st.button("Generate JSON"):
        json_data = json_generator.generate_json(st.session_state["extracted_text"])
        pdf_data = pdf_generator.text_to_pdf(str(json_data), "output/intake_summary.pdf")

        st.session_state["json_data"] = json_data
        st.session_state["pdf_data"] = pdf_data
        st.success("JSON & PDF generated!")

    if "json_data" in st.session_state:
        st.json(st.session_state["json_data"])

        if json_file_path.exists():
            st.download_button("Download JSON", json_file_path.read_bytes(), "intake_payload.json")

        if pdf_file_path.exists():
            st.download_button("Download PDF", pdf_file_path.read_bytes(), "intake_summary.pdf")

        if st.button("Next →"):
            st.session_state.step = 4
            st.rerun()

    if st.button("← Back"):
        st.session_state.step = 2
        st.rerun()


# STEP 4 — Final Page

elif st.session_state.step == 4:
    st.header("Step 4: Final Options")

    st.success("🎉 Process Completed Successfully!")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Regenerate JSON"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("📝 Re-Extract Text"):
            st.session_state.step = 2
            st.rerun()

    with col3:
        if st.button("💬 Chat with AI Assistant"):
            st.session_state.step = 5
            st.rerun()

    if st.button("← Back"):
        st.session_state.step = 3
        st.rerun()


# STEP 5 — Chat Page
    
elif st.session_state.step == 5:
    initialize()

    st.set_page_config(page_title="💬 Chat Assistant", layout="wide")


    if "assistant" not in st.session_state:
        st.session_state.assistant = ChatAssistant()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.header("💬 Chat with AI Assistant")

    chat_container = st.container()

    for msg in st.session_state.messages:
        st.markdown(f"**You [{msg['timestamp']}]:** {msg['user']}")
        st.markdown(f"**Bot [{msg['timestamp']}]:** {msg['bot']}")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here...")
        send_button = st.form_submit_button("Send")
        
        if send_button and user_input.strip():
            timestamp = datetime.now().strftime("%H:%M")
            
            answer, _, _ = st.session_state.assistant.ask(user_input)
            
            st.session_state.messages.append({
                "user": user_input,
                "bot": answer,
                "timestamp": timestamp
            })
            
            st.rerun()

    if st.button("← Back"):
        st.session_state.step = 1
        st.rerun()




