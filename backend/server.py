import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAGUIAgent
from agent import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatchedLangGraphAGUIAgent(LangGraphAGUIAgent):
    def dict_repr(self):
        return {
            'id': self.name,
            'name': self.name,
            'description': self.description or '',
            'type': 'langgraph'
        }

sdk = CopilotKitRemoteEndpoint(
    agents=[
        PatchedLangGraphAGUIAgent(
            name="expense_guardian",
            description="An agent that helps file expenses. It requires approval for expenses over $100.",
            graph=graph,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/api/copilotkit")

def main():
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=5000, reload=True)

if __name__ == "__main__":
    main()
