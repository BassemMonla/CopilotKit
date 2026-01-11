from copilotkit import LangGraphAGUIAgent, LangGraphAgent
import inspect

print("--- LangGraphAGUIAgent ---")
print(dir(LangGraphAGUIAgent))
print("\nMethods:")
for name, method in inspect.getmembers(LangGraphAGUIAgent, predicate=inspect.isfunction):
    print(name)

print("\n--- LangGraphAgent ---")
print(dir(LangGraphAgent))
