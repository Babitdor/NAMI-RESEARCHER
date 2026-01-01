"""
Citation requirements module for consistent source attribution.

This module defines the standard citation format and requirements
that should be used across all research agents.
"""

CITATION_REQUIREMENTS = """
═══════════════════════════════════════════════════════════════
CITATION REQUIREMENTS (NON-NEGOTIABLE):
═══════════════════════════════════════════════════════════════

1. **PRESERVE all URLs exactly as returned by tools**
   - Never modify, shorten, truncate, or paraphrase URLs
   - Copy URLs character-for-character from search results

2. **Format for inline citations:**
   - Use markdown link format: [Descriptive Title](https://complete-url.com)
   - Include publication year when available
   - Note source type: [Paper], [Article], [Documentation], etc.

3. **Format for source lists:**
   - [1] Source Title: https://complete-exact-url.com
   - [2] Another Source: https://another-url.com
   - Number sources sequentially without gaps

4. **Source attribution requirements:**
   - Every major claim needs a source
   - Include author/publication when available
   - Rate confidence based on source quality

Example inline citation:
"Recent studies show significant improvements ([Stanford AI Index 2024](https://aiindex.stanford.edu/report/))"

Example source list:
### Sources
[1] Attention Is All You Need: https://arxiv.org/abs/1706.03762
[2] BERT: Pre-training of Deep Bidirectional Transformers: https://arxiv.org/abs/1810.04805
"""

CITATION_INLINE_FORMAT = """
**Inline Citation Format:**
- Format: "Finding or claim ([Source Title](https://url.com))"
- Include year: "According to research in 2024 ([Source](URL))..."
- Multiple sources: "This is supported by [1], [2], and [3]"
"""

CITATION_BIBLIOGRAPHY_FORMAT = """
**Bibliography Format:**
Each source must include:
- Sequential number: [1], [2], [3]...
- Descriptive title
- Complete URL
- Format: [N] Title: https://complete-url.com

Example:
### Sources
[1] OpenAI GPT-4 Technical Report: https://openai.com/research/gpt-4
[2] Anthropic Claude Model Card: https://anthropic.com/claude
[3] Google Gemini Overview: https://blog.google/technology/ai/gemini
"""

CITATION_QUALITY_HIERARCHY = """
**Source Quality Hierarchy:**
1. Peer-reviewed academic papers (highest quality)
2. Official documentation and technical reports
3. Industry whitepapers and research blogs
4. News articles from reputable outlets
5. Community discussions and forums (lowest, use with caution)

**Confidence Labels:**
- High: Peer-reviewed, multiple confirmations
- Medium: Single authoritative source
- Low: Single source, non-authoritative
- Speculative: No direct source, inference
"""
