from copilotkit import CopilotKitRemoteEndpoint
import inspect

try:
    print(inspect.getsource(CopilotKitRemoteEndpoint.info))
except Exception as e:
    print(f"Error getting info source: {e}")

try:
    print(inspect.getsource(CopilotKitRemoteEndpoint.__init__))
except Exception as e:
    print(f"Error getting init source: {e}")
