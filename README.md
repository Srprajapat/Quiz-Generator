-----

# AI-Powered Quiz Generator 🧠✨

This project is a web application built with **Streamlit** that leverages the **Google Gemini API** to automatically generate multiple-choice quizzes from uploaded documents. Simply provide a PDF, DOCX, or TXT file, and the application will create an interactive quiz based on its content.

-----

## Features 🚀

  * **Generate from Documents**: Create quizzes directly from your study materials, reports, or articles.
  * **Multiple File Formats**: Supports **PDF**, **DOCX**, and **TXT** files.
  * **Customizable Quizzes**: Specify the desired **number of questions** (1-10) and **difficulty level** (Easy, Medium, Hard).
  * **Interactive Interface**: A user-friendly quiz experience with immediate feedback on your answers.
  * **Scoring System**: Tracks your score in real-time and displays a final result upon completion.
  * **Powered by Gemini**: Utilizes Google's powerful generative AI to understand context and formulate relevant questions.

-----

## Technology Stack 🛠️

  * **Framework**: Streamlit
  * **Language**: Python
  * **AI Model**: Google Gemini API (`gemini-1.5-flash`)
  * **Core Libraries**: `google-generativeai`, `python-dotenv`

-----

## Setup and Installation

Follow these steps to get the Quiz Generator running on your local machine.

### 1\. Prerequisites

  * Python 3.8 or newer
  * Git

### 2\. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/your-username/quiz-generator.git
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

Create a `requirements.txt` file with the following content:

```txt
streamlit
google-generativeai
python-dotenv
```

Then, install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 5\. Set Up Your API Key 🔑

You need a Google API key to use the Gemini model.

1.  Generate an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  In the root directory of the project, create a file named `.env`.
3.  Add your API key to the `.env` file as shown below:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

-----

## How to Run the Application ▶️

With your environment activated and the `.env` file in place, run the following command in your terminal:

```bash
streamlit run app.py
```

This will start the Streamlit server, and the application will open in a new tab in your web browser.

-----

## File Structure 📂

The project is structured as follows:

```
quiz-generator/
├── .env              # Stores your API key (not committed to Git)
├── app.py            # The main Streamlit application script
└── requirements.txt  # Lists the Python dependencies
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
