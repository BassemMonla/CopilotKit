from copilotkit.agent import Agent
import inspect

try:
    print(inspect.getsource(Agent.dict_repr))
except Exception as e:
    print(f"Error: {e}")
