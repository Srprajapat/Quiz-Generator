import streamlit as st
import json
import os
from groq import Groq
from dotenv import load_dotenv
import tempfile
import time
import logging
import PyPDF2
from docx import Document

# Load environment variables and initialize client
load_dotenv()
# Try Streamlit secrets first, fall back to environment variable
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        logging.warning("Using GROQ_API_KEY from environment variable (st.secrets not found).")
    else:
        logging.warning("No GROQ_API_KEY provided; please set in secrets.toml or environment.")

# ensure we have a key
if not groq_api_key:
    st.error("API key missing. Add GROQ_API_KEY to .streamlit/secrets.toml or set environment variable.")
    st.stop()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Initialize Groq Client ---
try:
    if groq_api_key:
        client = Groq(api_key=groq_api_key)
        logging.info("Groq client initialized successfully.")
    else:
        st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
        logging.error("Groq API key not found.")
        st.stop()
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    logging.error(f"Error initializing Groq client: {e}")
    st.stop()

# --- Functions using the 'client' object ---
def attach_file(uploaded_file):
    st.write(f"Processing file: {uploaded_file.name}")
    logging.info(f"Processing file: {uploaded_file.name}")
    try:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension == '.pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_extension == '.docx':
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file_extension == '.txt':
            text = uploaded_file.read().decode('utf-8')
        else:
            st.error("Unsupported file type. Please upload PDF, DOCX, or TXT.")
            logging.error(f"Unsupported file type: {file_extension}")
            return None
        
        st.write(f"File processed successfully: {uploaded_file.name}")
        logging.info(f"File processed successfully: {uploaded_file.name}")
        return text
    except Exception as e:
        st.error(f"Error processing file {uploaded_file.name}: {e}")
        logging.error(f"Error processing file {uploaded_file.name}: {e}")
        return None

def fetch_questions(file_text, num_questions, difficulty):

    RESPONSE_JSON_SCHEMA = {
        "type": "object",
        "properties": {
            "mcqs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "mcq": {"type": "string"},
                        "options": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "string"},
                                "b": {"type": "string"},
                                "c": {"type": "string"},
                                "d": {"type": "string"},
                            },
                            "required": ["a", "b", "c", "d"]
                        },
                        "correct": {"type": "string"}
                    },
                    "required": ["mcq", "options", "correct"]
                }
            }
        },
        "required": ["mcqs"]
    }

    prompt = f"""
Generate {num_questions} MCQ questions from the content below.

Difficulty: {difficulty}

Rules:
- Questions must come directly from the content
- Do not repeat questions
- "correct" must contain the FULL text of the correct option
- Do not include explanations

Content:
{file_text[:4000]}
"""

    logging.info(f"Generating {num_questions} questions")

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "mcq_generation",
                        "schema": RESPONSE_JSON_SCHEMA
                    }
                },
                max_tokens=2000
            )

            parsed = json.loads(response.choices[0].message.content)

            questions = parsed["mcqs"]

            # Validate answers
            valid_questions = []
            for q in questions:
                options = list(q["options"].values())
                if q["correct"] in options:
                    valid_questions.append(q)

            if len(valid_questions) == len(questions):
                logging.info("Questions generated successfully")
                return valid_questions
            else:
                logging.warning("Invalid answers detected, retrying...")
                continue

        except Exception as e:

            error_message = str(e).lower()

            if "rate limit" in error_message or "429" in error_message:

                if attempt < max_retries - 1:
                    wait = (2 ** attempt) * 5
                    st.warning(f"Rate limit hit. Retrying in {wait}s")
                    time.sleep(wait)
                    continue
                else:
                    st.error("Rate limit exceeded.")
                    return None

            logging.error(e)
            st.error(f"Generation failed: {e}")
            return None

# --- Streamlit UI (This part remains the same as the previous correct answer) ---
st.title("📄 Quiz Generator from a Document")
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)
st.write("Upload a document (PDF, DOCX, TXT) or enter text/topics below and I'll generate a quiz for you.")

# Initialize session state variables
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

with st.sidebar:
    st.header("Quiz Settings")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=100, value=3, step=1)
    difficulty = st.radio("Difficulty Level:", ("Easy", "Medium", "Hard"))
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    user_text = st.text_area("Or enter text/topics manually (ignored if file provided):", height=100)

    if st.button("Generate Quiz"):
        # prioritize file if present, otherwise use manual text
        if uploaded_file:
            with st.spinner("Processing file and generating questions..."):
                file_text = attach_file(uploaded_file)
                if file_text:
                    st.session_state.questions = fetch_questions(file_text, num_questions, difficulty)
                    st.session_state.current_question_index = 0
                    st.session_state.score = 0
                    logging.info(f"Quiz generated with {len(st.session_state.questions) if st.session_state.questions else 0} questions.")
                    st.rerun()
        elif user_text and user_text.strip():
            with st.spinner("Generating questions from provided text..."):
                st.session_state.questions = fetch_questions(user_text, num_questions, difficulty)
                st.session_state.current_question_index = 0
                st.session_state.score = 0
                logging.info(f"Quiz generated from text with {len(st.session_state.questions) if st.session_state.questions else 0} questions.")
                st.rerun()
        else:
            st.error("Please upload a file or enter some text first.")
            logging.warning("Quiz generation attempted without file or text.")

# Display the quiz if questions are generated
if st.session_state.questions:
    st.header(f"Score: {st.session_state.score} / {len(st.session_state.questions)}")
    
    if st.session_state.current_question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.current_question_index]
        
        st.markdown(f"**Question {st.session_state.current_question_index + 1}:** {current_question.get('mcq')}")
        
        options_list = list(current_question.get("options", {}).values())
        correct_answer = current_question.get("correct")
        
        with st.form(key=f"question_form_{st.session_state.current_question_index}"):
            user_answer = st.radio("Select your answer:", options_list, index=None)
            submitted = st.form_submit_button("Submit Answer")

            if submitted:
                if user_answer is None:
                    st.warning("Please select an answer before submitting.")
                else:
                    if user_answer == correct_answer:
                        st.session_state.score += 1
                        st.success("Correct! 🎉")
                        logging.info(f"Question {st.session_state.current_question_index + 1}: Correct answer.")
                    else:
                        st.error(f"Incorrect. ❌ The correct answer was: **{correct_answer}**.")
                        logging.info(f"Question {st.session_state.current_question_index + 1}: Incorrect answer. Correct: {correct_answer}")
                    
                    time.sleep(1.5)
                    st.session_state.current_question_index += 1
                    st.rerun()
    else:
        st.header("Quiz Complete! 🥳")
        st.markdown(f"### Your Final Score: **{st.session_state.score} / {len(st.session_state.questions)}**")
        st.balloons()
        logging.info(f"Quiz completed. Final score: {st.session_state.score} / {len(st.session_state.questions)}")
        if st.button("Create Another Quiz"):
            st.session_state.questions = None

            st.rerun()

# Spacer to push footer down
st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p><strong>Made by srprajapat with ❤️</strong></p>
    <p>© 2025 srprajapat. All rights reserved.</p>
    <div>
        <a href="https://github.com/Srprajapat/Quiz-Generator" target="_blank" style="margin: 0 15px; color: #333;">
            <i class="fab fa-github fa-2x"></i>
        </a>
        <a href="https://twitter.com/s_r_prajapat" target="_blank" style="margin: 0 15px; color: #1DA1F2;">
            <i class="fab fa-twitter fa-2x"></i>
        </a>
        <a href="https://www.linkedin.com/in/seetaram-prajapat/" target="_blank" style="margin: 0 15px; color: #0077B5;">
            <i class="fab fa-linkedin fa-2x"></i>
        </a>
        <a href="https://instagram.com/s_r_prajapat" target="_blank" style="margin: 0 15px; color: #E4405F;">
            <i class="fab fa-instagram fa-2x"></i>
        </a>
        <a href="https://srprajapat.onrender.com" target="_blank" style="margin: 0 15px; color: #FF5722;">
            <i class="fas fa-globe fa-2x"></i>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)