# inference.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import textwrap
from viz_generator import code_to_mermaid

DEFAULT_MODEL = "Salesforce/codet5-small"

class CodeExplainViz:
    def __init__(self, model_name_or_path=DEFAULT_MODEL):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path)

    def explain(self, code: str, max_length: int = 256) -> dict:
        prompt = "explain: " + code
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(**inputs, max_length=max_length, num_beams=4, early_stopping=True)
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        short = lines[0] if lines else textwrap.shorten(text, width=120)
        detailed = "\n".join(lines[1:]) if len(lines) > 1 else text
        mermaid = code_to_mermaid(code)
        unit_tests = self._make_unit_test_template(code)
        return {"short": short, "detailed": detailed, "mermaid": mermaid, "unit_tests": unit_tests}

    def _make_unit_test_template(self, code: str) -> str:
        import re
        m = re.search(r"def\s+([A-Za-z0-9_]+)\s*\((.*?)\):", code)
        fn = m.group(1) if m else "function_under_test"
        params = m.group(2) if m else ""
        param_count = len([p for p in params.split(',') if p.strip()]) if params.strip() else 0
        args = ", ".join(["0"] * param_count)
        template = f"""import pytest

from your_module import {fn}

def test_{fn}_basic():
    # TODO: replace with real inputs and expected outputs
    assert {fn}({args}) == ...

def test_{fn}_edge_cases():
    # Example edge-case tests
    with pytest.raises(Exception):
        {fn}(...)"""
        return template
