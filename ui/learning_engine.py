import streamlit as st
import json
from core.reasoning_engine import get_enriched_context, run_module_reasoning
from ui.architecture import render_architecture_ui
from ui.execution_flows import render_execution_flows

def render_learning_engine(repo_data: dict):
    """
    Renders the 6-module learning experience with lazy loading.
    """
    st.markdown("## Learn This Repo")
    st.markdown("Explore the codebase through 6 specialized reasoning modules.")

    # Shared Context Preparation
    if "enriched_context" not in st.session_state:
        if st.button("Understand in detail"):
            with st.spinner("Gemini is building a semantic map of the repo..."):
                try:
                    # Load the analysis data
                    with open(repo_data["analysis_path"]) as f:
                        repo_analysis = json.load(f)
                    
                    st.session_state.enriched_context = get_enriched_context(
                        f"https://github.com/{repo_data['owner']}/{repo_data['repo']}",
                        repo_data["files"],
                        repo_analysis
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"Error preparing context: {e}")
            return
        else:
            st.info("Click the button above to start the deep reasoning process. This prepares the common context for all modules.")
            return

    # Initialize reasoning output if not exists
    if "reasoning_output" not in st.session_state or st.session_state.reasoning_output is None:
        st.session_state.reasoning_output = {}

    # Define Tabs
    tabs = st.tabs([
        "Architecture",
        "Execution Flows",
        "Design Tradeoffs",
        "Principles",
        "Risks & Smells",
        "Extension Roadmap"
    ])

    module_mapping = [
        ("architecture", tabs[0], "Architecture"),
        ("execution_flows", tabs[1], "Execution Flows"),
        ("design_tradeoffs", tabs[2], "Design Decisions"),
        ("engineering_principles", tabs[3], "Principles"),
        ("risks", tabs[4], "Risks & Smells"),
        ("extensions", tabs[5], "Extension Roadmap")
    ]

    for key, tab, label in module_mapping:
        with tab:
            render_module_with_lazy_load(key, label, repo_data)

def render_module_with_lazy_load(key, label, repo_data):
    """
    Helper to render a module if it exists, otherwise show the unlock trigger.
    """
    output = st.session_state.reasoning_output
    
    if key in output and output[key]:
        st.markdown(f"### {label}")
        
        # Specific Rendering Logic
        if key == "architecture":
            render_architecture_ui(output[key])
        elif key == "execution_flows":
            render_execution_flows(output[key])
        elif key == "design_tradeoffs":
            render_tradeoffs_ui(output[key])
        elif key == "engineering_principles":
            render_principles_ui(output[key])
        elif key == "risks":
            render_risks_ui(output[key])
        elif key == "extensions":
            render_extensions_ui(output[key])
            
        if st.button(f"Refresh {label}", key=f"refresh_{key}"):
            del st.session_state.reasoning_output[key]
            st.rerun()
    else:
        st.markdown(f"""
        <div style="padding: 2rem; border-radius: 10px; border: 1px dashed #444; text-align: center; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(5px);">
            <h4>{label} Module is Locked</h4>
            <p style="font-size: 0.9rem; color: #aaa;">Reason over the code to unlock this specific piece of repository wisdom.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Unlock {label}", key=f"unlock_{key}"):
            with st.spinner(f"Gemini is reasoning about {label.lower()}..."):
                try:
                    result = run_module_reasoning(key, st.session_state.enriched_context)
                    st.session_state.reasoning_output[key] = result
                    st.rerun()
                except Exception as e:
                    if "503" in str(e):
                        st.error("Gemini is currently overloaded. Please try again in 30 seconds.")
                    else:
                        st.error(f"Error unlocking {label}: {e}")

# --- UI Renderers for individual modules (updated with aesthetics) ---

def render_tradeoffs_ui(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    st.markdown("#### Design Decisions & Inferred Rationale")
    for decision in data.get("decisions", []):
        with st.expander(f"{decision['decision']}"):
            st.markdown(f"**Rationale:** {decision['rationale']}")
            st.markdown(f"**Tradeoff:** {decision['tradeoff']}")
            st.caption(f"Confidence: {decision['confidence']}/10")

def render_principles_ui(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        score = data.get("consistency_score", 0)
        st.metric("Internal Consistency", f"{score}/100")
        
    st.markdown("#### Principles in Practice")
    for p in data.get("principles", []):
        st.markdown(f"**{p['principle']}**: {p['implementation']}")
        st.markdown("---")

def render_risks_ui(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    st.warning("Detected Code Smells & Potential Risks")
    for risk in data.get("risks", []):
        with st.container():
            st.markdown(f"**{risk['area']}** ({risk['risk_level'].upper()})")
            st.write(risk['issue'])
            st.info(f"Refactoring Suggestion: {risk['suggestion']}")
            st.divider()

def render_extensions_ui(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    st.markdown("#### System Evolution Roadmap")
    for ext in data.get("roadmap", []):
        with st.expander(f"{ext['feature']}"):
            st.write(ext['description'])
            st.markdown(f"**Effort:** {ext['effort']} | **Impact:** {ext['impact']}")
            st.markdown(f"**Difficulty:** {ext['difficulty']}")
