# ⚙️ CODE-EXPLAIN-VIZ

> 🧠 **Explain. Visualize. Test.** — Turn Python code into clear explanations, flowcharts, and test templates.


## 🚀 Quick Start

1️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

2️⃣ **Run the CLI demo:**
```bash
python cli.py --file data_examples/example_code.py
```

3️⃣ **Visualize your code:**
👉 Copy the **Mermaid flowchart** text printed by the CLI  
👉 Paste it into [Mermaid Live Editor](https://mermaid.live)  
👉 Or render it using **mermaid-cli** to see your control flow visually!


## 💡 What You Get

| Output | Description |
|--------|--------------|
| 📝 **short** | One-line summary of what the function does |
| 📖 **detailed** | Step-by-step explanation of the logic |
| 🧩 **mermaid** | Mermaid-based flowchart of control flow |
| 🧪 **unit_tests** | Auto-generated pytest template |


## 🔍 How It Works

✨ **LLM + AST Magic**

- 🤖 A **CodeT5 model** generates natural-language explanations from source code.  
- 🧠 `viz_generator.py` parses your function’s **AST** (Abstract Syntax Tree) to produce a **Mermaid flowchart**.  
- 🔗 Combining both gives you a **human-friendly explanation** + a **deterministic code visualization**.


## 🧬 Train / Fine-tune

Fine-tune your own model using:
```bash
python train_docgen.py --data data/train_data.jsonl
```

📁 **Dataset format (JSONL):**
Each line should contain:
```json
{"code": "...", "doc": "..."}
```

## 🎯 Summary

**code-explain-viz** helps you:
✅ Understand code with AI-powered explanations  
✅ Visualize logic flow clearly with Mermaid diagrams  
✅ Auto-generate unit test templates for quick validation
