import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from tools import all_tools

load_dotenv()

SYSTEM_PROMPT = (
    "You are an autonomous AI agent with access to tools. "
    "Solve the user's request step-by-step. "
    "Use python_calculator for any arithmetic. "
    "Use web_search for current events or facts you don't know. "
    "Use local_file_reader to read project files. "
    "Only use a tool when needed. Verify before answering."
)

def build_agent() -> AgentExecutor:
    if not os.getenv("GOOGLE_API_KEY"):
        sys.exit(
            "Error: GOOGLE_API_KEY missing. "
            "Copy .env.example to .env and paste your Gemini key from "
            "https://aistudio.google.com/apikey"
        )

    # Gemini via LangChain — same agent interface, different provider
    llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, all_tools, prompt)

    # verbose=True prints Thought → Action → Observation
    return AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=True,
        max_iterations=8,
    )

def main():
    agent = build_agent()
    print("\n🤖 Gemini Autonomous Agent Ready. Type 'exit' to quit.\n")

    while True:
        try:
            user = input("You: ").strip()
            if user.lower() in {"exit", "quit"}:
                break
            if not user:
                continue

            result = agent.invoke({"input": user})
            print(f"\n✅ Final Answer: {result['output']}\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        except Exception as e:
            print(f"⚠️  Agent error: {e}\n")

if __name__ == "__main__":
    main()