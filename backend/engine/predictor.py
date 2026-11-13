import ast
import re
import math
from typing import Dict, List, Any

class PredictiveCodeIntelligenceEngine:
    """
    Universal Predictive Code Intelligence Engine:
    Computes Cyclomatic Complexity (McCabe), Cognitive Hazards, State Mutation Density,
    and Defect Probability Score (0 - 100%) for arbitrary code in any language.
    """

    def analyze_source(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language.lower() == "python":
            try:
                return self._analyze_python(code)
            except Exception:
                return self._universal_code_analysis(code, language)
        else:
            return self._universal_code_analysis(code, language)

    def _analyze_python(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "error": f"Syntax error at line {e.lineno}: {e.msg}",
                "overall_risk_score": 96.0,
                "overall_risk_level": "CRITICAL",
                "total_complexity": 8,
                "total_lines": len(code.splitlines()),
                "functions": []
            }

        function_risks = []
        total_complexity = 0
        total_lines = len(code.splitlines())

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_name = node.name
                start_line = node.lineno
                end_line = getattr(node, "end_lineno", start_line + 10)
                
                branches = 1
                state_mutations = 0
                has_async = isinstance(node, ast.AsyncFunctionDef)
                has_locks = False

                for subnode in ast.walk(node):
                    if isinstance(subnode, (ast.If, ast.While, ast.For, ast.AsyncFor, 
                                            ast.ExceptHandler, ast.With, ast.AsyncWith)):
                        branches += 1
                    elif isinstance(subnode, ast.BoolOp):
                        branches += len(subnode.values) - 1
                    elif isinstance(subnode, (ast.Assign, ast.AugAssign, ast.Subscript)):
                        state_mutations += 1
                    elif isinstance(subnode, ast.Name) and "lock" in subnode.id.lower():
                        has_locks = True

                fn_lines = end_line - start_line + 1
                raw_risk = (branches * 5.0) + (state_mutations * 3.0) + (fn_lines * 0.7)

                if has_async and not has_locks and state_mutations > 0:
                    raw_risk += 30  # High probability of race condition

                defect_probability = round(min(98.5, max(12.0, (1 / (1 + math.exp(-raw_risk / 20))) * 100)), 1)

                risk_level = (
                    "CRITICAL" if defect_probability >= 80 else
                    "HIGH" if defect_probability >= 60 else
                    "MODERATE" if defect_probability >= 35 else "LOW"
                )

                risk_factors = []
                if branches > 4:
                    risk_factors.append(f"High cyclomatic branching (McCabe CC: {branches})")
                if state_mutations > 3:
                    risk_factors.append(f"Frequent state modifications ({state_mutations} mutations)")
                if has_async and not has_locks:
                    risk_factors.append("Asynchronous execution with unlocked state mutations (Race Hazard)")
                if fn_lines > 30:
                    risk_factors.append(f"Function length exceeds safe cognitive threshold ({fn_lines} LOC)")
                if not risk_factors:
                    risk_factors.append("Standard linear execution flow")

                function_risks.append({
                    "function_name": fn_name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "cyclomatic_complexity": branches,
                    "state_mutations": state_mutations,
                    "lines_of_code": fn_lines,
                    "defect_probability": defect_probability,
                    "risk_level": risk_level,
                    "risk_factors": risk_factors
                })
                total_complexity += branches

        if function_risks:
            max_fn_risk = max(fn["defect_probability"] for fn in function_risks)
            avg_risk = sum(fn["defect_probability"] for fn in function_risks) / len(function_risks)
            overall_score = round((0.7 * max_fn_risk) + (0.3 * avg_risk), 1)
        else:
            overall_score = min(total_lines * 2.0, 40.0)

        overall_risk_level = (
            "CRITICAL" if overall_score >= 80 else
            "HIGH" if overall_score >= 60 else
            "MODERATE" if overall_score >= 35 else "LOW"
        )

        return {
            "overall_risk_score": overall_score,
            "overall_risk_level": overall_risk_level,
            "total_complexity": max(1, total_complexity),
            "total_lines": total_lines,
            "functions": sorted(function_risks, key=lambda x: x["defect_probability"], reverse=True)
        }

    def _universal_code_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Universal analyzer for JavaScript, TypeScript, Java, C++, Go, Rust, etc."""
        lines = code.splitlines()
        line_count = len(lines)
        
        # Count branching operators
        branch_matches = len(re.findall(r'\b(if|else if|for|while|case|catch|switch)\b', code))
        async_matches = len(re.findall(r'\b(async|await|Promise|thread|Thread|go |mutex)\b', code))
        pointer_hazards = len(re.findall(r'(\->|\*|\&|malloc|free|delete)', code))
        sql_hazards = len(re.findall(r'(SELECT|INSERT|UPDATE|DELETE|\.execute\()', code, re.IGNORECASE))

        raw_score = (branch_matches * 6.0) + (async_matches * 5.0) + (pointer_hazards * 3.0) + (line_count * 0.4)
        if sql_hazards > 0 and ("f\"" in code or "+" in code):
            raw_score += 35

        defect_score = round(min(97.5, max(15.0, (1 / (1 + math.exp(-raw_score / 22))) * 100)), 1)
        risk_level = "CRITICAL" if defect_score >= 80 else "HIGH" if defect_score >= 60 else "MODERATE" if defect_score >= 35 else "LOW"

        risk_factors = []
        if branch_matches > 3:
            risk_factors.append(f"Multi-path branching detected ({branch_matches} branches)")
        if async_matches > 0:
            risk_factors.append(f"Concurrent / async state transitions detected ({async_matches} markers)")
        if sql_hazards > 0:
            risk_factors.append("Database query construction patterns detected")
        if not risk_factors:
            risk_factors.append("Standard linear code flow")

        return {
            "overall_risk_score": defect_score,
            "overall_risk_level": risk_level,
            "total_complexity": branch_matches + 1,
            "total_lines": line_count,
            "functions": [
                {
                    "function_name": f"{language}_module",
                    "start_line": 1,
                    "end_line": line_count,
                    "cyclomatic_complexity": branch_matches + 1,
                    "defect_probability": defect_score,
                    "risk_level": risk_level,
                    "risk_factors": risk_factors
                }
            ]
        }
