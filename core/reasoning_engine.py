from reasoners.architecture_reasoner import analyze_architecture
from reasoners.execution_flow_reasoner import analyze_execution_flows
# from reasoners.design_tradeoff_reasoner import analyze_design_tradeoffs
from reasoners.principles_reasoner import analyze_principles
# from reasoners.risks_reasoner import analyze_risks
from reasoners.extension_reasoner import analyze_extensions

def run_reasoning(repo_analysis: dict) -> dict:
    return {
        "architecture": analyze_architecture(repo_analysis),
        "execution_flows": analyze_execution_flows(repo_analysis),
        # "design_tradeoffs": analyze_design_tradeoffs(repo_analysis),
        "engineering_principles": analyze_principles(repo_analysis),
        # "risks_and_smells": analyze_risks(repo_analysis),
        "extensions": analyze_extensions(repo_analysis),
    }
