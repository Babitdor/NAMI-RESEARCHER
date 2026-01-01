from langchain_tavily import TavilySearch
from typing_extensions import Optional
from langchain_core.tools import tool
import httpx
from markdownify import markdownify
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import language_tool_python
from langchain.tools import tool
import wikipedia
import logging
import arxiv
import os
import tempfile
import requests
from datetime import datetime
from typing import Dict, Any
from markdown_pdf import MarkdownPdf, Section
from src.rag.rag_ingestion import auto_ingest_report
from src.utils.markdown_render import fix_markdown_hierarchy
from dotenv import load_dotenv
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun


logging.getLogger("langchain").setLevel(logging.WARNING)
load_dotenv()


@tool
def save_report_and_ingest(
    topic: str, report: str, filename: str, state: Optional[Dict[str, Any]] = None
) -> str:
    """Save a research report to Markdown and PDF format, and automatically ingest it into the RAG knowledge base.

    This tool saves reports in multiple formats and makes them available for future research queries.

    Args:
        topic: The topic or title of the research report
        report: The full markdown content of the report to save
        filename: Base filename (without extension) for saving the report
        state: Optional state dictionary containing research context

    Returns:
        A status message indicating the success or failure of the save operation,
        including file paths and RAG ingestion results.

    Use this tool when:
    - A research report has been generated and needs to be saved
    - You want to make a report available for future research queries
    - You need both human-readable (PDF) and machine-readable (MD) formats
    """

    # Import dependencies

    # Validate report content
    if not report or len(report.strip()) < 100:
        logging.warning(f"Report is very short or empty ({len(report)} chars)")
        logging.info("This may indicate an issue with report generation.")
        if len(report.strip()) < 10:
            logging.info("Skipping save and RAG ingestion due to empty report.")
            return (
                "❌ Report is too short (< 10 chars). Skipping save and RAG ingestion."
            )

    # Create directories if they don't exist
    os.makedirs("reports", exist_ok=True)

    # Add timestamp to avoid overwriting files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_md = f"reports/{filename}.md"
    filename_pdf = f"reports/{filename}.pdf"

    # Fix markdown hierarchy for PDF generation
    fixed_report = fix_markdown_hierarchy(report)

    # Save Markdown file (save the original report)
    try:
        with open(filename_md, "w", encoding="utf-8") as f:
            f.write(report)
        logging.info(f"Markdown Report saved to: {filename_md}")
    except Exception as e:
        return f"❌ Failed to save Markdown report: {str(e)}"

    # Generate PDF using fixed markdown
    pdf_status = ""
    try:
        pdf = MarkdownPdf()
        pdf.meta["title"] = topic
        pdf.add_section(Section(fixed_report, toc=True))
        pdf.save(filename_pdf)
        logging.info(f"PDF Report saved to: {filename_pdf}")
        pdf_status = f"✅ PDF: {filename_pdf}\n"
    except Exception as e:
        logging.warning(f"PDF generation failed: {e}")
        logging.info(f"Markdown report still saved to: {filename_md}")
        pdf_status = f"⚠️  PDF generation failed (Markdown still saved)\n"

    # Auto-ingest report into RAG knowledge base
    rag_status = ""
    try:
        logging.info("Adding report to RAG knowledge base...")
        rag_result = auto_ingest_report(
            report_content=report,
            topic=topic,
            state=state,  # type: ignore
        )

        if rag_result.get("success"):
            chunks = rag_result.get("chunks_added", 0)
            logging.info(f"Report added to RAG: {chunks} chunks indexed")
            logging.info("Future research can now reference this report!")
            rag_status = f"✅ RAG: {chunks} chunks indexed - Future research can reference this!\n"
        else:
            error = rag_result.get("error", "Unknown error")
            logging.warning(f"RAG ingestion failed: {error}")
            logging.info("Report saved but not added to knowledge base")
            rag_status = f"⚠️  RAG ingestion failed: {error}\n"

    except Exception as e:
        logging.warning(f"Could not add to RAG: {str(e)}")
        logging.info("Check RAG_DIR in .env and ensure vector store is accessible")
        rag_status = f"⚠️  RAG ingestion failed: {str(e)}\n"
    # Return comprehensive status
    return (
        f"📄 Report saved successfully!\n\n"
        f"✅ Markdown: {filename_md}\n"
        f"{pdf_status}"
        f"\n📊 Report details:\n"
        f"  - Topic: {topic}\n"
        f"  - Length: {len(report)} characters\n"
        f"  - Timestamp: {timestamp}"
    )


# Maximum characters to return from any single tool to prevent token overflow
MAX_TOOL_OUTPUT_CHARS = 8000


def _truncate_output(text: str, max_chars: int = MAX_TOOL_OUTPUT_CHARS) -> str:
    """Truncate tool output to prevent token overflow."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n... [Output truncated at {max_chars} characters]"


@tool
def search_tavily(query: str) -> str:
    """Search the web for current information, news, and general knowledge.

    Use this tool when you need to:
    - Find recent news, events, or developments
    - Look up current facts, statistics, or data
    - Research general topics across multiple web sources
    - Verify information or get multiple perspectives
    - Find real-time information (weather, stock prices, etc.)

    The tool searches across the web and returns the top 5 most relevant results
    with snippets for efficient analysis.

    Args:
        query: Search query string for web search

    Returns:
        Formatted search results with titles, URLs, and snippets from up to
        5 relevant web sources.
    """
    # Use include_raw_content=False to avoid massive content that causes token overflow
    result = TavilySearch(max_results=5, include_raw_content=False).invoke(query)
    return _truncate_output(str(result))


@tool
def search_pubmed(query: str) -> str:
    """Search peer-reviewed biomedical and life sciences literature on PubMed.

    Use this tool when you need to:
    - Find scientific research papers and clinical studies
    - Access peer-reviewed medical and health information
    - Research diseases, treatments, drugs, or medical procedures
    - Find evidence-based information on health topics
    - Look up genetic, molecular, or biological research
    - Access NIH and other authoritative medical databases

    PubMed contains 35+ million citations from MEDLINE, life science journals,
    and online books, making it the authoritative source for medical research.

    Args:
        query: Medical or scientific search query using MeSH terms or medical terminology

    Returns:
        Formatted results with article titles, authors, abstracts, and publication
        details from relevant peer-reviewed sources.

    Note:
        For general health questions or news, use search_tavily instead.
        Use this tool specifically for scientific/medical research literature.
    """
    result = PubmedQueryRun().invoke(query)
    return _truncate_output(str(result))


@tool
def search_arxiv(query: str, max_results: int = 3) -> str:
    """Search arXiv for academic papers in physics, math, CS, and related fields.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 3)

    Returns:
        Formatted list of papers with titles, authors, abstracts, and links
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for paper in client.results(search):
            results.append(
                f"""
                **{paper.title}**
                - Authors: {', '.join([author.name for author in paper.authors])}
                - Published: {paper.published.strftime('%Y-%m-%d')}
                - Abstract: {paper.summary[:300]}...
                - PDF: {paper.pdf_url}
                - arXiv ID: {paper.entry_id}
                """
            )

        if not results:
            return f"❌ No papers found on arXiv for query: '{query}'\n\nSuggestions:\n- Try broader search terms\n- Check spelling\n- Use technical keywords\n- Try alternative terminology"

        return "\n\n".join(results)

    except Exception as e:
        return f"❌ Error searching arXiv: {str(e)}\n\nThis might be due to:\n- Network connectivity issues\n- arXiv API temporarily unavailable\n- Invalid query format"


@tool
def rag_tool(question: str, collection_name: str = "research_reports") -> str:
    """Query your personal document knowledge base using RAG.
    Essential for retrieving information from your ingested documents.

    Args:
        question: Question to ask about your documents
        collection_name: Name of the vector store collection (default: "research_reports")
    """
    try:
        rag_dir = os.getenv("RAG_DIR")

        if not rag_dir or not os.path.exists(rag_dir):
            return (
                f"❌ Vector store not found at: {rag_dir or 'Not configured'}\n\n"
                f"To use RAG tool:\n"
                f"1. Set RAG_DIR in your .env file\n"
                f"2. Run document ingestion to create the vector store\n"
                f"3. Ensure documents are properly indexed"
            )

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )

        try:
            vectorstore = Chroma(
                persist_directory=rag_dir,
                embedding_function=embeddings,
                collection_name=collection_name,
            )
        except Exception as ve:
            return (
                f"❌ Failed to load vector store\n\n"
                f"Error: {str(ve)}\n\n"
                f"Possible causes:\n"
                f"- Vector store corrupted\n"
                f"- Collection '{collection_name}' doesn't exist\n"
                f"- Permission issues accessing {rag_dir}"
            )

        # Use MMR (Maximal Marginal Relevance) for better diversity in results
        retriever = vectorstore.as_retriever(
            search_type="mmr",  # Maximal Marginal Relevance for diversity
            search_kwargs={
                "k": 5,  # Number of documents to return
                "fetch_k": 20,  # Number of documents to fetch before filtering
                "lambda_mult": 0.7,  # Diversity factor (0=max diversity, 1=max relevance)
            },
        )
        source_docs = retriever.invoke(question)

        if not source_docs:
            return (
                f"❌ No relevant documents found in knowledge base for: '{question}'\n\n"
                f"Suggestions:\n"
                f"- Try rephrasing your question\n"
                f"- Use different keywords\n"
                f"- Check if relevant documents were ingested\n"
                f"- Verify collection name: '{collection_name}'\n"
                f"- Try broader search terms"
            )

        context = "\n\n".join(doc.page_content for doc in source_docs)

        template = """You are a helpful assistant answering questions based on provided documents.
            Use the following context to answer the question. If you don't know based on the context, say so.

            Context:
            {context}

            Question: {question}

            Answer:"""

        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOllama(model="gpt-oss:20b-cloud", temperature=0)

        # Create chain
        rag_chain = (
            {"context": lambda x: context, "question": lambda x: question}
            | prompt
            | llm
            | StrOutputParser()
        )

        answer = rag_chain.invoke({})

        sources_info = "\n\n📚 Sources:\n"
        for i, doc in enumerate(source_docs[:3], 1):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")
            preview = doc.page_content[:150].replace("\n", " ")
            sources_info += f"{i}. {source} (Page {page})\n   Preview: {preview}...\n"

        return _truncate_output(f"{answer}\n{sources_info}")

    except Exception as e:
        return (
            f"❌ RAG tool error: {str(e)}\n\n"
            f"Troubleshooting:\n"
            f"- Check if LLM model 'gpt-oss:20b-cloud' is available\n"
            f"- Verify vector store integrity\n"
            f"- Check system resources (memory, disk space)"
        )


@tool
def duck_duck_go_search(query: str) -> str:
    """Search DuckDuckGo for a given query. Results are returned in English."""
    try:
        # Configure wrapper to return English results from US region
        wrapper = DuckDuckGoSearchAPIWrapper(
            region="us-en",  # Force US English results
            max_results=5,  # Standard result count
            safesearch="moderate",  # Moderate safe search
        )
        search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        res = search.run(query)

        if not res or res.strip() == "":
            return (
                f"❌ No results found on DuckDuckGo for: '{query}'\n\n"
                f"Suggestions:\n"
                f"- Try different keywords\n"
                f"- Use more specific terms\n"
                f"- Check spelling\n"
                f"- Try a different search tool"
            )

        return _truncate_output(res)
    except Exception as e:
        return (
            f"❌ DuckDuckGo search error: {str(e)}\n\n"
            f"Possible causes:\n"
            f"- Network connectivity issues\n"
            f"- Rate limiting (too many requests)\n"
            f"- Service temporarily unavailable\n"
            f"- Query format issues"
        )


@tool
def duck_duck_go_search_results(query: str) -> str:
    """Search DuckDuckGo for a given query and return structured results. Results are returned in English."""
    try:
        # Configure wrapper to return English results from US region
        wrapper = DuckDuckGoSearchAPIWrapper(
            region="us-en",  # Force US English results
            max_results=5,  # Standard result count
            safesearch="moderate",  # Moderate safe search
        )
        search = DuckDuckGoSearchResults(api_wrapper=wrapper)
        res = search.run(query)

        if not res or res.strip() == "" or res == "[]":
            return (
                f"❌ No search results found on DuckDuckGo for: '{query}'\n\n"
                f"Suggestions:\n"
                f"- Try broader search terms\n"
                f"- Remove special characters\n"
                f"- Use common terminology\n"
                f"- Try alternative search tools (Tavily, Wikipedia)"
            )

        return _truncate_output(res)
    except Exception as e:
        return (
            f"❌ DuckDuckGo search results error: {str(e)}\n\n"
            f"This could be due to:\n"
            f"- Rate limiting (wait a few moments)\n"
            f"- Network issues\n"
            f"- Invalid characters in query\n"
            f"- Service availability"
        )


@tool
def summarize_text(text: str) -> str:
    """
    Summarizes a given text.
    Useful for summarizing research reports, markdowns, or long notes.
    """
    try:
        if not text or text.strip() == "":
            return (
                "❌ No text provided to summarize\n\nPlease provide valid text content."
            )

        if len(text) < 50:
            return (
                f"❌ Text too short to summarize (only {len(text)} characters)\n\n"
                f"Minimum recommended: 50 characters\n"
                f"Provided text: '{text[:100]}...'"
            )

        llm = ChatOllama(model="gpt-oss:20b-cloud", temperature=0.7)
        template = """Summarize the following text in clear, structured Markdown format. Keep all essential details, and include a 'Key Takeaway' section at the end:

{text}"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = {"text": lambda x: text} | prompt | llm | StrOutputParser()
        summary = chain.invoke({"text": text})

        if not summary or summary.strip() == "":
            return (
                "❌ Failed to generate summary\n\n"
                "The LLM returned an empty response. Try:\n"
                "- Checking if the LLM model is running\n"
                "- Verifying text format\n"
                "- Using different text content"
            )

        return summary

    except Exception as e:
        return (
            f"❌ Summarization error: {str(e)}\n\n"
            f"Troubleshooting:\n"
            f"- Check if Ollama is running\n"
            f"- Verify model 'gpt-oss:20b-cloud' is installed\n"
            f"- Check system resources\n"
            f"- Try with shorter text"
        )


@tool
def wiki_search(query: str) -> str:
    """Search Wikipedia and return a concise summary."""
    try:
        # Limit to 10 sentences to prevent token overflow
        res = wikipedia.summary(query, sentences=10)

        if not res or res.strip() == "":
            return (
                f"❌ No Wikipedia article found for: '{query}'\n\n"
                f"Suggestions:\n"
                f"- Check spelling\n"
                f"- Try alternative terms\n"
                f"- Use more specific or general terms\n"
                f"- Try related topics"
            )

        return _truncate_output(res)
    except wikipedia.exceptions.DisambiguationError as de:
        options = de.options[:5]  # Get first 5 options
        return (
            f"❌ Wikipedia disambiguation required for: '{query}'\n\n"
            f"Multiple articles found. Please be more specific:\n"
            + "\n".join([f"- {opt}" for opt in options])
        )
    except wikipedia.exceptions.PageError:
        return (
            f"❌ No Wikipedia page found for: '{query}'\n\n"
            f"Suggestions:\n"
            f"- Verify the topic exists on Wikipedia\n"
            f"- Try different keywords\n"
            f"- Check for spelling errors\n"
            f"- Try broader or more common terms"
        )
    except Exception as e:
        return (
            f"❌ Wikipedia search error: {str(e)}\n\n"
            f"This might be caused by:\n"
            f"- Network connectivity issues\n"
            f"- Wikipedia API temporarily down\n"
            f"- Invalid query format\n"
            f"- Rate limiting"
        )


@tool
def extract_pdf_content(pdf_url: str) -> str:
    """Download and extract text from academic PDFs.

    Essential for:
    - Reading full papers from arXiv PDFs
    - Extracting methodology sections
    - Getting complete citations
    - Accessing supplementary materials

    Args:
        pdf_url: URL to the PDF file

    Returns:
        Extracted text content (first 3 pages, limited to 3000 chars)
    """
    try:
        from langchain_community.document_loaders import PyPDFLoader

        # Download PDF
        print(f"[PDF] Downloading from {pdf_url}...")
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name

        # Load and extract
        print(f"[PDF] Extracting content...")
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        # Extract first 3 pages (abstract, intro, methodology)
        content = "\n\n".join(
            [
                f"--- Page {i+1} ---\n{page.page_content}"
                for i, page in enumerate(pages[:3])
            ]
        )

        # Cleanup
        os.unlink(tmp_path)

        # Handle Unicode characters that may cause encoding issues
        # Replace problematic characters with ASCII equivalents
        result = content[:3000]  # Limit output
        # Encode to ASCII, replacing unsupported characters
        result = result.encode("ascii", errors="replace").decode("ascii")

        return f"[SUCCESS] Successfully extracted PDF content:\n\n{result}\n\n... (truncated for brevity)"

    except ImportError:
        return "[ERROR] PyPDF2 not installed\n\n" "Install with: pip install pypdf"
    except requests.exceptions.RequestException as e:
        return (
            f"[ERROR] Failed to download PDF: {str(e)}\n\n"
            "Possible causes:\n"
            "- Invalid URL\n"
            "- Network connectivity issues\n"
            "- PDF requires authentication\n"
            "- Timeout (large file)"
        )
    except Exception as e:
        return (
            f"[ERROR] Error extracting PDF: {str(e)}\n\n"
            "Troubleshooting:\n"
            "- Verify PDF format is valid\n"
            "- Check if file is corrupted\n"
            "- Try a different PDF URL"
        )


@tool
def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
    """Fetch and convert webpage content to markdown.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Webpage content as markdown (truncated to prevent token overflow)
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        content = markdownify(response.text)
        return _truncate_output(content)
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"


@tool
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"


@tool
def semantic_scholar_search(query: str, limit: int = 5) -> str:
    """Search Semantic Scholar for academic papers with citation metrics.

    Better than arXiv alone because:
    - Covers ALL fields (not just STEM)
    - Includes citation counts and influential citations
    - Has full-text search across paper content
    - Provides paper recommendations

    Args:
        query: Search query string
        limit: Maximum number of results (default: 5)

    Returns:
        Formatted list of papers with titles, authors, citations, and links
    """
    try:
        result = SemanticScholarQueryRun().invoke(query, top_k_results=limit)

        return _truncate_output(str(result))

    except Exception as e:
        return (
            f"[ERROR] Error searching Semantic Scholar: {str(e)}\n\n"
            "Try again in a moment or use alternative search tools."
        )


@tool
def check_grammar(text: str) -> str:
    """Check grammar, spelling, and style issues.

    Uses LanguageTool for:
    - Grammar errors
    - Spelling mistakes
    - Style suggestions
    - Punctuation issues

    Args:
        text: Text to check (first 1000 chars analyzed)

    Returns:
        List of issues with suggestions
    """
    MAX_TEXT_LENGTH = 1000
    MAX_ISSUES_DISPLAY = 10
    MAX_SUGGESTIONS = 3

    try:
        # Limit text length to avoid timeouts
        text = text[:MAX_TEXT_LENGTH]
        print(f"[GRAMMAR] Checking {len(text)} characters...")

        tool = language_tool_python.LanguageTool("en-US")

        try:
            matches = tool.check(text)

            if not matches:
                return "[SUCCESS] No grammar or style issues detected!"

            # Format issues
            issues = []
            for i, match in enumerate(matches[:MAX_ISSUES_DISPLAY], 1):
                suggestions = (
                    ", ".join(match.replacements[:MAX_SUGGESTIONS])
                    if match.replacements
                    else "N/A"
                )
                rule_id = getattr(match, "ruleId", getattr(match, "rule_id", "Unknown"))

                issues.append(
                    f"{i}. {match.message}\n"
                    f"   Context: ...{match.context}...\n"
                    f"   Suggestion: {suggestions}\n"
                    f"   Category: {rule_id}"
                )

            # Build summary
            summary = f"Found {len(matches)} issue(s) (showing first {MAX_ISSUES_DISPLAY}):\n\n"
            summary += "\n\n".join(issues)

            if len(matches) > MAX_ISSUES_DISPLAY:
                summary += (
                    f"\n\n... and {len(matches) - MAX_ISSUES_DISPLAY} more issues"
                )

            return summary

        finally:
            tool.close()

    except Exception as e:
        return (
            f"[ERROR] Grammar check failed: {str(e)}\n\n"
            "Note: First run requires internet to download language models"
        )
