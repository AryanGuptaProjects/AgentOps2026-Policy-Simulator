# tasks.py
from crewai import Task
from agents import policy_evaluator, adversarial_citizen

def create_evaluation_task(policy_text: str):
    """Creates a task for the evaluator to stress-test the given policy."""
    return Task(
        description=f"Evaluate the following urban policy for Jevons Paradox vulnerabilities:\n\n{policy_text}",
        expected_output="A structured report detailing primary intent, vulnerabilities, and projected rebound effects.",
        agent=policy_evaluator
    )

def create_exploitation_task(policy_text: str):
    """Creates a task for the adversarial swarm to find loopholes in the given policy."""
    return Task(
        description=f"Analyze the following urban policy and find loopholes to exploit for maximum personal utility:\n\n{policy_text}",
        expected_output="A list of specific loopholes and the economic incentives driving the exploitation.",
        agent=adversarial_citizen
    )
