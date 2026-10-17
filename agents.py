# agents.py
import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import POLICY_EVALUATOR_SYSTEM, ADVERSARIAL_SWARM_SYSTEM

# Define Gemini as the "brain" for your agents
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    verbose=True,
    temperature=0.7,
    google_api_key=os.getenv("GEMINI_API_KEY") # Dev 1 will manage this key in the environment
)

# 1. The Evaluator Agent
policy_evaluator = Agent(
    role="Urban Sustainability Policy Evaluator",
    goal="Identify vulnerabilities and Jevons Paradox resource rebound effects in proposed policies.",
    backstory=POLICY_EVALUATOR_SYSTEM,
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm  # <--- We are now explicitly telling CrewAI to use Gemini
)

# 2. The Swarm Agent
adversarial_citizen = Agent(
    role="Adversarial Citizen Swarm",
    goal="Maximize personal utility by exploiting loopholes in the urban policy.",
    backstory=ADVERSARIAL_SWARM_SYSTEM,
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm  # <--- We are now explicitly telling CrewAI to use Gemini
)
