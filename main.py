import streamlit as st
import json
import os
from google import genai
from dotenv import load_dotenv
import tempfile
import time

# Load environment variables and initialize client
load_dotenv()
google_api_key = st.secrets["GOOGLE_API_KEY"]

# --- FIX 1: Reverted API Initialization to your original working method ---
try:
    if google_api_key:
        client = genai.Client(api_key=google_api_key)
    else:
        st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
        st.stop()
except Exception as e:
    st.error(f"Error initializing Google GenAI client: {e}")
    st.stop()

# --- Functions using the 'client' object ---
def attach_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name
    
    st.write(f"Attempting to attach file: {uploaded_file.name}")
    try:
        # --- FIX 2: Reverted File Upload to your original working method ---
        uploaded_file_uri = client.files.upload(file=temp_file_path)
        st.write(f"Uploaded file for attachment (URI: {uploaded_file_uri.uri}): {uploaded_file.name}")
        return uploaded_file_uri
    except Exception as e:
        st.error(f"Error processing file {uploaded_file.name}: {e}")
        return None
    finally:
        os.remove(temp_file_path)

def fetch_questions(uploaded_file_uri, num_questions, difficulty):
    RESPONSE_JSON_SCHEMA = {
        "mcqs": [
            {
                "mcq": "multiple choice question",
                "options": {
                    "a": "choice 1",
                    "b": "choice 2",
                    "c": "choice 3",
                    "d": "choice 4",
                },
                "correct": "The full text of the correct choice",
            }
        ]
    }
    prompt_template = f"""
    You are an expert in generating MCQ quizzes based on provided content.
    Given the content from the attached file, create a quiz of {num_questions} multiple choice questions.
    The difficulty of the questions should be {difficulty}.
    Ensure the questions are not repeated and are directly based on the provided text.
    Your response MUST be a valid JSON object. Format your response exactly like the JSON schema below.
    The "correct" field must contain the full text of the correct option, which must also be one of the values in the "options" dictionary.

    JSON Schema:
    ```json
    {json.dumps(RESPONSE_JSON_SCHEMA, indent=4)}
    ```
    """
    
    content_parts = [prompt_template, uploaded_file_uri]
    
    try:
        # --- FIX 3: Reverted Content Generation to your original working method ---
        response = client.models.generate_content(
            model="gemini-2.0-flash",  
            contents=content_parts
        )
        if response.text:
            cleaned_json_string = response.text.strip()
            if cleaned_json_string.startswith("```json"):
                cleaned_json_string = cleaned_json_string[7:]
            if cleaned_json_string.endswith("```"):
                cleaned_json_string = cleaned_json_string[:-3]
            
            cleaned_json_string = cleaned_json_string.strip()

            try:
                parsed_response = json.loads(cleaned_json_string).get("mcqs", [])
                return parsed_response
            except json.JSONDecodeError as json_err:
                st.error(f"Error parsing JSON response from the model: {json_err}")
                st.code(response.text, language='text')
                return None
        else:
            st.warning("Model did not generate any text.")
            if response.prompt_feedback:
                st.write(f"Prompt feedback: {response.prompt_feedback}")
            return None
    except Exception as e:
        st.error(f"An error occurred during content generation: {e}")
        return None

# --- Streamlit UI (This part remains the same as the previous correct answer) ---
st.title("📄 Quiz Generator from a Document")
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 10px;
    text-align: center;
    z-index: 1000;
    border-top: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)
st.write("Upload a document (PDF, DOCX, TXT) and I'll generate a quiz for you.")

# Initialize session state variables
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

with st.sidebar:
    st.header("Quiz Settings")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=3, step=1)
    difficulty = st.radio("Difficulty Level:", ("Easy", "Medium", "Hard"))
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

    if st.button("Generate Quiz"):
        if uploaded_file:
            with st.spinner("Uploading file and generating questions..."):
                attached_file_uri = attach_file(uploaded_file)
                if attached_file_uri:
                    st.session_state.questions = fetch_questions(attached_file_uri, num_questions, difficulty)
                    st.session_state.current_question_index = 0
                    st.session_state.score = 0
                    st.rerun()
        else:
            st.error("Please upload a file first.")

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
                    else:
                        st.error(f"Incorrect. ❌ The correct answer was: **{correct_answer}**.")
                    
                    time.sleep(1.5)
                    st.session_state.current_question_index += 1
                    st.rerun()
    else:
        st.header("Quiz Complete! 🥳")
        st.markdown(f"### Your Final Score: **{st.session_state.score} / {len(st.session_state.questions)}**")
        st.balloons()
        if st.button("Create Another Quiz"):
            st.session_state.questions = None

            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
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