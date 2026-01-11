from copilotkit import LangGraphAgent

if hasattr(LangGraphAgent, 'dict_repr') or hasattr(LangGraphAgent('test', 'test', None), 'dict_repr'):
    print("LangGraphAgent has dict_repr")
else:
    print("LangGraphAgent DOES NOT HAVE dict_repr")
