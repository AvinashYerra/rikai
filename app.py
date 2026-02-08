import streamlit as st
import json
import logging
import traceback
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize session state
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = {}
if "reasoning_output" not in st.session_state:
    st.session_state.reasoning_output = None

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
        
        #Phase 1
        dependencies = parse_requirements(path)
        project_type = classify_project(dependencies, files)
        entrypoints = detect_entrypoints(path)
        complexity = analyze_complexity(path)
        test_info = detect_tests(files)

        #Save Phase 1 Artifact
        analysis_path = save_repo_analysis(
            repo_path=path,
            project_type=project_type,
            dependencies=dependencies,
            entrypoints=entrypoints,
            complexity=complexity,
            test_info=test_info
        )

        st.session_state.analyzed = True
        st.session_state.analysis_data = {
            "path": path,
            "owner": owner,
            "repo": repo,
            "files": files,
            "index_path": index_path,
            "analysis_path": analysis_path,
            "project_type": project_type,
            "dependencies": dependencies,
            "entrypoints": entrypoints,
            "complexity": complexity,
            "test_info": test_info
        }

    if st.session_state.analyzed:
        data = st.session_state.analysis_data
        
        st.divider()
        st.header("Static Understanding")
        
        
        st.metric("Total files", len(data["files"]))
        st.subheader("Project Type")
        st.info(data["project_type"])
        

        st.subheader("Dependencies")
        st.write(data["dependencies"])

        st.subheader("Entry Points")
        st.write(data["entrypoints"] if data["entrypoints"] else "No clear entrypoints detected")

        st.subheader("Testing")
        if data["test_info"]["has_tests"]:
            st.success(f"{data['test_info']['test_file_count']} test files detected")
        else:
            st.warning("No tests detected")

        st.subheader("Most Complex Files")
        st.dataframe(
            sorted(
                data["complexity"],
                key=lambda x: x["cyclomatic_complexity"],
                reverse=True
            )[:10]
        )

        #Phase 2
        st.divider()
        st.header("Phase 2: Deep Reasoning (Gemini)")

        if st.button("Run Architectural Reasoning"):
            with st.spinner("Running multi-step reasoning using Gemini..."):
                try:
                    with open(data["analysis_path"]) as f:
                        repo_analysis = json.load(f)

                    logger.info(f"Starting reasoning for project at: {data['path']}")
                    reasoning_results = run_reasoning(repo_analysis)
                    
                    # Log the output for debugging
                    logger.info("Reasoning complete. Output received.")
                    logger.debug(f"Reasoning output: {json.dumps(reasoning_results, indent=2)}")
                    
                    reasoning_path = save_reasoning_output(data["path"], reasoning_results)
                    st.session_state.reasoning_output = reasoning_results
                    st.session_state.reasoning_path = reasoning_path
                    
                except Exception as e:
                    logger.error(f"Error during reasoning: {str(e)}")
                    logger.error(traceback.format_exc())
                    st.error(f"An error occurred during architectural reasoning: {str(e)}")
                    st.info("Check the terminal logs for more details.")

        if st.session_state.reasoning_output:
            output = st.session_state.reasoning_output
            # st.success(f"Reasoning output saved at {st.session_state.reasoning_path}")

            # Display Raw Output for developers
            with st.expander("Raw Reasoning Output (Debug)"):
                st.json(output)

            st.subheader("Architecture")
            st.json(output["architecture"])

            st.subheader("Execution Flows")
            st.json(output["execution_flows"])

            st.subheader("Engineering Principles")
            st.json(output["engineering_principles"])

            st.subheader("Extension Ideas")
            st.json(output["extensions"])

