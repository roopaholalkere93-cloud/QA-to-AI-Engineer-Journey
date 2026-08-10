These commands (/goal, /compact, and /mcp) are specialized control commands used in advanced AI coding environments, development assistants, and agentic CLI tools (such as Claude Code, Kiro, and custom LLM interfaces) to manage autonomous tasks, context length, and external integrations.
1. The /goal Command
The /goal command sets a standing objective or completion condition that allows an AI assistant to run autonomously across multiple turns until the objective is verified and fulfilled.
•	How It Works: Instead of prompting the AI step-by-step, you provide an end state (e.g., /goal get the entire test suite passing). The agent works loop-by-loop. After each turn, an independent evaluator or fast model checks whether the condition holds. If it does not, the agent continues executing instead of returning control to you. 
•	Key Subcommands / Usage:
o	/goal [objective] — Sets the objective and starts the autonomous loop. 
o	/goal status — Outputs the current progress, turn count, elapsed time, and verification state. 
o	/goal clear — Stops and clears the active goal. 
•	Best Used For: Bounded, verifiable, and iterative tasks like fixing failing test suites, migrating code modules, or implementing specific acceptance criteria. 
2. The /compact Command
The /compact command is a context-management utility designed to reduce token usage and optimize memory. 
•	How It Works: As an AI coding or chat session goes on, the context window fills up with long code snippets, tool outputs, and conversational back-and-forth. Running /compact compresses the conversation history—summarizing previous steps, dropping redundant tool results, and retaining only the essential state needed to move forward. 
•	Why It Matters: It prevents context degradation (where models lose focus due to too much noise), lowers API costs, and speeds up response times during long, complex debugging or development sessions.
3. The /mcp Command
The /mcp command manages the Model Context Protocol (MCP), an open standard created by Anthropic that connects AI models securely to external data sources, developer tools, and environments. 
•	How It Works: MCP standardizes how a client host discovers and invokes tools provided by external "MCP servers" (such as databases, local filesystems, GitHub, or custom enterprise APIs). The /mcp command lets you interact with, configure, and troubleshoot these protocol connections directly from your session. 
•	Common Subcommands & Context:
o	Managing connected servers, viewing token weights/schemas of tool origins, and checking server status.
o	Authentication management (e.g., /mcp auth, /mcp logout) for remote or enterprise-secured MCP servers. 
•	Security & Efficiency: MCP shifts how agents pull data; rather than loading massive tool definitions or raw outputs directly into the context window all at once, MCP-compliant environments allow progressive disclosure and code-execution patterns to keep interactions secure and token-efficient

