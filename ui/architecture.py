import streamlit as st
import streamlit.components.v1 as components
import json

def render_mermaid(mermaid_code: str):
    """Renders a Mermaid diagram using HTML/JS."""
    html_code = f"""
    <div class="mermaid">
        {mermaid_code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
    </script>
    """
    components.html(html_code, height=600, scrolling=True)

def render_architecture_ui(architecture_data):
    """Renders components, flows, and boundaries in a structured UI."""
    if not architecture_data:
        st.info("No architecture data available.")
        return

    # Handle string input (JSON)
    if isinstance(architecture_data, str):
        try:
            architecture_data = json.loads(architecture_data)
        except json.JSONDecodeError:
            st.error("Failed to parse architecture data.")
            st.code(architecture_data)
            return

    # Components Section
    st.markdown("### 🧩 System Components")
    
    components_list = architecture_data.get("components", [])
    for comp in components_list:
        with st.container():
            st.markdown(f"""
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #00d4ff; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #00d4ff;">{comp.get('name', 'Unknown Component')}</h4>
                <p style="font-size: 14px; color: #cccccc;">{comp.get('description', '')}</p>
                <div style="margin-top: 10px;">
                    <span style="font-size: 12px; font-weight: bold; color: #888;">FILES:</span>
                    {' '.join([f'<code style="background: #333; padding: 2px 5px; border-radius: 3px; font-size: 11px;">{f}</code>' for f in comp.get('files', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Execution Flows Section (Integrated)
    flows = architecture_data.get("flows", [])
    if flows:
        st.markdown("### 🔄 Execution Flows")
        
        # Create Mermaid graph definition
        mermaid_code = "graph TD\n"
        
        # Add nodes and edges
        for flow in flows:
            # Flexible field access for schema updates
            source_name = flow.get("from") or flow.get("source") or "Start"
            dest_name = flow.get("to") or flow.get("destination") or "End"
            action_text = flow.get("description") or flow.get("action") or ""
            
            source_id = source_name.replace(" ", "_")
            dest_id = dest_name.replace(" ", "_")
            
            # Clean up action text for Mermaid (shorten if too long)
            clean_action = action_text[:50] + "..." if len(action_text) > 50 else action_text
            
            mermaid_code += f"    {source_id}[\"{source_name}\"] -- \"{clean_action}\" --> {dest_id}[\"{dest_name}\"]\n"

        # Add styling
        mermaid_code += """
        classDef default fill:#1e1e1e,stroke:#333,stroke-width:1px,color:#fff;
        classDef highlight fill:#00d4ff,stroke:#00d4ff,stroke-width:2px,color:#000;
        """
        
        render_mermaid(mermaid_code)
        
        # Also show as list for detail
        with st.expander("View Flow Details"):
            for flow in flows:
                s = flow.get("from") or flow.get("source") or "Start"
                d = flow.get("to") or flow.get("destination") or "End"
                a = flow.get("description") or flow.get("action") or ""
                st.markdown(f"**{s}** → **{d}**")
                st.caption(a)
                st.divider()

    # Boundaries Section
    if "boundaries" in architecture_data:
        st.markdown("### 🛡️ Architecture Boundaries")
        boundaries = architecture_data["boundaries"]
        cols = st.columns(len(boundaries)) if boundaries else []
        for i, boundary in enumerate(boundaries):
            with cols[i]:
                name = boundary.get("name") or boundary.get("type") or "Boundary"
                desc = boundary.get("description", "")
                st.markdown(f"""
                <div style="background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #444; height: 100%;">
                    <h5 style="margin-top: 0; color: #ff4b4b;">{name}</h5>
                    <p style="font-size: 13px;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
