import os
import json
from pathlib import Path
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from prompts import SWARM_PERSONAS, get_swarm_prompt

# --- Load Environment Variables ---
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY. Please set it in your .env file.")

# --- TASK 3: Define the Structured Output Schema (JSON Enforcement) ---
class LoopholeResponse(BaseModel):
    agent_name: str = Field(description="The name of the persona or agent.")
    strategy: str = Field(description="The exact loophole or workaround strategy.")
    emissions_multiplier: float = Field(description="Estimated factor by which emissions increase (e.g., 1.5).")

# --- The Shared Clipboard (State) ---
class SimulationState(TypedDict):
    policy_proposal: str           
    demographic_actions: List[dict]
    environmental_impact: str      
    loop_count: int                

# --- TASK 1: Initialize Gemini API Connection ---
# Defaults to gemini-3.8-flash for reliable free-tier quota and structured output support
gemini_llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
    temperature=0.7,
    google_api_key=api_key,
)

# Bind our Pydantic schema so Gemini is forced to return JSON matching LoopholeResponse
structured_gemini_llm = gemini_llm.with_structured_output(LoopholeResponse)


# --- NODES ---

def input_node(state: SimulationState):
    """Ingests the user's policy proposal."""
    print(f"-> [Input Node] Processing policy: '{state['policy_proposal']}'")
    return {"policy_proposal": state["policy_proposal"]}

def swarm_node(state: SimulationState):
    """Generates loophole strategies for the 3 cheater personas and writes individual JSON files."""
    print("-> [Swarm Node] Generating 3 adversarial cheater personas using Gemini...")
    
    policy = state["policy_proposal"]
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    agent_results = []
    
    for idx, (persona_name, persona_desc) in enumerate(SWARM_PERSONAS.items(), start=1):
        print(f"   [+] Querying persona {idx}/3: '{persona_name}'...")
        prompt = get_swarm_prompt(policy, persona_name, persona_desc)
        
        # Invoke Gemini with structured output enforcement
        result: LoopholeResponse = structured_gemini_llm.invoke([HumanMessage(content=prompt)])
        
        cheater_data = {
            "agent_name": result.agent_name if result.agent_name else persona_name,
            "persona_type": persona_name,
            "strategy": result.strategy,
            "emissions_multiplier": result.emissions_multiplier
        }
        
        # Write individual JSON file for this cheater
        clean_name = persona_name.lower().replace(" ", "_")
        json_file_path = output_dir / f"cheater_{idx}_{clean_name}.json"
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(cheater_data, f, indent=4)
            
        cheater_data["file_path"] = str(json_file_path)
        agent_results.append(cheater_data)
        print(f"       [✓] Saved individual JSON: {json_file_path}")
    
    return {"demographic_actions": agent_results}

def evaluator_node(state: SimulationState):
    """The Evaluator: Reviews the loopholes found by the 3 cheaters and writes a report."""
    print("-> [Evaluator Node] Analyzing all cheater outputs and evaluating rebound effects...")
    
    policy = state["policy_proposal"]
    actions = state["demographic_actions"]
    
    # Format the 3 cheater strategies for the evaluator
    actions_summary = "\n".join([
        f"- {a['agent_name']} ({a['persona_type']}): {a['strategy']} (Emissions Multiplier: {a['emissions_multiplier']}x)"
        for a in actions
    ])
    
    prompt = f"""
Policy Under Evaluation:
{policy}

Adversarial Swarm Loophole Strategies Identified:
{actions_summary}

Write a comprehensive policy stress-test evaluation report:
1. Primary Intent of Policy
2. Vulnerability Breakdown (how the loopholes compromise the policy)
3. Projected Rebound Effects (Jevons Paradox & environmental impact)
4. Recommended Policy Patch
"""
    response = gemini_llm.invoke([HumanMessage(content=prompt)])
    
    # Extract clean text from Gemini response
    content = response.content
    if isinstance(content, list):
        text_content = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in content])
    else:
        text_content = str(content)
        
    return {"environmental_impact": text_content}


# --- DRAWING THE FLOWCHART ---
workflow = StateGraph(SimulationState)

workflow.add_node("input_node", input_node)
workflow.add_node("swarm_node", swarm_node)
workflow.add_node("evaluator_node", evaluator_node)

workflow.add_edge(START, "input_node")
workflow.add_edge("input_node", "swarm_node")
workflow.add_edge("swarm_node", "evaluator_node")
workflow.add_edge("evaluator_node", END)

app = workflow.compile()


# --- TESTING THE GEMINI PIPELINE ---
if __name__ == "__main__":
    print("=== STARTING 3-CHEATER SWARM & JSON GENERATION TEST ===")
    
    initial_input = {
        "policy_proposal": "Ban all gas-powered delivery vans in the city center.",
        "demographic_actions": [],
        "environmental_impact": "",
        "loop_count": 1
    }
    
    final_output = app.invoke(initial_input)
    
    print("\n=== FINAL TEST OUTPUT ===")
    print(f"Policy: {final_output['policy_proposal']}\n")
    print("Generated 3 Cheater Personas:")
    for action in final_output['demographic_actions']:
        print(f" - [{action['persona_type']}] {action['agent_name']}: {action['strategy']}")
        print(f"   Multiplier: {action['emissions_multiplier']}x | Saved to: {action['file_path']}")
    print(f"\nEvaluator Report:\n{final_output['environmental_impact']}")