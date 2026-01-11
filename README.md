# CopilotKit Expense Guardian Demo

This project is a demonstration of a human-in-the-loop AI agent using **CopilotKit**, **LangGraph**, **FastAPI**, and **Next.js**.

## 🏗️ Architecture

The application consists of two main components:

1.  **Backend (Python/FastAPI)**:
    -   Hosts the AI Agent logic using **LangGraph**.
    -   Exposes the agent via **CopilotKit Remote Endpoint**.
    -   Handles expense filing logic and approval workflows.
2.  **Frontend (TypeScript/Next.js)**:
    -   Provides the chat interface using **CopilotKit's React UI** (`CopilotSidebar`).
    -   Connects to the backend to stream agent responses.

### Interaction Flow
1.  User types a request (e.g., "File expense of $105") in the Frontend Sidebar.
2.  CopilotKit SDK forwards the request to the FastAPI Backend.
3.  The **LangGraph Agent** processes the request:
    -   If amount <= $100: Calls the `file_expense` tool directly.
    -   If amount > $100: Interrupts execution and requests "Human Approval".
4.  The Agent's state and response are streamed back to the Frontend.

---

## 🛠️ Code Overview

### Backend (`/backend`)

**`agent.py`**
Defines the LangGraph workflow:
-   **State**: `AgentState` containing messages.
-   **Nodes**:
    -   `agent`: The LLM (GPT-4o) that decides which tool to call.
    -   `tools`: Executes the `file_expense` tool.
    -   `approval_check`: Handles the human-in-the-loop interruption logic.
-   **Edges**: Conditional logic (`should_continue`) checks if the expense amount exceeds $100.

**`server.py`**
The FastAPI entry point:
-   Initializes `CopilotKitRemoteEndpoint`.
-   **Important Patch**: Contains a `PatchedLangGraphAGUIAgent` class. This works around a compatibility issue where `LangGraphAGUIAgent` was missing the `dict_repr` method required by the SDK.
-   Run logic: Starts the server on port `5000`.

### Frontend (`/frontend`)

**`app/page.tsx`**
The main application page:
-   Wraps content in `<CopilotKit>` provider pointing to `http://localhost:5000/api/copilotkit/`.
-   Renders `<CopilotSidebar>` for the chat interface.

**`app/layout.tsx`**
Global layout:
-   **Fix**: Added `suppressHydrationWarning` to the `html` tag to resolve Next.js hydration mismatch errors caused by browser extensions or dynamic injections.

---

## 🚀 Getting Started

### Prerequisites
-   Python 3.11+
-   Node.js 18+
-   OpenAI API Key

### 1. Backend Setup
```bash
cd backend
# Create .env file with OPENAI_API_KEY=...
pip install -r requirements.txt
python server.py
# Server runs at http://localhost:5000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:3000
```

## 🐛 Troubleshooting & Fixes Applied

during development, we resolved:
1.  **Backend Crash**: Initialized a patched agent class to fix an `AttributeError` in the CopilotKit SDK libraries.
2.  **Frontend Hydration**: Fixed a "Client-side exception" by suppressing hydration warnings in `layout.tsx`.
3.  **Agent Visibility**: Verified agent registration at `/api/copilotkit/info`.

**Note**: Ensure your Frontend `@copilotkit/react-core` version is compatible with the Python SDK backend.
