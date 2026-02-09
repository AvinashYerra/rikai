import streamlit as st
import time
import json
from core.repo_loader import clone_repo
from core.structure import get_repo_summary, generate_file_tree, render_ascii_tree
from utils.validators import parse_github_url

# Analysis imports
from core.repo_filter import build_ignore_spec
from core.repo_indexer import index_repository
from utils.json_writer import save_repo_index
from core.dependency_parser import parse_requirements
from core.project_classifier import classify_project
from core.entrypoint_detector import detect_entrypoints
from core.complexity_analyzer import analyze_complexity
from core.test_detector import detect_tests
from utils.analysis_writer import save_repo_analysis

def render_sidebar():
    """Renders the sidebar with repo input, loads repo, runs analysis, and shows summary."""
    st.sidebar.title("🧩 Rikai")
    st.sidebar.markdown("---")
    
    # Persistent Input
    url = st.sidebar.text_input("GitHub Repository URL", key="repo_url_input")
    
    # Determine if we need to load/reload
    if url:
        parsed = parse_github_url(url)
        if not parsed:
            st.sidebar.error("Invalid GitHub URL")
        else:
            owner, repo = parsed
            repo_id = f"{owner}/{repo}"
            
            # Check if we need to load this specific repo (if it's new or not yet analyzed)
            if st.session_state.get("current_repo_id") != repo_id or not st.session_state.get("analyzed"):
                
                with st.sidebar.status("Loading & Analyzing...", expanded=True) as status:
                    try:
                        # 1. Clone
                        st.write("Cloning repository...")
                        path = clone_repo(owner, repo)
                        st.session_state.current_repo_path = path
                        st.session_state.current_repo_id = repo_id
                        
                        # 2. Structure & Index
                        st.write("Indexing files...")
                        ignore_spec = build_ignore_spec()
                        files = index_repository(path, ignore_spec)
                        index_path = save_repo_index(path, owner, repo, files)
                        
                        # 3. Analysis (Phase 1)
                        st.write("Analyzing dependencies & complexity...")
                        dependencies = parse_requirements(path)
                        project_type = classify_project(dependencies, files)
                        entrypoints = detect_entrypoints(path)
                        complexity = analyze_complexity(path)
                        test_info = detect_tests(files)
                        
                        # 4. Save Artifacts
                        analysis_path = save_repo_analysis(
                            repo_path=path,
                            project_type=project_type,
                            dependencies=dependencies,
                            entrypoints=entrypoints,
                            complexity=complexity,
                            test_info=test_info
                        )
                        
                        # 5. Additional Metadata (for sidebar)
                        repo_stats = get_repo_summary(path)
                        file_tree = generate_file_tree(path)
                        ascii_tree = render_ascii_tree(file_tree)

                        # 6. Update Session State
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
                            "test_info": test_info,
                            "repo_stats": repo_stats,
                            "file_tree": file_tree,
                            "ascii_tree": ascii_tree
                        }
                        
                        status.update(label="Repository Global & Loaded!", state="complete", expanded=False)
                        st.rerun() 
                        
                    except Exception as e:
                        st.sidebar.error(f"Error loading repo: {e}")
                        st.session_state.analyzed = False
                        st.stop()
                        
    # Analysis Summary Presenter (only if loaded)
    if st.session_state.get("analyzed") and st.session_state.get("analysis_data"):
        data = st.session_state.analysis_data
        stats = data.get("repo_stats", {})
        
        st.sidebar.markdown("### 📊 Repo Summary")
        
        # Key Metrics
        c1, c2 = st.sidebar.columns(2)
        c1.metric("Files", stats.get("file_count", 0))
        c2.metric("Size", f"{stats.get('total_size_bytes', 0)/1024:.0f}KB")
        
        st.sidebar.markdown(f"**Language:** {stats.get('main_language', 'Unknown')}")
        st.sidebar.markdown(f"**Type:** {data.get('project_type', 'Unknown')}")
        
        # Testing status
        test_info = data.get("test_info", {})
        if test_info.get("has_tests"):
            st.sidebar.success(f"✅ Tests Detected ({test_info.get('test_file_count')} files)")
        else:
            st.sidebar.warning("⚠️ No tests detected")
            
        # Entrypoints
        eps = data.get("entrypoints", [])
        if eps:
            with st.sidebar.expander("🚪 Entry Points"):
                for ep in eps:
                    st.code(ep, language="text")

        # Dependencies
        deps = data.get("dependencies", [])
        if deps:
            with st.sidebar.expander("📦 Dependencies"):
                st.write(", ".join(deps[:20]) + ("..." if len(deps)>20 else ""))

        # Complexity
        complexity = data.get("complexity", [])
        if complexity:
            with st.sidebar.expander("📉 Complex Files"):
                sorted_comp = sorted(complexity, key=lambda x: x["cyclomatic_complexity"], reverse=True)[:5]
                for item in sorted_comp:
                    st.caption(f"{item['path']} (CC: {item['cyclomatic_complexity']})")

        # File Tree
        ascii_tree = data.get("ascii_tree", "")
        if ascii_tree:
            with st.sidebar.expander("📂 File Tree", expanded=True):
                st.code(ascii_tree, language="text")

    elif not url:
        st.session_state.analyzed = False
        st.sidebar.info("👈 Paste a GitHub URL to start analysis.")
