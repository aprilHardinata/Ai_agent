# AI Agent (Backend) 🤖

This repository contains the **Backend** and **AI Agent** service that handles data processing and Artificial Intelligence requests for the AI Food Scanner mobile application. It is built using Python.

This backend is part of a decoupled system. For the mobile application (Frontend), please visit the following repository:
🔗 **Frontend Repository:** [AI Food Scanner (Flutter)](https://github.com/aprilHardinata/AI_Food_Scanner)

---

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Package Manager:** [uv](https://docs.astral.sh/uv/) (Fast and modern Python package installer)

## ⚙️ Setup & Installation

Follow the steps below to run the backend server locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/aprilHardinata/Ai_agent.git
   cd Ai_agent
   ```

2. **Install Dependencies:**
   Since this project uses `uv`, run the following command to install all dependencies automatically:
   ```bash
   uv sync
   ```

3. **Environment Configuration (`.env`):**
   Ensure you have a `.env` file in the root directory containing the required API Keys or secrets.
   *Example `.env` content:*
   ```env
   API_KEY=your_api_key_here
   ```

## 🚀 Running the Server

Once the dependencies are installed and the `.env` file is ready, start the main server using:

```bash
uv run python main.py
```
*(Or simply `python main.py` if your virtual environment is already activated)*

The server will start and listen for incoming requests from the frontend application. Make sure to keep this server running while testing the mobile app.
