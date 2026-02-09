import streamlit as st
import json
from streamlit_agraph import agraph, Node, Edge, Config


def render_execution_flows(flow_data: dict):
    """
    Renders execution flow artifacts in Streamlit.

    Expected schema:
    {
        entry_points: [],
        execution_flows: [],
        async_or_background_tasks: {}
    }
    """

    if not flow_data:
        st.warning("No execution flow data available.")
        return

    # Handle string input (JSON)
    if isinstance(flow_data, str):
        try:
            flow_data = json.loads(flow_data)
        except json.JSONDecodeError:
            st.error("Failed to parse execution flow data.")
            st.code(flow_data)
            return

    st.header("Execution Intelligence")

    render_entry_points(flow_data.get("entry_points", []))
    render_flows(flow_data.get("execution_flows", []))
    render_async(flow_data.get("async_or_background_tasks", {}))


# -----------------------------
# ENTRY POINTS
# -----------------------------

def render_entry_points(entry_points):

    st.subheader("Entry Points")

    if not entry_points:
        st.info("No entry points detected.")
        return

    for ep in entry_points:
        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**{ep.get('id', 'unknown')}**")
                st.caption(ep.get("file", "unknown file"))

                if ep.get("symbol"):
                    st.code(ep["symbol"])

            with col2:
                confidence = ep.get("confidence", 0)
                st.metric("Confidence", f"{confidence:.2f}")


# -----------------------------
# FLOWS
# -----------------------------

def render_flows(flows):

    st.subheader("Execution Flows")

    if not flows:
        st.info("No flows detected.")
        return

    for flow in flows:

        with st.expander(f"{flow.get('name')} ({flow.get('type')})", expanded=True):

            st.write(flow.get("description", ""))

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Confidence",
                f"{flow.get('confidence', 0):.2f}"
            )

            col2.metric(
                "Complexity",
                flow.get("architectural_complexity", "unknown")
            )

            col3.metric(
                "Latency Risk",
                flow.get("latency_risk", "unknown")
            )

            if flow.get("nodes") and flow.get("edges"):
                render_graph(flow)

            if flow.get("branches"):
                render_branches(flow["branches"])

            if flow.get("failure_points"):
                st.warning("Failure Points:")
                for fp in flow["failure_points"]:
                    st.write(f"• {fp}")


# -----------------------------
# GRAPH
# -----------------------------

def render_graph(flow):

    st.markdown("### Flow Graph")

    nodes = []
    edges = []

    for node in flow["nodes"]:
        nodes.append(
            Node(
                id=node,
                label=node,
                size=25
            )
        )

    for edge in flow["edges"]:
        edges.append(
            Edge(
                source=edge["from"],
                target=edge["to"],
                label=edge.get("interaction", "")
            )
        )

    config = Config(
        width="100%",
        height=400,
        directed=True,
        physics=True,
        hierarchical=False
    )

    agraph(nodes=nodes, edges=edges, config=config)


# -----------------------------
# BRANCHING
# -----------------------------

def render_branches(branches):

    st.markdown("### Control Branching")

    for branch in branches:
        st.info(
            f"""
**Condition:** {branch.get('condition')}

From → To  
`{branch.get('from')}` → `{branch.get('to')}`
"""
        )


# -----------------------------
# ASYNC MODEL
# -----------------------------

def render_async(async_data):

    st.subheader("Execution Model")

    if not async_data:
        st.info("No async model detected.")
        return

    col1, col2 = st.columns(2)

    col1.metric(
        "Execution Model",
        async_data.get("execution_model", "unknown")
    )

    col2.metric(
        "Confidence",
        f"{async_data.get('confidence', 0):.2f}"
    )

    if async_data.get("detected_workers"):
        st.write("**Detected Workers:**")
        for worker in async_data["detected_workers"]:
            st.write(f"• {worker}")

    if async_data.get("notes"):
        st.write("**Notes:**")
        for note in async_data["notes"]:
            st.write(f"• {note}")

    if async_data.get("scaling_implication"):
        st.warning(
            f"Scaling Implication: {async_data['scaling_implication']}"
        )
