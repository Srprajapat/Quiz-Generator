-----

# AI-Powered Quiz Generator 🧠✨

This project is a web application built with **Streamlit** that leverages the **Groq API** to automatically generate multiple-choice quizzes from uploaded documents. Simply provide a PDF, DOCX, or TXT file, and the application will create an interactive quiz based on its content.

-----

## Features 🚀

  * **Generate from Documents**: Create quizzes directly from your study materials, reports, or articles.
  * **Multiple File Formats**: Supports **PDF**, **DOCX**, and **TXT** files.
  * **Customizable Quizzes**: Specify the desired **number of questions** (1-10) and **difficulty level** (Easy, Medium, Hard).
  * **Interactive Interface**: A user-friendly quiz experience with immediate feedback on your answers.
  * **Scoring System**: Tracks your score in real-time and displays a final result upon completion.
  * **Powered by Groq**: Utilizes Groq's fast Llama models for efficient quiz generation.

-----

## Technology Stack 🛠️

  * **Framework**: Streamlit
  * **Language**: Python
  * **AI Model**: Groq API (llama-3.1-8b-instant)
  * **Core Libraries**: `groq`, `PyPDF2`, `python-docx`, `streamlit`

-----

## Setup and Installation

Follow these steps to get the Quiz Generator running on your local machine.

### 1\. Prerequisites

  * Python 3.8 or newer
  * Git

### 2\. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/Srprajapat/Quiz-Generator
cd quiz-generator
```

### 3\. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

  * **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  * **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 4\. Install Dependencies

The `requirements.txt` file is already included in the repository. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 5\. Set Up Your API Key 🔑

You need a Groq API key to use the Llama model.

1.  Sign up and generate an API key from [Groq Console](https://console.groq.com/).
2.  For local development, create a file named `secrets.toml` in the root directory (add it to `.gitignore`).
3.  Add your API key to the `secrets.toml` file as shown below:
    ```
    GROQ_API_KEY = "YOUR_API_KEY_HERE"
    ```
4.  For production (e.g., Streamlit Cloud), add the key in your app's secrets settings instead.

-----

## How to Run the Application ▶️

With your environment activated and the `secrets.toml` file in place, run the following command in your terminal:

```bash
streamlit run main.py
```

This will start the Streamlit server, and the application will open in a new tab in your web browser.

-----

## File Structure 📂

The project is structured as follows:

```
quiz-generator/
├── .env              # Optional: Stores API key for local dev (not committed to Git)
├── secrets.toml      # Stores your API key for local development (not committed to Git)
├── main.py           # The main Streamlit application script
├── requirements.txt  # Lists the Python dependencies
└── README.md         # This file
```

-----

## Contributing 🤝

Contributions are welcome\! If you have suggestions for improvements or want to add new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a new Pull Request.

-----

## Author
Seetaram Prajapat - [GitHub Profile](https://github.com/Srprajapat)

## Contact

For any questions or suggestions, reach out to me at [**seetaram.22jics083@jietjodhpur.ac.in**](mailto\:seetaram.22jics083@jietjodhpur.ac.in) or connect on [LinkedIn](https://www.linkedin.com/in/seetaram-prajapat).

## License 📜

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
