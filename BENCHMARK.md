# ΔPrompt — Benchmarking Difference-Based Prompting and Agentic LLM Behavior

ΔPrompt benchmarked for **formally evaluating prompting strategies**, with a focus on **ΔPrompt (difference-based prompting)** and **ΔAgents (difference-driven AI agents)**.

Unlike traditional benchmarks that evaluate *models*, ΔPrompt benchmarked **how instructions are given**—measuring efficiency, quality, iteration cost, and agentic behavior under realistic workflows.

---

## ✨ Key Ideas

* **ΔPrompt**: Encode *only what changes* from a model’s default behavior.
* **Difference Encoding**: Treat prompts as corrections, not full specifications.
* **Efficiency First**: Token economy, iteration cost, and human effort matter.

---

## 🧠 Philosophy

> *If models are smart, prompts should be small.*

ΔPrompt exists to test that hypothesis.

---

## 📦 What ΔPrompt Does

ΔPrompt evaluated prompting methods across **five domains**:

| Domain | Focus                               |
| ------ | ----------------------------------- |
| EXPL   | Explanation clarity & efficiency    |
| REAS   | Reasoning activation & control      |
| CODE   | Coding correctness & iteration cost |
| CREA   | Creative control & refinement       |
| INST   | Instruction-following & safety      |
| AGENT  | Planning, tool use, autonomy        |

---

## 🧪 Prompting Regimes Compared

ΔPrompt compared:

1. Naive explicit prompting
2. Role-based prompting
3. Few-shot prompting
4. **ΔPrompt (with and without anchors)**
5. **ΔAgent (agentic variant)**

---

## 📊 Core Metrics

### Prompt-Level Metrics

* **PES** — Prompt Efficiency Score
* **IES** — Iterative Efficiency Score
* **DCR** — Delta Compression Ratio

### Agent-Specific Metrics

* Planning Quality (PQ)
* Tool Selection Accuracy (TSA)
* Tool Sequencing & State (TSS)
* Autonomy Control (AC)
* Hallucination Resistance (HR)
* Output Usefulness (OU)
* Token Efficiency (TE)

---

## 🧠 Example: ΔPrompt

```text
Baseline: concise, correct, neutral.

Δ(explain quantum entanglement | high-school level, <80 words, one analogy)
```

Only deviations from the baseline are specified.

---

## 🤖 Example: ΔAgent Prompt

```text
Baseline: autonomous, reliable, minimal verbosity.

Δ(act as research agent | plan-first, explicit tool calls, ask before recommending)

Goal:
Compare top 3 open-source vector databases for production use.
```

---

## 🧪 Running ΔPrompt (Conceptual)

ΔPrompt is model-agnostic. You can run it with, we tested with:

* X.AI - Grok 4.1
* OpenAI - GPT-5
* Anthropic - Claude 4.5
* Google - Gemini 3 Pro
* Local / open-source LLMs - Ollama etc.

Typical workflow:

1. Select task set
2. Apply each prompting regime
3. Log tokens, tool calls, outputs
4. Score using ΔPrompt metrics
5. Compare efficiency vs quality

---

## ⚠️ Limitations

* Requires careful baseline alignment
* Human evaluation still necessary for creative tasks
* Agent scoring assumes transparent tool traces

ΔPrompt evaluates *interaction strategy*, not model truthfulness guarantees.

---

## 🔮 Roadmap

* Automated ΔPrompt runner (Python)
* Agent failure-injection tests
* Multi-agent benchmarks

---

## 📄 Citation (Draft)

```bibtex
@misc{deltaprompt2026,
  title={ΔPrompt: Evaluating Difference-Based Prompting and Agentic LLM Behavior},
  author={Seyhun Akyurek},
  year={2026}
}
```

---

## 🤝 Contributing

Contributions welcome:

Open an issue or submit a PR.