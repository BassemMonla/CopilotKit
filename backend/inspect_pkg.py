import copilotkit
print("copilotkit dir:", dir(copilotkit))

try:
    import copilotkit.integrations.langgraph
    print("copilotkit.integrations.langgraph dir:", dir(copilotkit.integrations.langgraph))
except ImportError as e:
    print("copilotkit.integrations.langgraph import failed:", e)

try:
    from copilotkit import LangGraphAGUIAgent
    print("Imported LangGraphAGUIAgent from copilotkit")
except ImportError:
    print("Could not import LangGraphAGUIAgent from copilotkit")
