from copilotkit import LangGraphAgent, LangGraphAGUIAgent
import inspect

print("--- LangGraphAgent.__init__ Source ---")
try:
    print(inspect.getsource(LangGraphAgent.__init__))
except Exception as e:
    print(f"Could not get source: {e}")

print("\n--- LangGraphAGUIAgent MRO ---")
print(LangGraphAGUIAgent.mro())

print("\n--- LangGraphAGUIAgent dict_repr check ---")
print(f"Has dict_repr: {hasattr(LangGraphAGUIAgent, 'dict_repr')}")
