"""
Output format templates for consistent agent responses.

This module defines standard output structures for different
agent roles to ensure consistent, well-organized responses.
"""

RESEARCH_OUTPUT_FORMAT = """
═══════════════════════════════════════════════════════════════
OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════

## Research Summary
[2-3 paragraph overview of key findings]

## Key Findings

### Finding 1: [Clear heading]
- **Details**: [Comprehensive explanation]
- **Source**: [Title] - [Complete URL]
- **Quality**: [Peer-reviewed/Industry/News/Blog] | [Date]
- **Confidence**: [High/Medium/Low]

### Finding 2: [Clear heading]
[Same structure...]

## Important Data Points

| Metric/Statistic | Value | Source | Year | Notes |
|------------------|-------|--------|------|-------|
| [Metric] | [Value] | [URL] | [Year] | [Context] |

## Information Gaps
[What couldn't be found but would be valuable]

## All Sources (Complete Bibliography)
**CRITICAL: Include URL for EVERY source**
- Source Title 1: https://complete-url-1.com
- Source Title 2: https://complete-url-2.com
"""

ANALYSIS_OUTPUT_FORMAT = """
═══════════════════════════════════════════════════════════════
OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════

## Key Findings
- 3-5 bullets focusing on MOST IMPORTANT insights
- Format: "Finding X shows Y ([Source](URL))"
- Order by importance/impact

## Important Trends or Patterns
- 2-4 bullets on SIGNIFICANT recurring themes
- Identify directionality: increasing/decreasing/stable
- Cross-reference when available

## Notable Statistics or Data
- 2-5 KEY data points (not every number)
- Format: "Metric: 47.3% ([Study Name](URL))"
- Include ranges for estimates

## Gaps in Information (if significant)
- 1-3 CRITICAL missing pieces
- Only include gaps that MATTER for decision-making

## Sources Referenced
- [Descriptive Source Title](https://exact-url.com)
- List by order of importance or appearance
"""

SYNTHESIS_OUTPUT_FORMAT = """
═══════════════════════════════════════════════════════════════
OUTPUT FORMAT (Comprehensive Report):
═══════════════════════════════════════════════════════════════

# [Research Topic Title]

## Executive Summary
[200-300 word high-level overview]
- Research question addressed
- Key methodology
- Major findings (3-5 bullets)
- Primary conclusions
- Actionable insights

---

## 1. Introduction

### 1.1 Research Context
[Background and motivation]

### 1.2 Research Objectives
[Specific questions addressed]

### 1.3 Scope and Methodology
[What was researched and how]

---

## 2. Findings

[Organize by THEMES, not by source]

### 2.1 [Theme 1]
[Integrate relevant findings with citations]

### 2.2 [Theme 2]
[Continue for all major themes...]

---

## 3. Analysis and Insights

### 3.1 Key Patterns Identified
[Trends and patterns across research]

### 3.2 Critical Insights
[Important conclusions and "aha" moments]

### 3.3 Contradictions and Debates
[Where sources disagreed]

---

## 4. Conclusion

### 4.1 Summary of Key Findings
[Restate main discoveries]

### 4.2 Implications
[What this means]

### 4.3 Recommendations
[Actionable next steps]

---

## References

**CRITICAL: EVERY reference MUST include complete URL**

[1] Source Title: https://complete-url.com
[2] Another Source: https://another-url.com
"""

BRIEF_OUTPUT_FORMAT = """
═══════════════════════════════════════════════════════════════
BRIEF OUTPUT FORMAT (200-400 words):
═══════════════════════════════════════════════════════════════

## [Topic] - [Timestamp]

**WHAT HAPPENED:**
[1-2 sentences]

**WHY IT MATTERS:**
[1-2 sentences]

**KEY DETAILS:**
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

**SOURCES:**
- [Link 1]
- [Link 2]

**CONFIDENCE:** [High/Medium/Low]
**BASED ON:** [X sources, Y hours old]
"""

COMPARISON_OUTPUT_FORMAT = """
═══════════════════════════════════════════════════════════════
COMPARISON OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════

# [Option A] vs [Option B] vs [Option C]

## Executive Summary
- Quick verdict: When to use each option
- Winner by category (if clear)

## Individual Overviews

### Option A: [Name]
- What it is
- Key strengths
- Key weaknesses
- Best for: [use cases]

### Option B: [Name]
[Same structure]

## Side-by-Side Comparison

### Feature Matrix
| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| [Feature 1] | [Details] | [Details] | [Details] |

### Performance Comparison
| Metric | Option A | Option B | Option C |
|--------|----------|----------|----------|
| [Metric] | [Value] | [Value] | [Value] |

## Recommendations

### Choose Option A if:
- [Condition 1]
- [Condition 2]

### Choose Option B if:
- [Condition 1]
- [Condition 2]

## Overall Assessment
[Balanced conclusion]
"""

CRITIQUE_OUTPUT_FORMAT = """
═══════════════════════════════════════════════════════════════
CRITIQUE OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════

## Critique Summary

**Overall Quality Score: X/10**

Brief assessment (2-3 sentences) of strengths and weaknesses.

---

## Detailed Evaluation

### Completeness: X/10
- ✓ Strength: [what's well covered]
- ✗ Weakness: [what's missing]
- → Recommendation: [specific improvement]

### Accuracy: X/10
- ✓ Strength: [what's well-sourced]
- ✗ Weakness: [questionable claims]
- → Recommendation: [how to verify]

### Depth: X/10
- ✓ Strength: [deep insights]
- ✗ Weakness: [superficial areas]
- → Recommendation: [how to deepen]

### Clarity: X/10
- ✓ Strength: [clear sections]
- ✗ Weakness: [confusing parts]
- → Recommendation: [how to clarify]

---

## Improvement Roadmap

**Priority 1 (Must Fix):**
- [Critical issue]

**Priority 2 (Should Fix):**
- [Important issue]

**Priority 3 (Nice to Have):**
- [Enhancement]
"""
