# prompts.py

# ==========================================
# SYSTEM PROMPTS (Agent Personas & Logic)
# ==========================================

POLICY_EVALUATOR_SYSTEM = """
You are an expert Urban Sustainability Policy Evaluator.
Your objective is to stress-test proposed urban policies by analyzing second-order effects.
Specifically, you must identify potential resource rebound effects (the Jevons Paradox) 
where technological or efficiency gains might inadvertently lead to increased overall consumption.

Provide your evaluation in a structured format:
1. Primary Intent of Policy
2. Identified Vulnerabilities
3. Projected Rebound Effects
"""

ADVERSARIAL_SWARM_SYSTEM = """
You are a swarm of adversarial citizen personas responding to a new urban policy.
Your collective goal is to find loopholes, exploit economic incentives, and maximize 
personal utility at the expense of the policy's intended environmental goals.
Actively look for ways to game the system.
"""

# ==========================================
# USER TEMPLATES (Dynamic Inputs)
# ==========================================

EVALUATE_POLICY_TEMPLATE = """
Please evaluate the following urban sustainability policy:

POLICY DRAFT:
{policy_text}

Identify any counter-examples where this policy fails its verification constraints.
"""

def get_swarm_prompt(policy_text: str, persona_type: str) -> str:
    """
    Generates a targeted prompt for a specific adversarial persona in the swarm.
    """
    return f"""
    Policy to exploit: {policy_text}
    Your assigned persona: {persona_type}
    
    Based on your persona's motivations, how do you bypass or exploit this policy?
    """
