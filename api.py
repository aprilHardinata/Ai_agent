import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools import hitung_kalori_makanan, hitung_kebutuhan_nutrisi
load_dotenv()

# --- 1. SETUP AGENT ---
model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature=0)
tools = [hitung_kalori_makanan,hitung_kebutuhan_nutrisi]
agent_executor = create_react_agent(model, tools)

# --- 2. SETUP FASTAPI ---
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    # Kirim input user ke agent
    try:
        response = agent_executor.invoke({"messages": [("user", request.message)]})
        
        # Ambil pesan terakhir dari AI
        last_message = response["messages"][-1]
        content = last_message.content
        
        # Logic agar output bersih (mengatasi format list of dict gemini 2.x)
        if isinstance(content, list):
            full_text = "".join([part['text'] for part in content if 'text' in part])
        elif isinstance(content,str):
            full_text = content
        else:
            full_text = str(content)

        return {"reply": full_text}
    except Exception as e:
        if "429" in str(e):
            return {"reply": f"Qouta habis :( ): {str(e)}"}
        return {"reply": f"Terjadi kesalahan sistem: {str(e)}"}
    

# uvicorn api:app --host 0.0.0.0 --port 8000 --reload untuk menjalankan server uvicorn
# Untuk testing di browser: http://127.0.0.1:8000/docs