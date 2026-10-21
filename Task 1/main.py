from pathlib import Path

from app.schemas import Invoice, Resume
from app.extractor import extract_structured_data


def load_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    # ---------------- Invoice ----------------
    print("=" * 50)
    print("📄 INVOICE EXTRACTION")
    print("=" * 50)

    invoice_text = load_text("examples/invoice_sample.txt")
    try:
        invoice: Invoice = extract_structured_data(invoice_text, Invoice)
        print("✅ Validated Invoice:")
        print(invoice.model_dump_json(indent=2))
    except Exception as e:
        print(f"❌ Invoice extraction failed: {e}")

    # ---------------- Resume ----------------
    print("\n" + "=" * 50)
    print("📄 RESUME EXTRACTION")
    print("=" * 50)

    resume_text = load_text("examples/resume_sample.txt")
    try:
        resume: Resume = extract_structured_data(resume_text, Resume)
        print("✅ Validated Resume:")
        print(resume.model_dump_json(indent=2))
    except Exception as e:
        print(f"❌ Resume extraction failed: {e}")


if __name__ == "__main__":
    main()