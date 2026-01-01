"""
RAG Ingestion Utility - Automatically add research reports to knowledge base
"""

import os
from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
import logging

logger = logging.getLogger(__name__)


class RAGIngestion:
    """Handles automatic ingestion of research reports into RAG knowledge base."""

    def __init__(self, rag_dir: str = None, collection_name: str = "research_reports"):  # type: ignore
        """Initialize RAG ingestion system.

        Args:
            rag_dir: Directory for vector store (uses RAG_DIR env if not provided)
            collection_name: Collection name for research reports
        """
        self.rag_dir = rag_dir or os.getenv("RAG_DIR")
        self.collection_name = collection_name

        if not self.rag_dir:
            raise ValueError(
                "RAG_DIR not configured. Set RAG_DIR environment variable or pass rag_dir parameter."
            )

        # Create directory if it doesn't exist
        os.makedirs(self.rag_dir, exist_ok=True)

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )

        logger.info(f"RAG ingestion initialized: {self.rag_dir}")

    def add_report(
        self,
        report_content: str,
        topic: str,
        metadata: dict = None,  # type: ignore
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> dict:
        """Add a research report to the RAG knowledge base.

        Args:
            report_content: The full research report text
            topic: Topic/title of the report
            metadata: Additional metadata to store
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            dict with ingestion results
        """
        # s = Spinner(f"Adding report to RAG: '{topic[:50]}...'", icon="📚 RAG |")
        # s.start()

        try:
            # Validate report content
            if not report_content or len(report_content.strip()) < 100:
                # s.stop(success=False)
                logger.warning(
                    f"Report too short for RAG ingestion: {len(report_content)} chars"
                )
                return {
                    "success": False,
                    "error": "Report content is too short or empty (minimum 100 characters required)",
                    "topic": topic,
                    "message": f"Skipped RAG ingestion: report too short ({len(report_content)} chars)",
                }

            # Prepare metadata
            doc_metadata = {
                "topic": topic,
                "source": "research_report",
                "created_at": datetime.now().isoformat(),
                "collection": self.collection_name,
            }

            if metadata:
                doc_metadata.update(metadata)

            # Split report into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
            )

            chunks = text_splitter.split_text(report_content)

            # Filter out empty chunks
            chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

            if not chunks:
                # s.stop(success=False)
                logger.warning(f"No valid chunks generated from report: '{topic}'")
                return {
                    "success": False,
                    "error": "No valid text chunks could be generated from report",
                    "topic": topic,
                    "message": "Report could not be split into valid chunks",
                }

            # Create documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = doc_metadata.copy()
                chunk_metadata["chunk_id"] = i  # type: ignore
                chunk_metadata["total_chunks"] = len(chunks)  # type: ignore

                documents.append(Document(page_content=chunk, metadata=chunk_metadata))

            # Load or create vector store
            vectorstore = Chroma(
                persist_directory=self.rag_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )

            # Add documents (auto-persists in newer versions)
            vectorstore.add_documents(documents)

            # s.stop(success=True)

            logger.info(
                f"Successfully added report to RAG: {len(chunks)} chunks from '{topic}'"
            )

            return {
                "success": True,
                "chunks_added": len(chunks),
                "topic": topic,
                "collection": self.collection_name,
                "message": f"Added {len(chunks)} chunks to knowledge base",
            }

        except Exception as e:
            # s.stop(success=False)
            logger.error(f"Failed to add report to RAG: {e}")

            return {
                "success": False,
                "error": str(e),
                "topic": topic,
                "message": f"Failed to add report: {str(e)}",
            }

    def add_multiple_reports(self, reports: list) -> dict:
        """Add multiple reports to RAG in batch.

        Args:
            reports: List of dicts with 'content', 'topic', and optional 'metadata'

        Returns:
            dict with batch ingestion results
        """
        results = {"successful": 0, "failed": 0, "details": []}

        for report in reports:
            result = self.add_report(
                report_content=report["content"],
                topic=report["topic"],
                metadata=report.get("metadata", {}),
            )

            if result["success"]:
                results["successful"] += 1
            else:
                results["failed"] += 1

            results["details"].append(result)

        logger.info(
            f"Batch ingestion complete: {results['successful']} successful, {results['failed']} failed"
        )

        return results

    def verify_ingestion(self, topic: str, query: str = None) -> dict:  # type: ignore
        """Verify that a report was successfully ingested.

        Args:
            topic: Topic to verify
            query: Optional query to test retrieval (uses topic if not provided)

        Returns:
            dict with verification results
        """
        try:
            vectorstore = Chroma(
                persist_directory=self.rag_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )

            # Search for documents with this topic
            search_query = query or topic
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            docs = retriever.invoke(search_query)

            # Filter for this topic
            topic_docs = [doc for doc in docs if doc.metadata.get("topic") == topic]

            return {
                "found": len(topic_docs) > 0,
                "chunks_found": len(topic_docs),
                "total_results": len(docs),
                "sample_content": (
                    topic_docs[0].page_content[:200] if topic_docs else None
                ),
            }

        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {"found": False, "error": str(e)}

    def list_ingested_reports(self) -> list:
        """List all ingested reports in the knowledge base.

        Returns:
            list of report topics with metadata
        """
        try:
            vectorstore = Chroma(
                persist_directory=self.rag_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )

            # Get all documents (sample)
            # Note: Chroma doesn't have a direct "list all" method
            # This retrieves a sample via broad query
            retriever = vectorstore.as_retriever(search_kwargs={"k": 100})
            docs = retriever.invoke("research")

            # Extract unique topics
            topics = {}
            for doc in docs:
                topic = doc.metadata.get("topic")
                if topic and topic not in topics:
                    topics[topic] = {
                        "topic": topic,
                        "created_at": doc.metadata.get("created_at"),
                        "chunks": doc.metadata.get("total_chunks", 1),
                    }

            return list(topics.values())

        except Exception as e:
            logger.error(f"Failed to list reports: {e}")
            return []


def auto_ingest_report(
    report_content: str,
    topic: str,
    state: dict = None,  # type: ignore
    rag_dir: str = None,  # type: ignore
) -> dict:
    """Convenience function to auto-ingest a report.

    Args:
        report_content: The research report content
        topic: Report topic
        state: Optional state dict to extract metadata
        rag_dir: Optional RAG directory (uses env if not provided)

    Returns:
        dict with ingestion results
    """
    try:
        ingestion = RAGIngestion(rag_dir=rag_dir)

        # Prepare metadata from state if available
        metadata = {}
        if state:
            metadata["quality_score"] = state.get("quality_score")
            metadata["confidence_scores"] = str(state.get("confidence_scores", {}))
            metadata["iteration_count"] = state.get("iteration_count", 0)
            metadata["refinement_count"] = state.get("refinement_count", 0)

        result = ingestion.add_report(report_content, topic, metadata)

        return result

    except Exception as e:
        logger.error(f"Auto-ingestion failed: {e}")
        return {"success": False, "error": str(e)}
