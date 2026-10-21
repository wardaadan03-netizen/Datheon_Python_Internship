"""Interactive CLI for the RAG assistant."""
from src.qa_engine import QAEngine
from src.logger import get_logger

logger = get_logger("query")


def _print_response(response) -> None:
    print("\n" + "=" * 60)
    print("📖 Answer")
    print("=" * 60)
    print(response.answer)
    print("\n📎 Sources")
    print("-" * 60)
    for i, c in enumerate(response.citations, 1):
        print(f"  [{i}] {c.source_file}  —  page {c.page}")
        print(f"      \"{c.snippet}\"")
    print("=" * 60 + "\n")


def main() -> None:
    engine = QAEngine()
    print("\n💬 Document Q&A Assistant — type 'exit' to quit.\n")

    while True:
        try:
            q = input("❓ Question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            _print_response(engine.ask(q))
        except Exception as e:
            logger.error(f"Query failed: {e}")


if __name__ == "__main__":
    main()