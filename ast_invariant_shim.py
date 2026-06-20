#!/usr/bin/env python3
"""
FEL Framework: AST Invariant Shim
Forensic tool to programmatically isolate data-mutation points within legacy sources.
Bypasses manual code reading by treating the application as an AST map.
"""

import ast
import sys

class LegacyMutationArchaeologist(ast.NodeVisitor):
    def __init__(self):
        self.mutation_points = []

    def visit_Assign(self, node):
        """Track variable state modifications."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Isolate specific global or state-heavy conventions
                if target.id.isupper() or "STATE" in target.id or "DB" in target.id:
                    self.mutation_points.append({
                        "type": "State Assignment",
                        "identifier": target.id,
                        "line": node.lineno
                    })
        self.generic_visit(node)

    def visit_Call(self, node):
        """Track database, raw socket, or side-effect heavy execution calls."""
        if isinstance(node.func, ast.Name):
            if any(keyword in node.func.id.lower() for keyword in ["execute", "commit", "update", "write", "save"]):
                self.mutation_points.append({
                    "type": "Implicit Data Mutation Call",
                    "identifier": node.func.id,
                    "line": node.lineno
                })
        elif isinstance(node.func, ast.Attribute):
            if any(keyword in node.func.attr.lower() for keyword in ["execute", "commit", "update", "write", "save"]):
                self.mutation_points.append({
                    "type": "Object Method Mutation Call",
                    "identifier": node.func.attr,
                    "line": node.lineno
                })
        self.generic_visit(node)

def audit_legacy_file(filepath: str):
    print(f"[FEL ARCHAEOLOGY] Commencing automated excavation on: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        
        tree = ast.parse(source)
        archaeologist = LegacyMutationArchaeologist()
        archaeologist.visit(tree)
        
        print(f"\n[FOUND] {len(archaeologist.mutation_points)} Structural Boundary Intersections:")
        for point in archaeologist.mutation_points:
            print(f"  -> Line {point['line']}: [{point['type']}] targeting symbol `{point['identifier']}`")
            
    except Exception as e:
        print(f"[ERROR] Excavation halted due to syntax anomalies: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ast_invariant_shim.py <path_to_legacy_file.py>")
        sys.exit(1)
    audit_legacy_file(sys.argv[1])
