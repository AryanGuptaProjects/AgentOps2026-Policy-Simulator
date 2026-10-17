from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

# --- TASK 1: The Shared Clipboard (The State) ---
class SimulationState(TypedDict):
    policy_proposal: str           # Box 1: What the mayor typed
    demographic_actions: List[dict]# Box 2: What the AI cheaters write down
    environmental_impact: str      # Box 3: The final report
    loop_count: int                # Box 4: Which simulation month we are in

# --- TASK 2: Building the Nodes (The Steps in the Line) ---

def input_node(state: SimulationState):
    """Step A: Ingests the user's policy proposal."""
    print("-> [Input Node] Policy received successfully.")
    return {"policy_proposal": state["policy_proposal"]}

def swarm_node(state: SimulationState):
    """Step B: The AI Cheaters (Currently using dummy text for Step 1)."""
    print("-> [Swarm Node] Simulating adversarial loophole generation...")
    # Hardcoded dummy response to test our plumbing
    dummy_cheat = {"agent": "Gig Worker", "action": "Using 5 gas scooters instead of 1 van."}
    return {"demographic_actions": [dummy_cheat]}

def evaluator_node(state: SimulationState):
    """Step C: The Evaluator reads the cheats and writes a report."""
    print("-> [Evaluator Node] Analyzing loopholes and generating report...")
    actions = state["demographic_actions"]
    report = f"Dummy Report: Evaluated actions: {actions}. Policy has minor leakage risks."
    return {"environmental_impact": report}


# --- TASK 2 (Continued): Drawing the Flowchart (LangGraph Routing) ---

# 1. Initialize the graph with our state blueprint
workflow = StateGraph(SimulationState)

# 2. Add our three stops (nodes) to the graph
workflow.add_node("input_node", input_node)
workflow.add_node("swarm_node", swarm_node)
workflow.add_node("evaluator_node", evaluator_node)

# 3. Connect the edges (The order of operations: START -> Input -> Swarm -> Evaluator -> END)
workflow.add_edge(START, "input_node")
workflow.add_edge("input_node", "swarm_node")
workflow.add_edge("swarm_node", "evaluator_node")
workflow.add_edge("evaluator_node", END)

# 4. Compile the graph into a runnable app
app = workflow.compile()


# --- TASK 3: The Safety Test (Running with Dummy Text) ---
if __name__ == "__main__":
    print("=== STARTING STEP 1 BACKBONE TEST ===")
    
    # Create test input data
    initial_input = {
        "policy_proposal": "Ban all gas delivery vans in the city center.",
        "demographic_actions": [],
        "environmental_impact": "",
        "loop_count": 1
    }
    
    # Run the graph locally
    final_output = app.invoke(initial_input)
    
    print("\n=== TEST COMPLETE. FINAL SHARED CLIPBOARD OUTPUT ===")
    print(final_output)