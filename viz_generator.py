# viz_generator.py
import ast

class VizBuilder(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.counter = 0

    def new_id(self, prefix="n"):
        self.counter += 1
        return f"{prefix}{self.counter}"

    def add_node(self, nid, label):
        label = label.replace("\n", "\\n").replace('"', '\\"')
        self.nodes.append((nid, label))

    def add_edge(self, a, b, label=""):
        self.edges.append((a, b, label))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        start = self.new_id("start")
        self.add_node(start, f"def {node.name}(...)")
        prev = start
        for stmt in node.body:
            cur = self.visit(stmt)
            if cur:
                self.add_edge(prev, cur)
                prev = cur
        return start

    def visit_Return(self, node: ast.Return):
        nid = self.new_id("ret")
        val = ast.unparse(node.value) if node.value else ""
        self.add_node(nid, f"return {val}")
        return nid

    def visit_Raise(self, node: ast.Raise):
        nid = self.new_id("raise")
        exc = ast.unparse(node.exc) if node.exc else ""
        self.add_node(nid, f"raise {exc}")
        return nid

    def visit_For(self, node: ast.For):
        nid = self.new_id("for")
        target = ast.unparse(node.target)
        iter_ = ast.unparse(node.iter)
        self.add_node(nid, f"for {target} in {iter_}")
        prev = nid
        for stmt in node.body:
            cur = self.visit(stmt)
            if cur:
                self.add_edge(prev, cur)
                prev = cur
        return nid

    def visit_While(self, node: ast.While):
        nid = self.new_id("while")
        cond = ast.unparse(node.test)
        self.add_node(nid, f"while {cond}")
        prev = nid
        for stmt in node.body:
            cur = self.visit(stmt)
            if cur:
                self.add_edge(prev, cur)
                prev = cur
        return nid

    def visit_If(self, node: ast.If):
        nid = self.new_id("if")
        cond = ast.unparse(node.test)
        self.add_node(nid, f"if {cond}")
        for stmt in node.body:
            cur = self.visit(stmt)
            if cur:
                self.add_edge(nid, cur, label="true")
        if node.orelse:
            for stmt in node.orelse:
                cur = self.visit(stmt)
                if cur:
                    self.add_edge(nid, cur, label="false")
        return nid

    def visit_Expr(self, node: ast.Expr):
        nid = self.new_id("expr")
        txt = ast.unparse(node.value)
        self.add_node(nid, txt)
        return nid

    def visit_Assign(self, node: ast.Assign):
        nid = self.new_id("assign")
        targets = ", ".join([ast.unparse(t) for t in node.targets])
        val = ast.unparse(node.value)
        self.add_node(nid, f"{targets} = {val}")
        return nid

    def generic_visit(self, node):
        super().generic_visit(node)
        return None

def code_to_mermaid(code: str) -> str:
    tree = ast.parse(code)
    vb = VizBuilder()
    root_id = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            root_id = vb.visit(node)
            break
    lines = ["flowchart TD"]
    for nid, label in vb.nodes:
        lines.append(f'    {nid}["{label}"]')
    for a, b, lbl in vb.edges:
        if lbl:
            lines.append(f'    {a} -->|{lbl}| {b}')
        else:
            lines.append(f'    {a} --> {b}')
    return "\n".join(lines)
