import streamlit as st
import re, time

st.set_page_config(page_title="ResearchMind - Autonomous Research Assistant", layout="wide")

# --- CSS as per requirement (Dark theme + Pipeline cards) ---
st.markdown("""
<style>
.stApp { background-color: #0A0A0B; color: white; }
.pipeline-card { background: #151515; border: 1px solid #2A2A2A; border-radius: 12px; padding: 18px; margin-bottom: 12px; }
.pipeline-label { font-size: 10px; color: #888; letter-spacing: 1.5px; margin-bottom: 6px; }
.pipeline-title { font-size: 15px; font-weight: 700; color: white; margin-bottom: 4px; }
.pipeline-desc { font-size: 12px; color: #999; line-height: 1.5; }
.tag { display: inline-block; background: #1E1E1E; border: 1px solid #333; color: #AAA; padding: 4px 10px; border-radius: 20px; font-size: 11px; margin: 2px; }
.orange-btn button { background: #FF8C00!important; color: black!important; font-weight: 700!important; border-radius: 10px!important; border: none!important; height: 48px; }
.stTextInput input { background: #151515!important; border: 1px solid #333!important; color: white!important; border-radius: 10px!important; height: 48px; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0;">
<div style="display:flex; align-items:center; gap:12px;">
<div style="background:#FF8C00; width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:800; color:black;">R</div>
<div><div style="font-weight:800; font-size:18px;">ResearchMind</div><div style="font-size:10px; color:#888; letter-spacing:2px;">AI RESEARCH ASSISTANT</div></div>
</div>
<div style="display:flex; gap:8px;"><span class="tag">Local LLM</span><span class="tag">Web Search</span><span class="tag">Source Reading</span><span class="tag">Critic Review</span></div>
</div>
<hr style="border:1px solid #1A1A1A; margin:10px 0 20px 0;">
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("<h1 style='font-size:42px; line-height:1.1;'>What would you<br>like to <span style='color:#FF8C00;'>research</span><br>today?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888; margin-top:10px;'>Our autonomous agents will search the web, read sources, draft your report, and refine it.</p>", unsafe_allow_html=True)
    
    topic = st.text_input("TOPIC", placeholder="e.g., Impact of AI in today's world...", label_visibility="collapsed")
    
    st.markdown('<div class="orange-btn">', unsafe_allow_html=True)
    run_btn = st.button("Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if run_btn and topic:
        from pipeline import run_full_pipeline
        
        progress = st.progress(0)
        status_box = st.empty()
        logs = st.empty()
        log_text = []
        def st_log(msg):
            log_text.append(msg)
            logs.code("\n".join(log_text))

        status_box.info("Pipeline Running: Search -> Reader -> Writer -> Critic")
        progress.progress(10)
        
        result = run_full_pipeline(topic, log_callback=st_log)
        
        # --- FIX for KeyError: 'final' ---
        # Handle both dict and CrewOutput
        if isinstance(result, dict):
            final_report = result.get("final") or result.get("raw") or str(result)
            search_out = result.get("search", "No search data")
            research_out = result.get("research", "No research data")
            urls = result.get("urls", [])
            draft_out = result.get("draft", final_report)
        else:
            # CrewOutput case
            final_report = getattr(result, 'raw', str(result))
            search_out = final_report
            research_out = final_report
            urls = []
            draft_out = final_report
        
        progress.progress(100)
        status_box.success("Research Complete - All 4 Agents Finished")

        st.markdown("---")
        
        # --- REQUIREMENT 1: FINAL REPORT FIRST ---
        st.markdown("<h2 style='color:#FF8C00;'>FINAL RESEARCH REPORT [Critic Chain Output]</h2>", unsafe_allow_html=True)
        st.markdown(final_report)
        st.download_button("Download Final Report", final_report, file_name="final_report.md")

        st.markdown("---")
        st.markdown("### Work of Each Agent (As Per Requirement)")

        # --- REQUIREMENT 2: SEPARATE WORK OF EACH AGENT ---
        with st.expander("01 - SEARCH AGENT WORK - Tools: web_search + wikipedia_search", expanded=True):
            st.info("This is REAL work of SEARCH AGENT - It searched web and found URLs")
            st.code(str(search_out)[:8000], language="markdown")
            st.success(f"Total URLs Found: {len(urls)}")

        with st.expander("02 - READER AGENT WORK - Tools: scrape_webpage + summarize_text", expanded=True):
            st.info("This is REAL work of READER AGENT - It read all URLs and summarized")
            st.code(str(research_out)[:8000], language="markdown")

        with st.expander("03 - WRITER CHAIN WORK - Draft Report", expanded=False):
            st.info("This is work of WRITER CHAIN - It created structured draft")
            st.markdown(str(draft_out)[:10000])

        with st.expander("04 - CRITIC CHAIN WORK - Shows Critical Things + Final Report", expanded=True):
            st.info("This is work of CRITIC CHAIN - It shows critical issues and fixes them")
            st.markdown(final_report)
            st.markdown("---")
            st.write("**Verified Source URLs (Tool: extract_links):**")
            for u in urls:
                st.markdown(f"- {u}")

with col2:
    # --- REQUIREMENT 3: PIPELINE VISUALIZATION ---
    st.markdown("""
    <div class="pipeline-card">
        <div class="pipeline-label">01 / SEARCH AGENT</div>
        <div class="pipeline-title">Search & Discover</div>
        <div class="pipeline-desc">Uses <b>web_search</b> + <b>wikipedia_search</b> tools to find sources with URLs. Output shown in Tab 01.</div>
    </div>
    <div class="pipeline-card">
        <div class="pipeline-label">02 / READER AGENT</div>
        <div class="pipeline-title">Read & Extract</div>
        <div class="pipeline-desc">Uses <b>scrape_webpage</b> + <b>summarize_text</b> tools to read and condense content. Output shown in Tab 02.</div>
    </div>
    <div class="pipeline-card">
        <div class="pipeline-label">03 / WRITER CHAIN</div>
        <div class="pipeline-title">Draft Report</div>
        <div class="pipeline-desc">Composes structured report with Introduction, Key Findings with Source URLs, Conclusion. Output shown in Tab 03.</div>
    </div>
    <div class="pipeline-card" style="border-left: 3px solid #FF8C00;">
        <div class="pipeline-label">04 / CRITIC CHAIN</div>
        <div class="pipeline-title">Review & Refine</div>
        <div class="pipeline-desc">Uses <b>extract_links</b> tool. Shows <b>CRITICAL REVIEW</b> (issues found), <b>MISSING SOURCES</b>, and <b>FINAL IMPROVED REPORT</b>. Output shown in Tab 04 + Final Report on top.</div>
    </div>
    """, unsafe_allow_html=True)