"""
Quality standards and thresholds for research agents.

This module defines consistent quality expectations across all
agents to ensure balanced, realistic evaluation criteria.
"""

QUALITY_STANDARDS = """
═══════════════════════════════════════════════════════════════
QUALITY STANDARDS:
═══════════════════════════════════════════════════════════════

**Philosophy: Quality is relative to information availability**

REALISTIC EXPECTATIONS:
✓ Find AVAILABLE sources (1-2 quality sources are acceptable)
✓ Extract key findings from what EXISTS
✓ Document what you found AND what you didn't find
✓ Minimum 2-3 sources with complete URLs
✓ Show evidence of honest tool usage

INFORMATION SCARCITY IS NORMAL FOR:
- Emerging technologies (< 6 months old)
- Niche academic subfields
- Proprietary/commercial innovations
- Regional or localized topics
- Recent developments with limited publications

Research is COMPLETE when:
✓ You made honest attempts with multiple tools
✓ You documented what you FOUND (even if limited)
✓ You explained what ISN'T available (if applicable)
✓ You extracted meaningful insights from available sources
✓ You provide value to the next phase (even if modest)

DO NOT waste iterations if:
❌ Multiple tools return no relevant results for niche topics
❌ Only 1-2 sources exist (this is VALID - document them well!)
❌ Information is genuinely scarce (acknowledge as a finding)
"""

QUALITY_CHECKLIST = """
═══════════════════════════════════════════════════════════════
QUALITY CHECKLIST:
═══════════════════════════════════════════════════════════════

**For Research:**
✓ All findings extracted from tool calls
✓ Key findings explicitly stated with sources
✓ Minimum 2-3 sources cited with complete URLs
✓ Evidence of structured research process
✓ Gaps and limitations documented

**For Analysis:**
✓ Major statistics have source URLs
✓ Important URLs preserved exactly
✓ [Unverified] flag added if critical claims lack sources
✓ [Speculative] tags applied to uncertain key data
✓ Actionable insights provided

**For Reports:**
✓ All source URLs preserved exactly as provided
✓ Sources section includes every referenced URL
✓ Inline citations use proper markdown links
✓ Logical flow and clear structure
✓ Abstract/Overview accurately reflects content
✓ Report answers original research question

**For All:**
✓ No fabricated data or sources
✓ Honest acknowledgment of limitations
✓ Clear, professional communication
"""

QUALITY_THRESHOLDS = """
═══════════════════════════════════════════════════════════════
QUALITY THRESHOLDS (Lenient & Completion-Focused):
═══════════════════════════════════════════════════════════════

**Scoring Scale:**
- 9-10: Exceptional - Outstanding quality for available information
- 7-8: Strong - Solid work given constraints
- 5-6: Good - Meets requirements, accomplishes goals
- 4-5: Acceptable - Basic requirements met, useful output
- 2-3: Weak - Some issues, but has value
- 1: Broken - Fundamental problems, unusable

**Acceptance Criteria:**
- Score ≥5: Approve immediately (good quality)
- Score 4: Approve (acceptable quality)
- Score 3: Approve for limited-info topics
- Score <3: Only reject if genuinely broken

**Context-Specific Scoring:**
- Limited-info topics (1-2 sources): Score 4-6 is typical
- Moderate-info topics (3-5 sources): Score 5-7 is typical
- Abundant-info topics (6+ sources): Score 6-8 is typical
- Emerging/niche topics: Score 3-5 is often appropriate

**Key Principles:**
- COMPLETION is mandatory
- LIMITED INFORMATION ≠ Poor Quality
- A finished report with gaps > no report
- Good enough beats perfect (never delivered)
"""

ITERATION_LIMITS = """
═══════════════════════════════════════════════════════════════
ITERATION LIMITS:
═══════════════════════════════════════════════════════════════

**Hard Limits (Prevent Endless Loops):**
- Max refinement iterations: 1 total
- Max quality check cycles: 2
- After 4+ total iterations: END immediately
- After research_done=True: MUST proceed to next phase

**When to Stop Iterating:**
- Quality score ≥ 5/10
- All critical gaps addressed
- Max iterations reached
- Diminishing returns (improvement < 1 point)
- Information genuinely doesn't exist

**When to Continue:**
- Quality score < 3/10 (genuinely broken)
- Critical factual errors identified
- No usable content produced
- Core question completely unanswered

**NEVER Iterate Because Of:**
- "Could have more sources" (accept what exists)
- "Limited information" (this is valid)
- "Not comprehensive enough" (completeness is relative)
- Minor gaps or nice-to-haves
"""

EVALUATION_DIMENSIONS = """
═══════════════════════════════════════════════════════════════
EVALUATION DIMENSIONS:
═══════════════════════════════════════════════════════════════

**1. COMPLETENESS (0-10)**
Assess relative to AVAILABLE information:
- Are available sources well-utilized?
- Is scope appropriate given availability?
- Is information scarcity acknowledged?
- Don't penalize for gaps that don't exist

**2. ACCURACY (0-10)**
Focus on correctness, not volume:
- Are claims properly sourced?
- Are there factual errors?
- Are sources reliable?
- For 1-2 sources: proper citation = full marks

**3. DEPTH (0-10)**
Relative to information availability:
- Is available information well-analyzed?
- For abundant info: synthesis expected
- For limited info: clear explanation = good depth
- Don't demand analysis of non-existent data

**4. CLARITY (0-10)**
Communication quality:
- Is structure logical?
- Is terminology explained?
- Are arguments clear?
- Short, clear reports score highly

**5. USEFULNESS (0-10)**
Value provided:
- Does it inform the reader?
- Is it valuable for decisions?
- For limited-info: does it state what is/isn't known?
"""
