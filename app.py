import os
import json
from pathlib import Path
import streamlit as st
from graph import app as simulation_app

st.set_page_config(page_title="Jevons Paradox Simulator", page_icon="🏙️", layout="wide")

# Sidebar for configuration
with st.sidebar:
    st.header("Simulation Parameters")
    aggression = st.slider("Swarm Aggression Level", 1, 10, 7)
    city_context = st.selectbox("City Context", ["Bengaluru", "London", "Tokyo", "New York"])
    st.markdown("---")
    active_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    st.caption(f"Brain: {active_model}")
    st.caption("Orchestration: LangGraph + Structured JSON")
    
    st.markdown("### Active Personas")
    st.markdown("- 🏢 **Corporate Exploiter**")
    st.markdown("- 🛠️ **Everyday Opportunist**")
    st.markdown("- 🚀 **Tech Disruptor**")

# Main dashboard area
st.title("🏛️ Jevons Paradox Policy Simulator")
st.markdown("Stress-test urban sustainability policies against an adversarial citizen swarm to discover loopholes and rebound effects.")

policy_input = st.text_area(
    "1. Propose a Policy Draft",
    height=140,
    placeholder="e.g., Ban all gas-powered delivery vans in the city center from 8 AM to 8 PM to reduce carbon emissions..."
)

if st.button("Run Swarm Simulation", type="primary", use_container_width=True):
    if policy_input.strip():
        with st.spinner("🤖 Simulating 3 adversarial cheaters and stress-testing policy with Gemini..."):
            initial_input = {
                "policy_proposal": f"[City: {city_context} | Aggression: {aggression}/10] {policy_input.strip()}",
                "demographic_actions": [],
                "environmental_impact": "",
                "loop_count": 1
            }
            try:
                final_output = simulation_app.invoke(initial_input)
                
                st.success("✅ Simulation complete! 3 cheaters analyzed and individual JSON files created.")
                
                # Render the 3 cheaters in 3 columns
                st.markdown("### 🦹 Adversarial Swarm Loopholes")
                cols = st.columns(3)
                
                actions = final_output.get("demographic_actions", [])
                for i, action in enumerate(actions):
                    with cols[i]:
                        with st.container(border=True):
                            st.subheader(action.get("persona_type", f"Cheater {i+1}"))
                            st.caption(f"Persona alias: **{action.get('agent_name', 'Unknown')}**")
                            st.markdown(f"**Strategy:**\n{action.get('strategy', 'N/A')}")
                            
                            multiplier = action.get("emissions_multiplier", 1.0)
                            st.metric(
                                label="Emissions Multiplier",
                                value=f"{multiplier}x",
                                delta=f"+{round((multiplier - 1.0) * 100, 1)}% emissions" if multiplier > 1.0 else "Neutral"
                            )
                            
                            # Provide direct download for individual JSON
                            json_str = json.dumps(action, indent=4)
                            file_path = action.get("file_path", f"cheater_{i+1}.json")
                            file_name = Path(file_path).name
                            
                            st.download_button(
                                label=f"📥 Download {file_name}",
                                data=json_str,
                                file_name=file_name,
                                mime="application/json",
                                key=f"dl_btn_{i}"
                            )
                
                st.markdown("---")
                st.markdown("### 📋 Environmental Stress-Test & Evaluation Report")
                st.info(final_output.get("environmental_impact", "No report generated."))
                
            except Exception as e:
                st.error(f"Error during simulation execution: {e}")
    else:
        st.warning("Please enter a policy draft before running the simulation.")

