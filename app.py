import streamlit as st
import json
import logging
import traceback

from ui.sidebar import render_sidebar
from ui.learning_engine import render_learning_engine
from ui.pr_reviewer import render_pr_reviewer
from ui.walkthrough_engine import render_walkthrough_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize session state variables if they don't exist
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = {}
if "reasoning_output" not in st.session_state:
    st.session_state.reasoning_output = None

st.set_page_config(
    page_title="Rikai | Repo Learning Engine",
    layout="wide",
    page_icon="🧩",
    initial_sidebar_state="expanded"
)

# --- Premium Global CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@400;500;600;700&display=swap');

    :root {
        --text-size-base: 0.9rem;
        --text-size-small: 0.8rem;
        --text-size-header: 1.2rem;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: var(--text-size-base);
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600 !important;
    }

    h1 { font-size: 1.8rem !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.4rem !important; margin-top: 1.5rem !important; }
    h3 { font-size: 1.2rem !important; margin-top: 1rem !important; }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-size: var(--text-size-base);
        font-weight: 500;
        padding: 0.5rem 1rem;
        background-color: #0d6efd;
        color: white;
        border: none;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #0b5ed7;
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.2);
        transform: translateY(-1px);
    }

    /* Metric Card Styling */
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-family: 'Outfit', sans-serif;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        font-size: var(--text-size-base) !important;
        font-weight: 500 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre;
        background-color: transparent;
        border-radius: 8px;
        color: #888;
        font-weight: 500;
        padding: 0 1rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(13, 110, 253, 0.1) !important;
        color: #0d6efd !important;
        border-bottom: 2px solid #0d6efd !important;
    }
</style>
""", unsafe_allow_html=True)

# Render Sidebar (handles repo loading and analysis)
render_sidebar()

st.title("🧩 Rikai")
st.caption("Advanced Repository Reasoning & Learning Engine")

if st.session_state.analyzed:
    data = st.session_state.analysis_data
    
    # Define Tabs
    tabs = st.tabs([
        "🎓 Learn This Repo", 
        "🕵️ PR Feedback Reviewer",
        "🧭 Interactive Walkthrough"
    ])
    
    with tabs[0]:
        st.divider()
        render_learning_engine(data)

    with tabs[1]:
        st.divider()
        render_pr_reviewer(data)

    with tabs[2]:
        st.divider()
        render_walkthrough_engine(data)

else:
    # Placeholder State
    st.info("👈 Please enter a valid GitHub repository URL in the sidebar to begin.")
    st.image("https://placehold.co/1200x500?text=Rikai+Intelligence+Ready", caption="Repository Analysis Hub")
