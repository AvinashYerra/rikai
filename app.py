import streamlit as st
from utils.validators import parse_github_url
from core.repo_loader import clone_repo
from core.repo_filter import build_ignore_spec
from core.repo_indexer import index_repository
from utils.json_writer import save_repo_index


st.title("Repo Learning Engine")

url = st.text_input("Paste GitHub repository URL")

if url:
    parsed = parse_github_url(url)
    if parsed:
        if st.button("Analyze Repository"):
            path = clone_repo(*parsed)
            st.success(f"Repository cloned at {path}")
           
            ignore_spec = build_ignore_spec()
            files = index_repository(path, ignore_spec)
            json_path = save_repo_index(
                repo_path=path,
                owner=parsed[0],
                repo=parsed[1],
                files=files
            )

            st.metric("Total files", len(files))
            st.success(f"Repo index saved at {json_path}")
            st.dataframe(files[:20])
            
    else:
        st.error("Invalid GitHub repository URL")








