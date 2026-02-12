# ΔPrompt — Sample Prompts

This file contains **canonical examples** of ΔPrompt (Delta Prompting) across common task categories.
Each prompt encodes **only deviations from baseline behavior**, not full instructions.

---

## Creative Task

```text
Baseline: coherent, engaging, modern prose, neutral tone.

Δ(write short story | ~300 words, bleak tone, minimalist style, ambiguous ending)

Theme:
A future where memories can be deleted, but one memory refuses to disappear.
```

---

## Reasoning Task

```text
Baseline: concise, correct, no explicit reasoning unless required.

Δ(solve | multi-step math, show reasoning, final answer boxed)

Problem:
A train travels 60 km at 30 km/h and then 60 km at 60 km/h.
What is the average speed for the entire trip?
```

---

## Coding Task

```text
Baseline: idiomatic, readable Python, correct by default.

Δ(implement function | O(n) time, no external libraries, no comments, include simple tests)

Task:
Write a function `first_unique_char(s: str) -> int` that returns the index of the
first non-repeating character in a string, or -1 if none exists.
```

---

## Data Analysis Task

```text
Baseline: rigorous, verified, cited, no marketing language.

Δ(analyze dataset | identify 3 key trends, output as markdown table, include Python code)

Task:
Analyze the provided sales data for the last 2 years and identify quarterly growth patterns.
```

---

## Copy Editing Task

```text
Baseline: modern, neutral prose, descriptive, high-quality.

Δ(review text | grammar and flow only, no structural changes, neutral tone)

Task:
Please review the attached blog post for any grammatical errors and ensure the
transitions between paragraphs are smooth.
```

---

## Multi-Step Tool-Using Agent

```text
Baseline: autonomous, reliable, minimal verbosity, no tool use unless helpful.

Δ(act as research agent | plan-first, explicit tool calls, verify before summarizing, ask before finalizing)

Goal:
Identify the top 3 open-source vector databases suitable for production use.

Tools available:
- Web search
- Documentation lookup
- Comparison table generator

Constraints:
- Focus on maturity, scalability, ecosystem
- Cite sources
- No marketing language

Output format:
1. Brief plan
2. Tool calls (annotated)
3. Comparison table
4. Recommendation + uncertainty notes
5. Ask user whether to proceed
```

---

## AI Agent Task

```text
Baseline: autonomous, goal-oriented, safe, minimal verbosity, explain decisions briefly.

Δ(act as task agent | plan-first, ask before irreversible actions, output checklist + next action)

Goal:
Research and prepare a short comparison of the top 3 task-management tools
for small engineering teams, focusing on pricing, integrations, and learning curve.
```

---

## Multi Step - Coordination Agent

**Scenario:**
A small product team wants to evaluate whether to adopt a new feature: **Metrics feature to their Ads Platform**.
Three agents collaborate: Research, Engineering, and Product.

### Shared Baseline (Declared Once)

```text
Baseline: cooperative, concise, factual, respect other agents’ outputs,
do not repeat information already provided unless correcting it.
```

### Agent 1 — Research Agent

```text
Δ(act as research agent | gather evidence, cite sources, no recommendations)

Task:
Summarize current industry practices and user demand related to the proposed feature.
```

### Agent 2 — Engineering Agent

```text
Δ(act as engineering agent | feasibility-focused, surface risks, estimate effort)

Task:
Evaluate technical feasibility, dependencies, and implementation complexity
based on the research agent’s findings.
```

### Agent 3 — Product Agent

```text
Δ(act as product agent | synthesize inputs, decision-oriented, no new research)

Task:
Based on research and engineering inputs, recommend whether to proceed,
including key tradeoffs and uncertainties.
```

### Coordination Rules (Δ-Based)

```text
Δ(wait for prior agents before responding)
Δ(reference other agents instead of restating)
Δ(flag disagreements explicitly)
```

### 🤖 Scenario Agent Output

Three agents collaborated: Research, Engineering, and Product.

**Research Agent**
```text
Industry practices for metrics in ad platforms include tracking core KPIs like impressions, CTR, CPC, conversion rate, CPA, ROAS, ROI, and engagement rate across platforms (Google Ads, Meta, etc.). 

Best practices: align with marketing funnel, consolidate cross-platform data, automate via APIs, use multiple tracking methods. 

Emerging: attention metrics (view time, emotional response) for better optimization beyond impressions/clicks; 36% of US ad buyers prioritize them. Shift to incrementality and media mix modeling due to privacy constraints.

User demand: 47% of marketers struggle with ROI measurement; over 60% track CTR/conversion rates for campaign tuning. Rising ad costs (CPL +25%, CPC +10%) drive need for efficient metrics to optimize spend and prove value. Demand for attention metrics and data-driven insights to identify working tactics. No recent X discussions found on demand/practices.
```

**Engineering Agent**
```text
Feasible to implement metrics feature: integrate standard KPIs (impressions, CTR, etc.) via APIs from ad platforms, as per Research Agent's practices. Dependencies: data aggregation tools (e.g., for cross-platform consolidation), privacy-compliant tracking (e.g., for incrementality). 

Complexity: medium—build dashboard/UI for real-time metrics; estimate 4-6 weeks effort for core, plus 2 weeks for attention metrics if added. 

Risks: data silos across platforms, accuracy in privacy era, potential API rate limits/costs. No disagreements.
```

**Product Agent**
```text
Recommend proceeding: high user demand for ROI/optimization metrics aligns with industry shift to advanced tracking (e.g., attention, incrementality). 

Tradeoffs: medium engineering effort vs. improved campaign efficiency/revenue potential. 

Uncertainties: adoption rate if basic metrics suffice; privacy regulations impacting data accuracy. No new research; references Research/Engineering inputs.
```

---

## Notes

* **Baseline** statements should be declared once per session when possible.
* ΔPrompts are **incrementally composable** in follow-up turns:

  1. **User:** `Explain how a transformer model works.`
  2. **User:** `Δ(more formal)` → *Model rewrites explanation in a formal tone.*
  3. **User:** `Δ(add counterexample)` → *Model adds a counterexample to the formal explanation.*
  4. **User:** `Δ(shorter)` → *Model shortens the entire combined output while maintaining prior deltas.*
* When behavior drifts, re-anchor briefly.

---

## Anchoring

Anchoring sets a persistent baseline for the entire session. Once anchored, you only need to use deltas for specific modifications.

### Setting a Technical Baseline
```text
Baseline: Technical, Pythonic, no comments, minimal verbosity.
```

### Setting an Agentic Baseline
```text
Baseline: Autonomous, plan-first, explicit tool use, ask before recommending.
```

---

## Philosophy

> *If the model is competent, instructions should be corrective — not exhaustive.*

ΔPrompt encodes intent through **difference, not repetition**.
