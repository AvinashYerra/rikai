from reasoners.architecture_reasoner import analyze_architecture
from reasoners.execution_flow_reasoner import analyze_execution_flows
from reasoners.learning_module_reasoner import generate_learning_module
from reasoners.design_tradeoff_reasoner import analyze_design_tradeoffs
from reasoners.principles_reasoner import analyze_principles
from reasoners.risks_reasoner import analyze_risks
from reasoners.extension_reasoner import analyze_extensions
from reasoners.repo_context_reasoner import analyze_repo_context

def get_enriched_context(repo_url: str, repo_index: dict, repo_analysis: dict) -> dict:
    """
    Prepares the context required for all reasoning modules.
    """
    repo_context = analyze_repo_context(repo_url, repo_index)
    return {
        "repo_context": repo_context,
        "static_analysis": repo_analysis
    }

def run_module_reasoning(module_key: str, enriched_context: dict) -> any:
    """
    Runs a specific reasoning module based on the provided key.
    """
    modules = {
        "architecture": analyze_architecture,
        "execution_flows": analyze_execution_flows,
        "design_tradeoffs": analyze_design_tradeoffs,
        "engineering_principles": analyze_principles,
        "risks": analyze_risks,
        "extensions": analyze_extensions
    }
    
    if module_key in modules:
        return modules[module_key](enriched_context)
    return None

def run_reasoning(repo_url: str, repo_index: dict, repo_analysis: dict, callback=None) -> dict:
    """
    Runs a full 6-module reasoning pass (maintained for backward compatibility if needed).
    """
    def update_status(msg):
        if callback:
            callback(msg)

    update_status("Preparing context...")
    enriched_context = get_enriched_context(repo_url, repo_index, repo_analysis)

    results = {}
    
    module_configs = [
        ("architecture", "Module 1: Analyzing Architecture..."),
        ("execution_flows", "Module 2: Analyzing Execution Flows..."),
        ("design_tradeoffs", "Module 3: Inferring Design Tradeoffs..."),
        ("engineering_principles", "Module 4: Detecting Engineering Principles..."),
        ("risks", "Module 5: Identifying Risks & Technical Debt..."),
        ("extensions", "Module 6: Suggesting Extension Roadmap...")
    ]

    for key, status_msg in module_configs:
        update_status(status_msg)
        results[key] = run_module_reasoning(key, enriched_context)

    return results
