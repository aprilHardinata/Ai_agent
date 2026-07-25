from google import genai
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI 
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from tools import hitung_kebutuhan_nutrisi

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def main():
    model = ChatGoogleGenerativeAI(model="models/gemini-3.1-flash-lite-preview", temperature=0)

    tools = [hitung_kebutuhan_nutrisi]
    system_prompt = "Kamu adalah asisten AI ahli gizi. Jawab pertanyaan seputar makanan dan kalori dengan pengetahuanmu sendiri yang luas. Jangan menolak menjawab hanya karena tidak ada tool-nya."
    agent_executor = create_react_agent(model, tools, prompt=system_prompt)

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