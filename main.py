from google import genai
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI 
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@tool
def hitung_kalori_makanan(nama_makanan: str, jumlah_porsi: int = 1) -> str:
    """
    Gunakan tool ini untuk mendapatkan informasi kalori makanan Indonesia secara akurat.
    Input: nama_makanan (string), jumlah_porsi (integer)
    """

    print("tools digunakan")
    # Database sederhana (nanti bisa kamu sambungkan ke API asli atau SQLite)
    data_kalori = {
        "nasi goreng": 250,
        "telur mata sapi": 90,
        "ayam goreng": 260,
        "nasi putih": 204,
        "sate ayam": 34, # per tusuk
    }
    
    makanan_key = nama_makanan.lower()
    if makanan_key in data_kalori:
        total = data_kalori[makanan_key] * jumlah_porsi
        return f"Total kalori untuk {jumlah_porsi} {nama_makanan} adalah {total} kkal."
    else:
        return f"Maaf, data kalori untuk {nama_makanan} tidak ditemukan di database saya."
    

def main():
    model = ChatGoogleGenerativeAI(model="models/gemini-3.1-flash-lite-preview", temperature=0)

    tools = [hitung_kalori_makanan]
    agent_executor = create_react_agent(model, tools)

    print("--- Asisten AI RPL (Gemini Mode) ---")
    print("Ketik 'keluar' untuk stop.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["keluar", "exit", "quit"]:
            break

        print("Assistant: ", end="", flush=True)
        
        # Stream response
        try:
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}
            ):
                if "agent" in chunk:
                    for message in chunk["agent"]["messages"]:
                        content = message.content
                        if isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and 'text' in item:
                                    print(item['text'], end="", flush=True)
                                elif isinstance(item, str):
                                    print(message.content, end="", flush=True)
                        elif isinstance(content, str):
                            print(item, end="", flush=True)

            print("\n")
        except Exception as e:
            print(f"\nWah, ada error nih: {e}")


if __name__ == "__main__":
    main()