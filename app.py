# app.py
import streamlit as st

st.set_page_config(page_title="Jevons Paradox Policy Simulator", page_icon="🏙️")

st.title("Jevons Paradox Policy Simulator")
st.markdown("Stress-test urban sustainability policies against an adversarial AI swarm powered by Gemini.")

st.header("1. Propose a Policy")
policy_input = st.text_area(
    "Enter the draft policy here:",
    height=200,
    placeholder="e.g., The city will subsidize energy-efficient smart HVAC systems..."
)

if st.button("Run Swarm Simulation"):
    if policy_input.strip():
        st.info("Sending policy to the Gemini execution engine... (Awaiting Developer 1's API connection)")
    else:
        st.warning("Please enter a policy draft before running the simulation.")
