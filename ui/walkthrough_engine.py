import streamlit as st
import json
from ui.architecture import render_mermaid
from reasoners.architecture_tour_reasoner import analyze_architecture_tour

def render_walkthrough_engine(analysis_data: dict):
    """
    Renders the Interactive Architecture Walkthrough UI.
    """
    st.markdown("## 🧭 Interactive Architecture Walkthrough")
    st.markdown("Let Gemini lead you on a guided tour of how this system works, step-by-step.")

    # 1. Configuration & Start
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Detect primary flow (default to "Main Request Flow")
        flow_options = ["Main Request Flow", "Data Ingestion Pipeline", "Authentication Lifecycle", "Background Processing"]
        selected_flow = st.selectbox("Select a flow to explore:", flow_options)
    
    with col2:
        beginner_mode = st.toggle("🍼 New Contributor Mode", help="Simplifies explanations for onboarding.")

    # 2. State Management for the Tour
    if "tour_data" not in st.session_state or st.session_state.get("current_flow") != selected_flow:
        if st.button("🚀 Start Guided Tour"):
            with st.spinner("Gemini is preparing your architectural tour..."):
                wisdom = st.session_state.get("reasoning_output", {})
                context = {
                    "static_analysis": analysis_data,
                    "architectural_wisdom": wisdom.get("architecture") if wisdom else "Not analyzed yet"
                }
                
                try:
                    tour_json = analyze_architecture_tour(context, selected_flow, beginner_mode)
                    tour_data = json.loads(tour_json)
                    st.session_state.tour_data = tour_data
                    st.session_state.tour_step = 0
                    st.session_state.current_flow = selected_flow
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating tour: {e}")
                    return

    # 3. Render the Active Tour
    if "tour_data" in st.session_state:
        tour = st.session_state.tour_data
        steps = tour.get("steps", [])
        current_idx = st.session_state.get("tour_step", 0)
        
        if not steps:
            st.info("No steps generated for this flow.")
            return

        current_step = steps[current_idx]
        
        # Navigation Header
        c1, c2, c3 = st.columns([1, 4, 1])
        with c1:
            if st.button("⬅️ Back", disabled=current_idx == 0):
                st.session_state.tour_step -= 1
                st.rerun()
        with c2:
            st.progress((current_idx + 1) / len(steps), text=f"Step {current_idx + 1} of {len(steps)}: {current_step.get('title')}")
        with c3:
            if current_idx < len(steps) - 1:
                if st.button("Next ➡️"):
                    st.session_state.tour_step += 1
                    st.rerun()
            else:
                if st.button("🏁 Finish"):
                    del st.session_state.tour_data
                    st.rerun()

        # Visual Context (Highlighted Mermaid)
        st.divider()
        st.markdown("### 🗺️ Visual Progression")
        
        # Modify the graph definition to highlight the current step
        base_graph = tour.get("graph_definition", "graph TD")
        current_visual_id = current_step.get("visual_id")
        
        if current_visual_id:
            # Simple highlight style
            highlight_style = f"\nstyle {current_visual_id} fill:#00d4ff,stroke:#00d4ff,stroke-width:4px,color:#000;"
            final_graph = base_graph + highlight_style
        else:
            final_graph = base_graph
            
        render_mermaid(final_graph)

        # Narration Content
        st.divider()
        nc1, nc2 = st.columns([2, 1])
        
        with nc1:
            st.markdown(f"### 🎙️ {current_step.get('title')}")
            st.markdown(f"**Location:** `{current_step.get('file')}`")
            st.info(current_step.get("narration"))
        
        with nc2:
            st.markdown("#### 💡 Why This Matters")
            st.write(current_step.get("rationale"))
            
            if st.button("🔍 Explore File", help="Jump to file details"):
                st.toast(f"Opening {current_step.get('file')}...")
                # Note: Real file jumping would require more UI integration

        if st.button("🛑 Stop Tour"):
            del st.session_state.tour_data
            st.rerun()
