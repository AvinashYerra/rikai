import streamlit as st
import json
from utils.github_utils import fetch_pr_diff, parse_pr_url
from reasoners.pr_reviewer_reasoner import analyze_pr

def render_pr_reviewer(analysis_data: dict):
    """
    Renders the PR Feedback Reviewer UI.
    Requires context from the loaded repository.
    """
    st.markdown("## PR Feedback Reviewer")
    st.markdown("Paste a GitHub Pull Request URL to get a deep architectural review based on this repository's design patterns.")

    # PR URL Input
    pr_url = st.text_input("GitHub Pull Request URL", placeholder="https://github.com/owner/repo/pull/123", key="pr_reviewer_input")

    if st.button("Review Pull Request"):
        if not pr_url:
            st.error("Please enter a valid PR URL.")
            return

        # 1. Parse and Validate URL
        parsed = parse_pr_url(pr_url)
        if not parsed:
            st.error("Invalid PR URL. Please ensure it follows the format: https://github.com/owner/repo/pull/123")
            return

        # Check if requested PR belongs to the loaded repo
        current_owner = analysis_data.get("owner")
        current_repo = analysis_data.get("repo")
        
        if parsed["owner"] != current_owner or parsed["repo"] != current_repo:
            st.warning(f"Warning: This PR belongs to `{parsed['owner']}/{parsed['repo']}`, but you have `{current_owner}/{current_repo}` loaded. Reasoning may be less accurate.")

        # 2. Fetch Diff
        with st.status("Fetching PR diff from GitHub...") as status:
            diff = fetch_pr_diff(pr_url)
            if not diff:
                st.error("Failed to fetch PR diff. Ensure the PR exists and is public.")
                return
            
            # Limit diff size for LLM context (simple truncation)
            if len(diff) > 50000:
                diff = diff[:50000] + "\n\n...[Diff truncated due to size]..."
            
            st.write("Diff fetched successfully.")
            
            # 3. Analyze PR
            st.write("Gemini is reviewing the changes...")
            repo_context = st.session_state.get("reasoning_output", {}) # Use existing wisdom if available
            
            # Package context for reviewer
            # If we don't have reasoning wisdom, use static analysis
            enriched_context = {
                "static_analysis": analysis_data,
                "architectural_wisdom": repo_context.get("architecture") if repo_context else "Not analyzed yet"
            }
            
            try:
                review_json = analyze_pr(enriched_context, diff)
                review_data = json.loads(review_json)
                st.session_state.last_pr_review = review_data
                status.update(label="Review Complete!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Error during PR review: {e}")
                return

    # Display Last Review if it exists
    if "last_pr_review" in st.session_state:
        review = st.session_state.last_pr_review
        st.divider()
        
        # 1. Approval Score & Key Verdict
        c1, c2 = st.columns([1, 3])
        score = review.get("approval_readiness_score", 0)
        verdict = review.get("overall_verdict", "Comment")
        
        with c1:
            st.metric("Readiness Score", f"{score}/100")
            if verdict == "Approve":
                st.success(f"Verdict: {verdict}")
            elif verdict == "Request Changes":
                st.error(f"Verdict: {verdict}")
            else:
                st.warning(f"Verdict: {verdict}")

        with c2:
            st.markdown(f"### Top Priority Improvement")
            st.markdown(f"> {review.get('top_priority_improvement', 'No critical issues found.')}")

        st.markdown("### Summary")
        st.write(review.get("summary", ""))

        # 2. Detailed Comments (GitHub style)
        st.markdown("### Detailed Feedback")
        comments = review.get("comments", [])
        if comments:
            for comment in comments:
                severity = comment.get("severity", "suggestion")
                icon = "[CRITICAL]" if severity == "critical" else "[MAJOR]" if severity == "major" else "[MINOR]" if severity == "minor" else "[INFO]"
                
                with st.expander(f"{icon} {comment.get('type').upper()} in {comment.get('file')}"):
                    st.markdown(f"**Issue:** {comment.get('issue')}")
                    st.markdown(f"**Suggestion:**")
                    st.info(comment.get('suggestion'))
                    st.caption(f"Lines: {comment.get('line_range')} | Severity: {severity}")
        else:
            st.info("No specific code improvements suggested.")
            
        if st.button("Clear Review"):
            del st.session_state.last_pr_review
            st.rerun()
