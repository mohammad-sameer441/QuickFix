from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os

from engine.predictor import PredictiveCodeIntelligenceEngine
from engine.localizer import SemanticBugLocalizer
from engine.repairer import AutomatedProgramRepairer
from engine.validator import PatchValidator

app = FastAPI(
    title="QuickFix AI Engine",
    description="Predictive Code Intelligence, Semantic Bug Localization & Automated Program Repair",
    version="1.0.0"
)

# Enable CORS for all frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core AI Engines
predictor = PredictiveCodeIntelligenceEngine()
localizer = SemanticBugLocalizer()
repairer = AutomatedProgramRepairer()
validator = PatchValidator()

# Request Models
class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code snippet or file contents")
    language: str = Field(default="python", description="Programming language")
    filename: Optional[str] = Field(default="main.py", description="Relative filename")
    api_key: Optional[str] = Field(default=None, description="Optional Gemini/OpenAI API key for extended LLM reasoning")

class RepairRequest(BaseModel):
    code: str
    vulnerability: Dict[str, Any]
    language: str = "python"

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "AegisCode Engine",
        "version": "1.0.0",
        "capabilities": [
            "Predictive Defect Intelligence",
            "Semantic Bug Localization",
            "Logical Vulnerability Identification",
            "Automated Program Repair (APR)",
            "Synthetic Unit Test Validation"
        ]
    }

@app.post("/api/predict")
def predict_defects(payload: CodeAnalysisRequest):
    """Calculates defect risk score, cyclomatic complexity, and risk factors."""
    result = predictor.analyze_source(payload.code, payload.language)
    return {"success": True, "data": result}

@app.post("/api/localize")
def localize_bugs(payload: CodeAnalysisRequest):
    """Localizes semantic and logical bugs, returning exact line numbers and root causes."""
    vulnerabilities = localizer.localize_vulnerabilities(payload.code, payload.language, payload.api_key)
    return {"success": True, "count": len(vulnerabilities), "vulnerabilities": vulnerabilities}

@app.post("/api/repair")
def repair_program(payload: RepairRequest):
    """Generates unified git diff patch and synthetic verification unit test."""
    repair_result = repairer.generate_repair(payload.code, payload.vulnerability, payload.language)
    validation = validator.validate_patch(
        payload.code,
        repair_result["repaired_code"],
        repair_result["synthetic_unit_test"]
    )
    repair_result["validation"] = validation
    return {"success": True, "data": repair_result}

@app.post("/api/full-analysis")
def full_pipeline(payload: CodeAnalysisRequest):
    """Runs the entire end-to-end pipeline in a single call."""
    # 1. Predict
    prediction = predictor.analyze_source(payload.code, payload.language)
    
    # 2. Localize
    vulnerabilities = localizer.localize_vulnerabilities(payload.code, payload.language, payload.api_key)
    
    # 3. Repair top vulnerability if found
    repairs = []
    for vuln in vulnerabilities:
        rep = repairer.generate_repair(payload.code, vuln, payload.language, api_key=payload.api_key)
        val = validator.validate_patch(payload.code, rep["repaired_code"], rep["synthetic_unit_test"])
        rep["validation"] = val
        repairs.append(rep)

    return {
        "success": True,
        "prediction": prediction,
        "vulnerabilities": vulnerabilities,
        "repairs": repairs
    }

@app.get("/api/benchmarks")
def get_benchmarks():
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    benchmarks = []
    
    file_map = {
        "race_condition.py": {
            "title": "E-Commerce Race Condition (Double-Spend)",
            "category": "Concurrency & State Atomicity",
            "severity": "CRITICAL"
        },
        "sqli.py": {
            "title": "SQL Injection in User Authentication Query",
            "category": "Data Sanitization & Injection (CWE-89)",
            "severity": "CRITICAL"
        },
        "auth_bypass.py": {
            "title": "Broken Object Authorization (IDOR)",
            "category": "Access Control & Security Logic (CWE-639)",
            "severity": "HIGH"
        },
        "resource_leak.py": {
            "title": "Unclosed File Descriptor & Resource Leak",
            "category": "Resource Management & Exhaustion (CWE-775)",
            "severity": "MODERATE"
        },
        "null_deref.py": {
            "title": "Missing Null / NoneType Check on DB Result",
            "category": "Runtime Exception (CWE-476)",
            "severity": "HIGH"
        },
        "mutable_defaults.py": {
            "title": "State Leakage via Mutable Default Arguments",
            "category": "Interpreter State Defect (CWE-665)",
            "severity": "MODERATE"
        },
        "weak_crypto.py": {
            "title": "Insecure Hashing with Deprecated MD5",
            "category": "Cryptographic Flaw (CWE-328)",
            "severity": "HIGH"
        },
        "off_by_one.py": {
            "title": "Off-By-One Slice & Boundary Overflow",
            "category": "Boundary Condition Violation (CWE-193)",
            "severity": "MODERATE"
        }
    }

    for filename, meta in file_map.items():
        filepath = os.path.join(samples_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                code_content = f.read()
            benchmarks.append({
                "id": filename,
                "title": meta["title"],
                "category": meta["category"],
                "severity": meta["severity"],
                "code": code_content
            })

    return {"benchmarks": benchmarks}

# Mount Root Static Web Application
from fastapi.responses import FileResponse

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@app.get("/")
def serve_index():
    index_file = os.path.join(root_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "AegisCode Engine Active. Open index.html directly or from root."}

@app.get("/styles.css")
def serve_styles():
    return FileResponse(os.path.join(root_dir, "styles.css"), media_type="text/css")

@app.get("/app.js")
def serve_js():
    return FileResponse(os.path.join(root_dir, "app.js"), media_type="application/javascript")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
