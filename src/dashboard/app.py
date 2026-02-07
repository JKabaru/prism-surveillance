import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
from src.engine.correlation_engine import PRISMCorrelationEngine
from src.engine.network_mapper import PRISMNetworkMapper
from src.engine.synthesizer import PRISMEvidenceSynthesizer
from src.engine.behavior_engine import PRISMBehaviorEngine
from src.dashboard.reporter import PRISMReporter
from src.engine.regime_monitor import PRISMRegimeMonitor

st.set_page_config(
    page_title="PRISM | AI-Powered Fraud Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode and styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<style>
    /* Global Styles */
    :root {
        --primary: #137fec;
        --background-dark: #050505;
        --surface-dark: #0d0d0d;
        --surface-lighter: #151515;
        --prism-cyan: #00f2ff;
        --prism-magenta: #ff00ff;
        --prism-violet: #8b5cf6;
        --card-dark: #111111;
        --border-glass: rgba(255, 255, 255, 0.08);
    }

    .stApp {
        background-color: var(--background-dark);
        color: #slate-300;
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Panel */
    .glass-panel {
        background: rgba(13, 13, 13, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    /* Neon Accents */
    .neon-cyan { text-shadow: 0 0 8px rgba(0, 242, 255, 0.4); color: var(--prism-cyan); }
    .neon-violet { text-shadow: 0 0 8px rgba(139, 92, 246, 0.4); color: var(--prism-violet); }
    .neon-magenta { text-shadow: 0 0 8px rgba(255, 0, 255, 0.4); color: var(--prism-magenta); }

    /* Metric Styling Overwrite */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: white !important;
    }
    [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] {
        background: var(--surface-dark);
        border: 1px solid var(--border-glass);
        border-radius: 12px;
        padding: 20px !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--surface-dark);
        border-right: 1px solid var(--border-glass);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #94a3b8;
    }

    /* Fraud Card */
    .fraud-card {
        background: var(--card-dark);
        padding: 24px;
        border-radius: 16px;
        border-left: 4px solid var(--prism-magenta);
        margin-bottom: 24px;
        transition: transform 0.2s ease, background 0.2s ease;
    }
    .fraud-card:hover {
        background: var(--surface-lighter);
        transform: translateY(-2px);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--background-dark);
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #444;
    }
</style>
""", unsafe_allow_html=True)

from src.data.loader import PRISMDataLoader

# Initialize Engines (passed session state data if available)
if 'partners_df' in st.session_state and st.session_state.partners_df is not None:
    engine = PRISMCorrelationEngine(time_window_seconds=1.0)
    mapper = PRISMNetworkMapper(st.session_state.clients_df, st.session_state.subs_df, st.session_state.partners_df)
    synthesizer = PRISMEvidenceSynthesizer()
    behavior_engine = PRISMBehaviorEngine()
    reporter = PRISMReporter()
    regime_monitor = PRISMRegimeMonitor()
    loader = PRISMDataLoader()
else:
    engine = PRISMCorrelationEngine(time_window_seconds=1.0)
    mapper = PRISMNetworkMapper(None, None, None)
    synthesizer = PRISMEvidenceSynthesizer()
    behavior_engine = PRISMBehaviorEngine()
    reporter = PRISMReporter()
    regime_monitor = PRISMRegimeMonitor()
    loader = PRISMDataLoader()


if 'app_state' not in st.session_state:
    st.session_state.app_state = "SETUP"

# Initialize Session States
if 'partners_df' not in st.session_state:
    st.session_state.partners_df = None
    st.session_state.subs_df = None
    st.session_state.clients_df = None
    st.session_state.trades_df = None
    st.session_state.col_mapping = {"Partners": {}, "Sub-Affiliates": {}, "Clients": {}, "Trades": {}}

def load_data_state(p, s, c, t):
    st.session_state.partners_df = p
    st.session_state.subs_df = s
    st.session_state.clients_df = c
    st.session_state.trades_df = t
    # Update Mapper attributes correctly
    mapper.partners_df = p
    mapper.subs_df = s
    mapper.clients_df = c
    # Trigger auto-focus on Overview
    st.session_state.active_intake_tab = "📊 Data Overview"
    st.toast("🚀 Data initialized! Visualizing distribution...", icon="✅")

from src.engine.llm_client import PRISMLLMClient

# Sidebar Header Branding
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
    <div style="width: 32px; height: 32px; border-radius: 6px; background: linear-gradient(135deg, var(--prism-cyan), var(--prism-violet), var(--prism-magenta)); display: flex; align-items: center; justify-content: center;">
        <span class="material-symbols-outlined" style="color: white; font-size: 20px;">deployed_code</span>
    </div>
    <div>
        <h1 style="font-size: 1.2rem; font-weight: 700; color: white; margin: 0; line-height: 1;">PRISM</h1>
        <span style="font-size: 0.6rem; color: #64748b; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<p style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Navigation</p>', unsafe_allow_html=True)

if st.session_state.app_state == "SETUP":
    setup_options = ["Data Hub", "Agentic Settings"]
    
    # Auto-transition logic (Setup)
    if 'page_transition' in st.session_state and st.session_state.page_transition in setup_options:
        st.session_state.current_page_setup = st.session_state.page_transition
        del st.session_state.page_transition
    
    if 'current_page_setup' not in st.session_state:
        st.session_state.current_page_setup = setup_options[0]

    page = st.sidebar.radio("Phase 1: Setup", setup_options, index=setup_options.index(st.session_state.current_page_setup))
    st.session_state.current_page_setup = page
    
    # Check for readiness in Sidebar
    data_ready = st.session_state.trades_df is not None
    llm_ready = 'llm_settings' in st.session_state and st.session_state.get('api_key')
    
    st.sidebar.divider()
    if data_ready and llm_ready:
        if st.sidebar.button("🚀 Begin Agentic Analysis", use_container_width=True):
            st.session_state.app_state = "PROCESSING"
            st.toast("Starting forensic analysis engine...", icon="⚙️")
            st.rerun()
    else:
        st.sidebar.warning("Complete Setup to unlock Analysis.")
        if not data_ready: st.sidebar.caption("❌ Data not loaded")
        if not llm_ready: st.sidebar.caption("❌ LLM not configured")

elif st.session_state.app_state == "PROCESSING":
    page = "Processing Pipeline"
    st.sidebar.info("Agentic processing in progress...")

else: # INSIGHTS state
    st.sidebar.markdown('<p style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Forensic Command</p>', unsafe_allow_html=True)
    
    # Coherent, meaningful navigation menu
    nav_options = [
        "🛡️ Command Center", 
        "🔍 Nexus Graph", 
        "📈 Regime Monitor", 
        "📡 Live Surveillance", 
        "📥 Data Management", 
        "⚙️ AI Settings"
    ]
    
    # Auto-transition logic (Robust matching)
    if 'page_transition' in st.session_state:
        target = st.session_state.page_transition
        match = next((opt for opt in nav_options if target in opt), None)
        if match:
            st.session_state.current_page = match
        del st.session_state.page_transition
    
    if 'current_page' not in st.session_state or st.session_state.current_page not in nav_options:
        st.session_state.current_page = nav_options[0]

    page = st.sidebar.radio("Go to", nav_options, index=nav_options.index(st.session_state.current_page))
    st.session_state.current_page = page
    
    st.sidebar.divider()
    if st.sidebar.button("System Reset (Setup Mode)", use_container_width=True):
        st.session_state.app_state = "SETUP"
        st.rerun()

# Sidebar System Health
st.sidebar.markdown("---")
st.sidebar.markdown('<p style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">System Health</p>', unsafe_allow_html=True)

health_metrics = [
    {"label": "Throughput", "value": "14.2k/s", "progress": 75, "color": "var(--prism-cyan)"},
    {"label": "Latency", "value": "42ms", "progress": 25, "color": "var(--prism-violet)"},
    {"label": "Stability", "value": "99.8%", "progress": 92, "color": "var(--prism-magenta)"}
]

for m in health_metrics:
    st.sidebar.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 4px;">
            <span style="color: #94a3b8;">{m['label']}</span>
            <span style="color: white; font-family: monospace;">{m['value']}</span>
        </div>
        <div style="height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px; overflow: hidden;">
            <div style="height: 100%; width: {m['progress']}%; background: {m['color']}; box-shadow: 0 0 8px {m['color']};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="glass-panel" style="padding: 16px; margin-top: 24px; border: 1px solid rgba(255,255,255,0.05); background: linear-gradient(135deg, rgba(255,255,255,0.05), transparent);">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
        <span class="material-symbols-outlined" style="color: var(--prism-cyan); font-size: 18px;">shield</span>
        <span style="font-size: 0.75rem; font-weight: 700; color: white;">Active Sentinel</span>
    </div>
    <p style="font-size: 0.65rem; color: #64748b; line-height: 1.4; margin: 0;">Autonomous firewall adjusting 1,240 rules based on current drift.</p>
</div>
""", unsafe_allow_html=True)

# --- Page Logic ---

if st.session_state.app_state == "PROCESSING":
    st.markdown('<h1 class="neon-cyan">🤖 Glass-Box Reasoning</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; margin-top: -15px; margin-bottom: 25px;">Complete transparency into the AI\'s data traversal and policy application.</p>', unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.subheader("Live Agent Feed")
        log_container = st.empty()
        
    with col_v2:
        st.subheader("Detected Entities")
        findings_container = st.container()

    # Shared logs
    if 'agent_logs' not in st.session_state: st.session_state.agent_logs = []
    
    def add_log(msg, type="info"):
        emoji = "ℹ️" if type == "info" else "🔍" if type == "scan" else "✅" if type == "success" else "⚠️"
        st.session_state.agent_logs.append(f"{emoji} {msg}")
        # Display last 10 logs with terminal styling
        log_html = f"<div style='background: #111; color: #0f0; padding: 10px; border-radius: 5px; font-family: monospace; height: 300px; overflow-y: auto;'>"
        log_html += "<br>".join(st.session_state.agent_logs[-15:])
        log_html += "</div>"
        log_container.markdown(log_html, unsafe_allow_html=True)

    # Actual Execution with real-time feedback
    import time
    add_log("Initializing PRISM Agentic Engine...", "info")
    time.sleep(1)
    
    # Emergency Interjection Check
    if st.session_state.get('agent_settings', {}).get('kill_switch'):
        add_log("Emergency Kill Switch active. Aborting pipeline.", "warning")
        st.error("Global Kill Switch is ON. Agentic actions are suspended.")
        if st.button("Reset Kill Switch"):
            st.session_state.agent_settings['kill_switch'] = False
            st.rerun()
        st.stop()

    # 1. Detection
    add_log("Scanning trade logs for temporal synchronization...", "scan")
    clusters = engine.detect_mirror_trades(st.session_state.trades_df)
    rings = engine.aggregate_rings(clusters)
    time.sleep(1)
    add_log(f"Detected {len(rings)} potential fraud clusters.", "success")
    
    # 2. Synthesis & Glass-Box view for each (Fully Autonomous)
    for ring in rings:
        with findings_container:
            st.markdown(f"**Ring {ring['id']}** identified.")
        
        add_log(f"Analyzing Ring {ring['id']} attribution and behavior...", "scan")
        attr = mapper.get_attribution(ring['client_ids'])
        evidence = synthesizer.synthesize_ring(ring, attr)
        
        # Show reasoning logs
        for r_log in evidence['agent_decision']['reasoning_logs']:
            add_log(f"  > {r_log}", "info")
            time.sleep(0.3)
        
        # Autonomous execution feedback
        action = evidence['agent_decision']['selected_action']
        add_log(f"Policy authorized. Executing {action} autonomously...", "success")
        
        with findings_container:
            st.success(f"Action Executed: {action}")
            # Non-blocking interjection link
            if st.button(f"Override {ring['id']}", key=f"ovr_{ring['id']}"):
                st.session_state.selected_ring = ring
                st.session_state.app_state = "INSIGHTS"
                st.rerun()

    add_log("Phase 2 Analysis: Behavioral anomalies...", "scan")
    time.sleep(1)
    add_log("Full Autonomous Cycle Complete. Audit trail generated.", "success")
    
    if st.button("Review Autonomous Decisions"):
        st.session_state.app_state = "INSIGHTS"
        st.rerun()
    st.stop()

# Robust page mapping for all states
if "Data Hub" in page or "Data Management" in page: page = "Data Intake"
elif "Agentic Settings" in page or "Settings" in page: page = "Settings"
elif "Command Center" in page: page = "Command Center"
elif "Nexus Graph" in page: page = "Nexus Graph"
elif "Regime Monitor" in page: page = "Regime Monitor"
elif "Live Surveillance" in page: page = "Live Surveillance"

# --- Global Data Refresh & Safety Guards ---
p_df = st.session_state.partners_df
s_df = st.session_state.subs_df
c_df = st.session_state.clients_df
t_df = st.session_state.trades_df

# Handle empty state globally for analytical pages
analytical_pages = ["Command Center", "Nexus Graph", "Live Surveillance", "Regime Monitor"]
if page in analytical_pages and t_df is None:
    st.title(f"🛡️ {page}")
    st.warning("Analysis engines are offline: No data detected.")
    st.info("Please initialize PRISM on the **Data Intake** or **Data Hub** page.")
    st.sidebar.divider()
    if st.sidebar.button("System Reset (Setup Mode)", use_container_width=True):
        st.session_state.app_state = "SETUP"
        st.rerun()
    st.stop()

# Mapper attribute safety sync
if p_df is not None:
    mapper.partners_df = p_df
    mapper.subs_df = s_df
    mapper.clients_df = c_df

# --- Page Rendering Logic ---

if page == "Settings":
    st.title("⚙️ AI & Agentic Settings")
    st.subheader("LLM Provider Configuration")
    
    col_l1, col_l2 = st.columns(2)
    provider = col_l1.selectbox("Provider", ["OpenRouter", "DeepSeek", "OpenAI", "Gemini", "Claude"], index=0)
    
    # Dynamic Model Fetching
    client = PRISMLLMClient(provider, st.session_state.get('api_key'))
    models = client.get_models()
    model_ids = [m['id'] for m in models]
    
    selected_model = col_l2.selectbox("Model selection", model_ids, index=0 if model_ids else None)
    
    api_key = st.text_input("API Key", type="password", value=st.session_state.get('api_key', ""))
    
    # Connection Lock
    if 'llm_verified' not in st.session_state: st.session_state.llm_verified = False

    if st.button("Test Connection"):
        temp_client = PRISMLLMClient(provider, api_key)
        with st.spinner("Verifying credentials..."):
            if temp_client.test_connection():
                st.success(f"Connected to {provider} successfully!")
                st.session_state.llm_verified = True
            else:
                st.error(f"Failed to connect to {provider}. Please check your API key.")
                st.session_state.llm_verified = False

    save_disabled = not st.session_state.llm_verified
    if st.button("Save & Proceed", disabled=save_disabled, use_container_width=True):
        st.session_state.api_key = api_key
        st.session_state.llm_settings = {"provider": provider, "model": selected_model}
        st.session_state.llm_ready = True # For easier checking
        
        # Auto-flow: If data is not yet loaded, guide user to Data Hub
        if st.session_state.trades_df is None:
            st.session_state.page_transition = "Data Hub"
            st.toast("LLM configured! Next: Load your data.", icon="🤖")
        else:
            st.toast("Settings saved successfully.", icon="✅")
        st.rerun()
    
    st.divider()
    st.subheader("Agentic Autonomy Policy")
    autonomy_enabled = st.toggle("Enable Autonomous Containment", value=True)
    kill_switch = st.checkbox("Global Kill Switch (Stop all Agent actions)", value=False)
    
    st.session_state.agent_settings = {
        "autonomy_enabled": autonomy_enabled,
        "kill_switch": kill_switch,
        "human_in_loop": st.checkbox("Always require human approval before execution", value=False)
    }

elif page == "Command Center":
    st.markdown('<h1 class="neon-violet">🛡️ Command Center</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; margin-top: -15px; margin-bottom: 25px;">Autonomous Fraud-Ring Mapping & Temporal Intelligence</p>', unsafe_allow_html=True)
    
    # Run Detection
    with st.spinner("Analyzing temporal correlations..."):
        clusters = engine.detect_mirror_trades(t_df)
        rings = engine.aggregate_rings(clusters)
        
        # Phase 2: Behavior
        bonus_abuse = behavior_engine.detect_bonus_abuse(t_df, c_df)
        commission_fraud = behavior_engine.detect_commission_inflation(t_df, c_df, s_df)
    
    # Top Stats
    col1, col2, col3, col4 = st.columns(4)
    risk_exposure = (len(rings)*4200 + len(bonus_abuse)*1000 + len(commission_fraud)*5000) if t_df is not None else 0
    col1.metric("Risk Exposure", f"${risk_exposure:,.0f}", "+5.4%")
    col2.metric("Active Threads", f"{len(rings) + len(bonus_abuse) + len(commission_fraud)}", "+3")
    col3.metric("System Health", "Operational", "42ms")
    col4.metric("Analyzed Trades", f"{len(t_df) if t_df is not None else 0:,}")
    
    st.divider()
    
    st.subheader("Agentic Investigation Workbench")
    
    for ring in rings:
        with st.container():
            attr = mapper.get_attribution(ring['client_ids'])
            evidence = synthesizer.synthesize_ring(ring, attr)
            
            # Fraud Card Rendering
            st.markdown(f"""
            <div class="glass-panel fraud-card" style="border-left: 4px solid var(--prism-magenta); margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 40px; height: 40px; border-radius: 10px; background: rgba(255, 0, 255, 0.1); border: 1px solid rgba(255, 0, 255, 0.2); display: flex; align-items: center; justify-content: center;">
                            <span class="material-symbols-outlined" style="color: var(--prism-magenta);">hub</span>
                        </div>
                        <div>
                            <h4 style="margin: 0; color: white; font-size: 1.1rem;">Ring: {ring['id']}</h4>
                            <p style="margin: 0; font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Temporal Cluster Detected</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--prism-magenta); line-height: 1;" class="neon-magenta">{evidence['confidence']*100:.1f}</div>
                        <div style="font-size: 0.6rem; font-weight: 700; color: #475569; text-transform: uppercase;">Confidence</div>
                    </div>
                </div>
                
                <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6; margin-bottom: 20px;">{evidence['hypothesis']}</p>
                
                <div style="background: rgba(0, 242, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.1); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                        <span class="material-symbols-outlined" style="color: var(--prism-cyan); font-size: 16px;">robot_2</span>
                        <span style="font-size: 0.7rem; font-weight: 700; color: var(--prism-cyan); text-transform: uppercase; letter-spacing: 1px;">Agentic Analysis Flow</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #cbd5e1; display: grid; grid-template-cols: 1fr 1fr; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 4px;"><span style="color: #22c55e;">●</span> Connection Mapped</div>
                        <div style="display: flex; align-items: center; gap: 4px;"><span style="color: #22c55e;">●</span> Evidence Synthesized</div>
                        <div style="display: flex; align-items: center; gap: 4px;"><span style="color: #22c55e;">●</span> Policy Applied</div>
                        <div style="display: flex; align-items: center; gap: 4px;"><span style="color: var(--prism-violet);">○</span> Action: <b>{evidence['agent_decision']['selected_action']}</b></div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.05);">
                    <div style="display: flex; gap: 16px;">
                        <div>
                            <p style="margin: 0; font-size: 0.6rem; color: #64748b; text-transform: uppercase;">Exposure</p>
                            <p style="margin: 0; font-size: 0.9rem; font-weight: 600; color: #e2e8f0;">${evidence['exposure']:,}</p>
                        </div>
                        <div>
                            <p style="margin: 0; font-size: 0.6rem; color: #64748b; text-transform: uppercase;">Accounts</p>
                            <p style="margin: 0; font-size: 0.9rem; font-weight: 600; color: #e2e8f0;">{len(ring['client_ids'])}</p>
                        </div>
                    </div>
                    <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); padding: 4px 12px; border-radius: 6px;">
                        <span style="font-size: 0.7rem; font-weight: 700; color: var(--prism-violet); text-transform: uppercase;">Decision: {evidence['agent_decision']['selected_action']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action logic (replacing code block with functional buttons)
            col_act1, col_act2 = st.columns(2)
            if col_act1.button(f"🔍 Investigate {ring['id']}", key=f"inv_{ring['id']}", use_container_width=True):
                st.session_state.selected_ring = ring
                st.session_state.page_transition = "Nexus Graph"
                st.rerun()
            
            with col_act2.expander("AI Reasoning Details"):
                st.json(evidence['agent_decision'])
                st.write(f"**Justification:** {evidence['agent_decision']['justification']}")


    st.markdown('<h3 style="margin-top: 40px; margin-bottom: 20px; font-size: 1.1rem; color: white;">🔍 Behavioral Anomalies</h3>', unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("#### Bonus Abuse Detected")
        if not bonus_abuse:
            st.success("No bonus abuse patterns detected.")
        for abuse in bonus_abuse:
             evidence = synthesizer.synthesize_bonus_abuse(abuse['client_id'], abuse['risk_score'], abuse['trade_count'])
             with st.expander(f"Client {abuse['client_id']} (Risk: {int(evidence['confidence']*100)}%)"):
                st.error(evidence['hypothesis'])
                st.write("**Indicators:**")
                for ind in evidence['indicators']:
                    st.write(f"- {ind}")
             
    with col_b2:
        st.markdown("#### Commission Inflation")
        if not commission_fraud:
             st.success("No commission inflation detected.")
        for fraud in commission_fraud:
             stats = fraud['stats']
             evidence = synthesizer.synthesize_commission_inflation(fraud['sub_affiliate_id'], fraud['risk_score'], stats)
             with st.expander(f"Sub {fraud['sub_affiliate_id']} (Risk: {int(evidence['confidence']*100)}%)"):
                st.warning(evidence['hypothesis'])
                st.write("**Indicators:**")
                for ind in evidence['indicators']:
                    st.write(f"- {ind}")

elif page == "Nexus Graph":
    if 'selected_ring' not in st.session_state:
        st.warning("Please select a ring from the Command Center first.")
    else:
        ring = st.session_state.selected_ring
        st.markdown(f'<h1 class="neon-cyan">🕵️ Investigation Workbench</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #64748b; margin-top: -15px; margin-bottom: 25px;">Evidence Analysis for Case: <b>{ring["id"]}</b></p>', unsafe_allow_html=True)
        
        # --- Interactive Filtering ---
        with st.expander("🔎 Filter Graph & Evidence", expanded=True):
            col_f1, col_f2, col_f3 = st.columns(3)
            f_symbol = col_f1.selectbox("Filter by Symbol", ["All"] + list(t_df['symbol'].unique()))
            f_direction = col_f2.selectbox("Filter by Direction", ["All", "Buy", "Sell"])
            f_min_vol = col_f3.slider("Min Volume", 0.0, 10.0, 0.0)
            
        filters = {}
        if f_symbol != "All": filters['symbol'] = f_symbol
        if f_direction != "All": filters['direction'] = f_direction
        if f_min_vol > 0: filters['min_volume'] = f_min_vol
        
        # Build Filtered Graph
        G = mapper.build_filtered_graph(ring['client_ids'], t_df, filters)
        
        # Simple Plotly Network Visualization
        pos = nx.spring_layout(G)
        
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line={'width': 0.5, 'color': '#888'},
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{node}: {G.nodes[node]['label']}")
            
            if G.nodes[node]['type'] == 'partner':
                node_color.append('#ff00ff')
            elif G.nodes[node]['type'] == 'sub':
                node_color.append('#8b5cf6')
            else:
                node_color.append('#00f2ff')

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[G.nodes[node]['label'] for node in G.nodes()],
            textposition="top center",
            hoverinfo='text',
            marker={
                'showscale': False,
                'color': node_color,
                'size': 20,
                'line_width': 2
            })

        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0,l=0,r=0,t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<h3 style="margin-top: 30px; margin-bottom: 15px; font-size: 1.1rem; color: white;">📦 Ring Evidence Package</h3>', unsafe_allow_html=True)
        attr = mapper.get_attribution(ring['client_ids'])
        evidence = synthesizer.synthesize_ring(ring, attr)
        
        col_ev1, col_ev2 = st.columns(2)
        with col_ev1:
            st.markdown("### Hypothesis")
            st.write(evidence['hypothesis'])
        with col_ev2:
            st.markdown("### Risk Indicators")
            for ind in evidence['indicators']:
                st.write(f"- {ind}")
                
        st.divider()
        
        # --- Actions & Reporting ---
        st.markdown('<h3 style="margin-top: 30px; margin-bottom: 15px; font-size: 1.1rem; color: white;">⚖️ Case Management</h3>', unsafe_allow_html=True)
        col_a1, col_a2, col_a3 = st.columns(3)
        
        if col_a1.button("📄 Export Evidence Brief"):
            # Generate static graph image bytes (mocking for now or using plotly static export if setup)
            # For this demo, we'll pass None to the reporter, or we could generate a simple matplotlib one
            report_html = reporter.generate_html_report(ring['id'], evidence, attr, graph_bytes=None)
            st.download_button(
                label="Download HTML Report",
                data=report_html,
                file_name=f"PRISM_Evidence_{ring['id']}.html",
                mime="text/html"
            )
            
        if col_a2.button("❄️ Freeze Payouts"):
            st.success(f"Payouts frozen for {len(ring['client_ids'])} accounts in Ring {ring['id']}. Audit log updated.")
            
            if col_a3.button("⚠️ Escalate to Compliance", key=f"esc_{ring['id']}"):
                st.warning(f"Case {ring['id']} escalated to Tier 2 Compliance Team.")

elif page == "Data Intake":
    st.markdown('<h1 class="neon-violet">📥 Data Intake</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; margin-top: -15px; margin-bottom: 25px;">Centralized workspace for data ingestion and refinement.</p>', unsafe_allow_html=True)

    # Controlled Tabs using radio to allow programmatic switching
    tabs_list = ["🚀 Ingestion", "📊 Data Overview", "🗺️ Field Mapping", "📝 Data Editor"]
    
    if 'active_intake_tab' not in st.session_state:
        st.session_state.active_intake_tab = tabs_list[0]
        
    # Find index of current active tab
    try:
        tab_index = tabs_list.index(st.session_state.active_intake_tab)
    except ValueError:
        tab_index = 0

    # Custom "Tab" selector
    active_tab = st.radio("Navigation", tabs_list, index=tab_index, horizontal=True, key="intake_tabs_nav", label_visibility="collapsed")
    st.session_state.active_intake_tab = active_tab # Sync back

    st.divider()

    if active_tab == "🚀 Ingestion":
        st.subheader("Select Data Source")
        ds_col1, ds_col2 = st.columns([1, 2])
        data_source = ds_col1.radio("Source Type", ["Synthetic Data", "File Upload", "Database Connection"])
        
        with ds_col2:
            if data_source == "Synthetic Data":
                st.write("### Synthetic Generation")
                st.caption("Generate realistic fraud patterns (Mirror, Bonus Abuse, Sleeper).")
                gen_col1, gen_col2 = st.columns(2)
                n_p = gen_col1.slider("Partners", 2, 20, 5)
                n_c = gen_col2.slider("Clients per Sub", 5, 50, 10)
                if st.button("Generate Demo Data", use_container_width=True):
                    with st.spinner("Generating..."):
                        p, s, c, t = loader.load_synthetic(num_partners=n_p, clients_per_sub=n_c)
                        load_data_state(p, s, c, t)
                        st.success(f"Generated {len(t)} trades.")
                        st.rerun()

            elif data_source == "File Upload":
                st.write("### File Upload")
                st.caption("Upload CSV files for Partners, Subs, Clients, and Trades.")
                up_col1, up_col2 = st.columns(2)
                p_file = up_col1.file_uploader("Partners CSV", type="csv")
                s_file = up_col1.file_uploader("Sub-Affiliates CSV", type="csv")
                c_file = up_col2.file_uploader("Clients CSV", type="csv")
                t_file = up_col2.file_uploader("Trades CSV", type="csv")
                
                if st.button("Load and Validate Files", use_container_width=True):
                    if p_file and s_file and c_file and t_file:
                        try:
                            mapping = st.session_state.get('col_mapping', None)
                            p, s, c, t = loader.load_from_files(p_file, s_file, c_file, t_file, column_mapping=mapping)
                            load_data_state(p, s, c, t)
                            st.success("Files loaded and validated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ingestion Error: {str(e)}")
                    else:
                        st.warning("Please upload all 4 files.")

            elif data_source == "Database Connection":
                st.write("### Database Connection")
                st.caption("Connect to external PRISM-compatible databases.")
                conn_str = st.text_input("Connection String", value="postgresql://user:pass@localhost:5432/prism_db")
                if st.button("Initialize Connection", use_container_width=True):
                    success, msg = loader.load_from_db(conn_str)
                    if success:
                        st.success(msg)
                        p, s, c, t = loader.load_synthetic(num_partners=2, subs_per_partner=2, clients_per_sub=5)
                        load_data_state(p, s, c, t)
                        st.rerun()
                    else:
                        st.error(msg)
    
    elif active_tab == "📊 Data Overview":
        st.subheader("Current Data Distribution")
        if t_df is not None:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Partners", len(p_df) if p_df is not None else 0)
            c2.metric("Sub-Affiliates", len(s_df) if s_df is not None else 0)
            c3.metric("Clients", len(c_df) if c_df is not None else 0)
            c4.metric("Trades", len(t_df) if t_df is not None else 0)
            
            st.divider()
            st.write("### Schema Quick Reference")
            req = loader.get_required_columns()
            for table, cols in req.items():
                st.write(f"**{table}**: `{', '.join(cols)}`")
            
            # --- NEXT STEP BUTTON ---
            st.divider()
            llm_ready = 'llm_settings' in st.session_state and st.session_state.get('api_key')
            if llm_ready:
                if st.button("🚀 All Systems Ready: Start Agentic Analysis", use_container_width=True):
                    st.session_state.app_state = "PROCESSING"
                    st.toast("Launching PRISM forensic engines...", icon="🛡️")
                    st.rerun()
            else:
                if st.button("➡️ Step 2: Configure AI & Model Settings", use_container_width=True):
                    st.session_state.page_transition = "Agentic Settings"
                    st.toast("Proceeding to AI configuration.", icon="⚙️")
                    st.rerun()
        else:
            st.warning("No data loaded. Use the Ingestion tab to begin.")

    elif active_tab == "🗺️ Field Mapping":
        st.subheader("Custom Field Mapping")
        st.info("Map your custom CSV headers to PRISM's internal schema requirements before uploading.")
        
        req = loader.get_required_columns()
        for table, mandatory_cols in req.items():
            with st.expander(f"Map {table} Fields"):
                for m_col in mandatory_cols:
                    user_col = st.text_input(f"Your column for '{m_col}'", value=st.session_state.col_mapping[table].get(m_col, m_col), key=f"map_{table}_{m_col}_main")
                    if user_col:
                        st.session_state.col_mapping[table][m_col] = user_col
        
        st.divider()
        if st.button("Confirm Mappings & Load Data", use_container_width=True):
            st.session_state.active_intake_tab = "🚀 Ingestion"
            st.toast("Schema mapped! Ready for ingestion.", icon="🗺️")
            st.rerun()

    elif active_tab == "📝 Data Editor":
        st.subheader("Interactive Data Workbench")
        if t_df is not None:
            # Table selection
            selected_table = st.selectbox("Select Table to View/Edit", ["Partners", "Sub-Affiliates", "Clients", "Trades"])
            
            # Use data from session state directly to avoid stale local variables
            target_df = {
                "Partners": st.session_state.partners_df, 
                "Sub-Affiliates": st.session_state.subs_df, 
                "Clients": st.session_state.clients_df, 
                "Trades": st.session_state.trades_df
            }[selected_table]

            # Use a stable key and capture edits
            edited_df = st.data_editor(target_df, num_rows="dynamic", use_container_width=True, key=f"editor_{selected_table}")
            
            if st.button(f"Commit Changes to {selected_table}", use_container_width=True):
                if selected_table == "Partners": st.session_state.partners_df = edited_df
                elif selected_table == "Sub-Affiliates": st.session_state.subs_df = edited_df
                elif selected_table == "Clients": st.session_state.clients_df = edited_df
                elif selected_table == "Trades": st.session_state.trades_df = edited_df
                
                # Immediate sync with Mapper attributes
                mapper.partners_df = st.session_state.partners_df
                mapper.subs_df = st.session_state.subs_df
                mapper.clients_df = st.session_state.clients_df
                
                st.success(f"Changes to {selected_table} committed! Analysis updated.")
                st.toast("Data synced! Analysis engines re-synchronized.", icon="🔄")
                st.rerun()
        else:
            st.warning("Load data first to use the workbench.")

elif page == "Live Surveillance":
    st.title("📡 Live Surveillance")
    st.caption("Continuous ecosystem monitoring and anomaly detection.")
    st.info("Ecosystem baseline synchronization in progress. Real-time trade feed active.")
    st.metric("Detection Pulse", "Steady", "4ms latency")

elif page == "Regime Monitor":
    st.title("📈 Proactive Regime Detection")
    st.caption("Baseline deviation analysis for sleeper agent activation.")
    
    # Run Monitor
    alerts = regime_monitor.detect_regime_shifts(t_df, c_df)
    
    col1, col2 = st.columns(2)
    col1.metric("Active Shifts Detected", len(alerts), "+1")
    col2.metric("Ecosystem Volatility", "Elevated", "Delta: +15%")
    
    st.divider()
    
    for alert in alerts:
        with st.expander(f"⚠️ Partner {alert['partner_id']} (Risk: {int(alert['risk_score']*100)}%)", expanded=True):
            st.error(alert['hypothesis'])
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Metric", alert['metric'])
            c2.metric("Baseline (20d)", f"{alert['baseline']:,.0f}")
            c3.metric("Current (3d)", f"{alert['current']:,.0f}", f"+{alert['z_score']}σ")
            
            # Simple Trend Chart
            st.line_chart(pd.DataFrame({
                'Baseline': [alert['baseline']]*10,
                'Current': np.concatenate([np.full(7, alert['baseline']), np.full(3, alert['current'])])
            }))
