# Proompter

✨ **Proompter** is an advanced prompt refinement tool that leverages LLMs to help you craft, evaluate, and optimize prompts for AI systems. It features a modern Streamlit UI and a FastAPI backend for programmatic access.

---

## Features
- **Modern, stylish Streamlit UI** for interactive prompt refinement
- **Automated prompt evaluation and optimization** using LLMs
- **Lottie animation and custom CSS** for a beautiful user experience
- **FastAPI backend** for API access and integration

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/Proompter.git
cd Proompter
```

### 2. Create and Activate a Virtual Environment (optional but recommended)
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install streamlit-lottie  # For Lottie animation in the UI
```

---

## Usage

### A. Run the Streamlit App (Modern UI)
```bash
cd prompt-suite
streamlit run app.py
```
- Open the provided local URL in your browser to use the UI.

### B. Run the FastAPI Backend (API Access)
```bash
cd prompt-suite
uvicorn main:app --host 0.0.0.0 --port 2137
```
- Access the API docs at: [http://127.0.0.1:2137/docs](http://127.0.0.1:2137/docs)

#### Example API Request
```json
POST /refine_prompt
{
  "prompt": "what is antibiotics"
}
```

---

## Example

- Enter a prompt in the Streamlit UI and click **Generate ✨**
- The app will display a refined, optimized version of your prompt with a modern look.

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
[MIT](LICENSE) 