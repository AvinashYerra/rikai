import streamlit as st
import json
from utils.validators import parse_github_url
from core.repo_loader import clone_repo
from core.repo_filter import build_ignore_spec
from core.repo_indexer import index_repository
from utils.json_writer import save_repo_index
from core.dependency_parser import parse_requirements
from core.project_classifier import classify_project
from core.entrypoint_detector import detect_entrypoints
from core.complexity_analyzer import analyze_complexity
from core.test_detector import detect_tests
from utils.analysis_writer import save_repo_analysis
from core.reasoning_engine import run_reasoning
from utils.reasoning_writer import save_reasoning_output


st.set_page_config(layout="wide")
st.title("Repo Learning Engine")

url = st.text_input("Paste GitHub repository URL")

if url:
    parsed = parse_github_url(url)

    if not parsed:
        st.error("Invalid GitHub repository URL")
        st.stop()

    owner, repo = parsed

    if st.button("Analyze Repository"):
        #Phase 0
        path = clone_repo(owner, repo)
        st.success(f"Repository cloned at {path}")

        ignore_spec = build_ignore_spec()
        files = index_repository(path, ignore_spec)

        index_path = save_repo_index(path, owner, repo, files)

        st.metric("Total files", len(files))
        st.success(f"Repo index saved at {index_path}")

        #Phase 1
        st.divider()
        st.header("Static Understanding")

        dependencies = parse_requirements(path)
        project_type = classify_project(dependencies, files)
        entrypoints = detect_entrypoints(path)
        complexity = analyze_complexity(path)
        test_info = detect_tests(files)

        st.subheader("Project Type")
        st.info(project_type)

        st.subheader("Dependencies")
        st.write(dependencies)

        st.subheader("Entry Points")
        st.write(entrypoints if entrypoints else "No clear entrypoints detected")

        st.subheader("Testing")
        if test_info["has_tests"]:
            st.success(f"{test_info['test_file_count']} test files detected")
        else:
            st.warning("No tests detected")

        st.subheader("Most Complex Files")
        st.dataframe(
            sorted(
                complexity,
                key=lambda x: x["cyclomatic_complexity"],
                reverse=True
            )[:10]
        )

        #Save Phase 1 Artifact
        analysis_path = save_repo_analysis(
            repo_path=path,
            project_type=project_type,
            dependencies=dependencies,
            entrypoints=entrypoints,
            complexity=complexity,
            test_info=test_info
        )
        st.success(f"Repo analysis saved at {analysis_path}")

        #Phase 2
        st.divider()
        st.header("Phase 2: Deep Reasoning (Gemini)")

        if st.button("Run Architectural Reasoning"):
            with st.spinner("Running multi-step reasoning using Gemini..."):
                with open(analysis_path) as f:
                    repo_analysis = json.load(f)

                reasoning_output = run_reasoning(repo_analysis)
                reasoning_path = save_reasoning_output(path, reasoning_output)

            st.success(f"Reasoning output saved at {reasoning_path}")

            st.subheader("Architecture")
            st.json(reasoning_output["architecture"])

            st.subheader("Execution Flows")
            st.json(reasoning_output["execution_flows"])

            st.subheader("Engineering Principles")
            st.json(reasoning_output["engineering_principles"])

            st.subheader("Extension Ideas")
            st.json(reasoning_output["extensions"])

