import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

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
# We use gemini-3.8-flash (the latest recommended model supporting structured outputs)
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
    """Task 1 & 3 Test: Getting structured JSON from Gemini using a simple prompt."""
    print("-> [Swarm Node] Asking Gemini for a loophole strategy in JSON format...")
    
    policy = state["policy_proposal"]
    
    # Simple test prompt (Task 2 multi-persona prompts will be added later)
    prompt = f"Given this city policy: '{policy}', write a brief loophole strategy from a delivery driver perspective."
    
    # Invoke Gemini with structured output enforcement
    result: LoopholeResponse = structured_gemini_llm.invoke([HumanMessage(content=prompt)])
    
    agent_result = {
        "agent": result.agent_name,
        "action": result.strategy,
        "emissions_multiplier": result.emissions_multiplier
    }
    
    print(f"   [✓] Gemini successfully returned structured JSON!")
    
    return {"demographic_actions": [agent_result]}

def evaluator_node(state: SimulationState):
    """The Evaluator: Reviews the loophole and writes a report."""
    print("-> [Evaluator Node] Analyzing Gemini's output...")
    
    policy = state["policy_proposal"]
    actions = state["demographic_actions"]
    
    prompt = f"Policy: {policy}\n\nWorkaround: {actions}\nWrite a short evaluation report on the environmental risk."
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
    print("=== STARTING GEMINI API & STRUCTURED OUTPUT TEST ===")
    
    initial_input = {
        "policy_proposal": "Ban all gas-powered delivery vans in the city center.",
        "demographic_actions": [],
        "environmental_impact": "",
        "loop_count": 1
    }
    
    final_output = app.invoke(initial_input)
    
    print("\n=== FINAL TEST OUTPUT ===")
    print(f"Policy: {final_output['policy_proposal']}\n")
    print("Structured JSON Output from Gemini:")
    for action in final_output['demographic_actions']:
        print(f" - Agent: {action['agent']}")
        print(f" - Strategy: {action['action']}")
        print(f" - Multiplier: {action['emissions_multiplier']}x")
    print(f"\nEvaluator Report:\n{final_output['environmental_impact']}")