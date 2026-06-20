#!/usr/bin/env python3
"""
FEL Framework: AST Invariant Shim
Programmatically extracts state-mutation points within legacy source code trees.
"""

import ast
import sys

class LegacyMutationArchaeologist(ast.NodeVisitor):
    def __init__(self):
        self.mutation_points = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id.isupper() or any(k in target.id for k in ["STATE", "DB", "GLOBAL"]):
                    self.mutation_points.append({"type": "State Mutation", "id": target.id, "line": node.lineno})
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if any(k in node.func.id.lower() for k in ["execute", "commit", "update", "write", "save"]):
                self.mutation_points.append({"type": "Implicit Call", "id": node.func.id, "line": node.lineno})
        self.generic_visit(node)

def audit_legacy_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    archaeologist = LegacyMutationArchaeologist()
    archaeologist.visit(tree)
    print(f"[FEL ARCHAEOLOGY] Found {len(archaeologist.mutation_points)} Boundary Intersections.")
    for p in archaeologist.mutation_points:
        print(f"  -> Line {p['line']}: [{p['type']}] targeting `{p['id']}`")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    audit_legacy_file(sys.argv[1])
