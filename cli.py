# cli.py
import argparse
from inference import CodeExplainViz

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Path to python file with a function")
    parser.add_argument("--code", type=str, help="Code string to explain")
    parser.add_argument("--model", type=str, default="Salesforce/codet5-small", help="Model path or HF name")
    args = parser.parse_args()

    code = None
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    elif args.code:
        code = args.code
    else:
        print("Provide --file or --code")
        return

    explainer = CodeExplainViz(model_name_or_path=args.model)
    out = explainer.explain(code)
    print("\n--- Short Explanation ---\n")
    print(out["short"])
    print("\n--- Detailed Explanation ---\n")
    print(out["detailed"])
    print("\n--- Mermaid Flowchart (copy into mermaid live editor) ---\n")
    print(out["mermaid"])
    print("\n--- Unit test template ---\n")
    print(out["unit_tests"])

if __name__ == "__main__":
    main()
