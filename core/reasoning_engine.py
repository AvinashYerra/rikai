from reasoners.architecture_reasoner import analyze_architecture
from reasoners.execution_flow_reasoner import analyze_execution_flows
from reasoners.learning_module_reasoner import generate_learning_module
# from reasoners.design_tradeoff_reasoner import analyze_design_tradeoffs
from reasoners.principles_reasoner import analyze_principles
# from reasoners.risks_reasoner import analyze_risks
from reasoners.extension_reasoner import analyze_extensions
from reasoners.repo_context_reasoner import analyze_repo_context


def run_reasoning(repo_url: str, repo_index: dict, repo_analysis: dict) -> dict:
    repo_context = analyze_repo_context(repo_url, repo_index)

    enriched_context = {
        "repo_context": repo_context,
        "static_analysis": repo_analysis
    }

    return {
        "repo_context": repo_context,
        "learning_module": generate_learning_module(enriched_context),
        # "architecture": analyze_architecture(enriched_context),
        # "execution_flows": analyze_execution_flows(enriched_context),
        # "engineering_principles": analyze_principles(enriched_context),
        # "extensions": analyze_extensions(enriched_context),
    }

