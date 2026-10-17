# BrandVoice AI – AI-Powered Tweet Generator

BrandVoice AI is a web application that generates on-brand social media tweets using Artificial Intelligence. It helps users create engaging and relevant Twitter/X content based on their brand details, target audience, campaign objectives, and preferred tone.

## 🌐 Project Links

* **Live Application:** https://brandvoice-ai-r8ow.onrender.com/
* **GitHub Repository:** https://github.com/Priyankamaurya-coder/BrandVoice_AI

## 🎯 Project Objectives

* Generate 10 brand-specific social media tweets.
* Infer a suitable brand voice from user-provided information.
* Create content aligned with campaign objectives and target audiences.
* Help users save time when planning social media content.
* Provide an easy-to-use interface for generating and copying tweets.

## ✨ Features

* Brand name and industry inputs.
* Campaign objective selection.
* Product and service details.
* Target audience specification.
* Custom or AI-inferred brand tone.
* AI-assisted brand voice insights.
* Generation of 10 tweets with different purposes.
* Copy buttons for individual tweets.
* Demo or fallback responses when AI generation is unavailable.

## 🛠️ Technologies Used

* **Python** – Core programming language
* **Django** – Web application framework
* **HTML and CSS** – User interface
* **JavaScript** – Interactive functionality
* **Google Gemini API** – AI-powered content generation
* **SQLite** – Database
* **Gunicorn** – Production application server
* **Render** – Deployment and hosting
* **Git and GitHub** – Version control and source code management

## ⚙️ How It Works

1. The user opens the BrandVoice AI application.
2. The user enters the brand name, industry, campaign objective, products or services, and target audience.
3. The user selects a preferred tone or allows the application to infer one.
4. The application prepares a prompt using the submitted information.
5. The Gemini API generates brand voice insights and relevant tweet content when the API is available.
6. The application displays 10 generated tweets with their intended purposes.
7. The user can copy individual tweets for further editing or use.

**Note:** Brand voice insights are inferred from the information supplied through the form. They should not be interpreted as independently verified analysis of the brand's social media accounts.

## 📂 Project Structure

```text
BrandVoice_AI/
├── config/
├── generator/
│   └── templates/
│       └── generator/
│           ├── home.html
│           └── results.html
├── Documentation/
│   └── BrandVoice_AI_Approach_Document.pdf
├── venv/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
└── test_gemini.py
```

*The structure above is illustrative. Keep the filenames consistent with your actual project.*

## 🚀 Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Priyankamaurya-coder/BrandVoice_AI.git
cd BrandVoice_AI
```

### 2. Create and activate a virtual environment

On Windows Command Prompt:

```cmd
py -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root and add your API key using the environment variable name expected by your application.

```text
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own valid API key. Never commit your actual API key to GitHub.

### 5. Apply database migrations

```bash
py manage.py migrate
```

### 6. Start the development server

```bash
py manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## 🧪 Testing

The application has been tested with example brands, including Nike and Amazon, to check tweet generation using different brand details and campaign objectives.

Testing should cover:

* Form input validation.
* Brand voice insight generation.
* Generation of 10 tweets.
* Copy-to-clipboard functionality.
* Behavior when the AI API is unavailable.
* Successful access to the deployed application.

## 🔐 Security

* API keys are stored in environment variables.
* The `.env` file should be excluded from version control.
* The virtual environment should not be uploaded to GitHub.
* Local database files should be excluded unless specifically required.

## 🔮 Future Enhancements

* Analyze actual brand social media posts to learn writing style.
* Integrate social media platform APIs.
* Add downloadable tweet reports.
* Support multiple languages.
* Save and manage previously generated campaigns.
* Add additional AI models and improved error handling.

## 👩‍💻 Author

**Priyanka Maurya**

B.E. Data Science | AI and Machine Learning | Python Development

## 📄 Documentation

The project's approach document describes its objectives, workflow, technologies, AI-based content generation, testing, and limitations. Refer to the `Documentation` folder for the report.

---

*BrandVoice AI – Create consistent, audience-focused social media content with AI.*
