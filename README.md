### 01. Initialize UV package manager

```
uv init
uv venv
.venv\Scripts\activate
```

- Add requirements.txt file and install all the dependencies by running `uv add -r requirements.txt`

### 02. Create keys

- [Gemini API Key](https://aistudio.google.com/api-keys)
- [Groq API Key](https://console.groq.com/keys)
- [OpenAI API Key](https://platform.openai.com/api-keys)

### 03. Create .env file and add keys

```
OPENAI_API_KEY = "your_openai_api_key"
GROQ_API_KEY = "your_groq_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
```
