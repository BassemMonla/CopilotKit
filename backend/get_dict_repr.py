from copilotkit import LangGraphAgent
import inspect

try:
    print(inspect.getsource(LangGraphAgent.dict_repr))
except Exception as e:
    print(f"Error: {e}")
