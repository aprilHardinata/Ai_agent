import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import hitung_kalori_makanan, hitung_kebutuhan_nutrisi
load_dotenv()

model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature=0)
tools = [hitung_kalori_makanan, hitung_kebutuhan_nutrisi]
memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_thread"
    image_base64: str | None = None

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        if request.image_base64:
            content = [
                {"type": "text", "text": request.message},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{request.image_base64}"}}
            ]
        else:
            content = request.message

        response = agent_executor.invoke(
            {"messages": [("user", content)]},
            config={"configurable": {"thread_id": request.thread_id}}
        )
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
            return {"reply": f"Quota habis: {str(e)}"}
        return {"reply": f"Terjadi kesalahan sistem: {str(e)}"}