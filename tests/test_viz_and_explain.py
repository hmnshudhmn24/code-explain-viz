import os
from data_examples.example_code import factorial
from inference import CodeExplainViz

def test_explain_and_viz_runs():
    with open("data_examples/example_code.py", "r", encoding="utf-8") as f:
        code = f.read()
    expl = CodeExplainViz()
    out = expl.explain(code)
    assert "mermaid" in out
    assert out["mermaid"].startswith("flowchart")
    assert isinstance(out["short"], str)
    assert len(out["short"]) > 0
