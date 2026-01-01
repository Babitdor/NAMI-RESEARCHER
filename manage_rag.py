"""
RAG Knowledge Base Management Utility

Usage:
    python manage_rag.py list              # List all ingested reports
    python manage_rag.py verify "topic"    # Verify a report was ingested
    python manage_rag.py ingest "file.md"  # Manually ingest a report
    python manage_rag.py search "query"    # Search the knowledge base
"""

import sys
import os
from dotenv import load_dotenv
from src.rag.rag_ingestion import RAGIngestion
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()


def list_reports():
    """List all reports in the knowledge base."""
    print("\n📚 Reports in Knowledge Base:")
    print("=" * 70)

    try:
        rag = RAGIngestion()
        reports = rag.list_ingested_reports()

        if not reports:
            print("No reports found in knowledge base.")
            print(
                "\nTip: Run research queries to automatically populate the knowledge base."
            )
            return

        for i, report in enumerate(reports, 1):
            print(f"\n{i}. {report['topic']}")
            print(f"   Created: {report.get('created_at', 'Unknown')}")
            print(f"   Chunks: {report.get('chunks', 'Unknown')}")

        print(f"\n{'=' * 70}")
        print(f"Total reports: {len(reports)}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nEnsure RAG_DIR is set in your .env file")


def verify_report(topic: str):
    """Verify a report exists in the knowledge base."""
    print(f"\n🔍 Verifying report: '{topic}'")
    print("=" * 70)

    try:
        rag = RAGIngestion()
        result = rag.verify_ingestion(topic)

        if result["found"]:
            print(f"✅ Report found!")
            print(f"   Chunks indexed: {result['chunks_found']}")
            print(f"   Total results: {result['total_results']}")
            print(f"\n   Sample content:")
            print(f"   {result.get('sample_content', 'N/A')[:200]}...")
        else:
            print(f"❌ Report not found in knowledge base")
            if "error" in result:
                print(f"   Error: {result['error']}")

    except Exception as e:
        print(f"❌ Error: {e}")


def ingest_file(filepath: str):
    """Manually ingest a markdown file."""
    print(f"\n📝 Ingesting file: {filepath}")
    print("=" * 70)

    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    try:
        # Read file
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract topic from filename or first heading
        topic = os.path.basename(filepath).replace(".md", "").replace("_", " ")

        # Check if there's a title in the content
        if content.startswith("# "):
            first_line = content.split("\n")[0]
            topic = first_line.replace("# ", "").strip()

        # Ingest
        rag = RAGIngestion()
        result = rag.add_report(
            report_content=content,
            topic=topic,
            metadata={"source_file": filepath, "manual_ingestion": True},
        )

        if result["success"]:
            print(f"✅ Successfully ingested!")
            print(f"   Topic: {topic}")
            print(f"   Chunks: {result['chunks_added']}")
        else:
            print(f"❌ Ingestion failed: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {e}")


def search_rag(query: str, k: int = 5):
    """Search the RAG knowledge base."""
    print(f"\n🔍 Searching for: '{query}'")
    print("=" * 70)

    try:
        rag_dir = os.getenv("RAG_DIR")
        if not rag_dir:
            print("❌ RAG_DIR not configured in .env")
            return

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )

        vectorstore = Chroma(
            persist_directory=rag_dir,
            embedding_function=embeddings,
            collection_name="research_reports",
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        docs = retriever.invoke(query)

        if not docs:
            print("No results found.")
            return

        print(f"\nFound {len(docs)} results:\n")

        for i, doc in enumerate(docs, 1):
            topic = doc.metadata.get("topic", "Unknown")
            created = doc.metadata.get("created_at", "Unknown")
            chunk_id = doc.metadata.get("chunk_id", "?")

            print(f"{i}. {topic} (Chunk {chunk_id})")
            print(f"   Created: {created}")
            print(f"   Content: {doc.page_content[:150]}...")
            print()

    except Exception as e:
        print(f"❌ Error: {e}")


def show_help():
    """Show usage help."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        list_reports()

    elif command == "verify":
        if len(sys.argv) < 3:
            print('Usage: python manage_rag.py verify "topic"')
            return
        verify_report(sys.argv[2])

    elif command == "ingest":
        if len(sys.argv) < 3:
            print('Usage: python manage_rag.py ingest "file.md"')
            return
        ingest_file(sys.argv[2])

    elif command == "search":
        if len(sys.argv) < 3:
            print('Usage: python manage_rag.py search "query"')
            return
        k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        search_rag(sys.argv[2], k)

    elif command in ["help", "-h", "--help"]:
        show_help()

    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
