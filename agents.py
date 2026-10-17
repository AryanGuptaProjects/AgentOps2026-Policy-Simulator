# agents.py
from crewai import Agent
from prompts import POLICY_EVALUATOR_SYSTEM, ADVERSARIAL_SWARM_SYSTEM

# 1. The Evaluator Agent
policy_evaluator = Agent(
    role="Urban Sustainability Policy Evaluator",
    goal="Identify vulnerabilities and Jevons Paradox resource rebound effects in proposed policies.",
    backstory=POLICY_EVALUATOR_SYSTEM,
    verbose=True,
    allow_delegation=False
)

# 2. The Swarm Agent
adversarial_citizen = Agent(
    role="Adversarial Citizen Swarm",
    goal="Maximize personal utility by exploiting loopholes in the urban policy.",
    backstory=ADVERSARIAL_SWARM_SYSTEM,
    verbose=True,
    allow_delegation=False
)
