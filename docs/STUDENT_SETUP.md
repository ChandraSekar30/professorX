# Student setup — ProfessorX

ProfessorX requires **both** the public skill and the teaching-plan MCP tool. For course-grounded answers, your AI must also read authorized reference documents. The MCP is **not optional**.

1. Choose a supported desktop AI client (Claude Code, Codex, Cursor or Gemini CLI). Install Python 3.11+, Node.js 22.20+, and Git.
2. Install the public skill for your agent. Example for Claude Code: `npx skills add ChandraSekar30/professorX --agent claude-code --global`. For other clients, use the agent-specific commands in the [README](../README.md#step-1--install-the-public-professorx-skill).
3. Install the local Python teaching-plan client: on Windows, `py -m pip install "git+https://github.com/ChandraSekar30/professorX.git"`; on macOS/Linux, `python3 -m pip install "git+https://github.com/ChandraSekar30/professorX.git"`.
4. Obtain the instructor-provided ProfessorX teaching gateway URL ending `/exec`. Configure your AI's local **stdio** MCP server to run `py -m professorx.mcp_bridge` (Windows) or `python3 -m professorx.mcp_bridge` (macOS/Linux), with `PROFESSORX_APPS_SCRIPT_URL` set to the gateway URL. See the exact [Claude Code, Codex, Cursor, and Gemini CLI setup](../README.md#step-2--install-and-connect-the-required-teaching-plan-mcp-tool).
5. Verify that your AI exposes the `get_teaching_plan` tool. Without it, ProfessorX setup is incomplete. Installing only a skill is insufficient.
6. Separately provide access to course references: connect your AI to Google Drive through a college account allowed to access the [shared course folder](https://drive.google.com/drive/folders/1WH1i14dFTLOAKA-NQZAl279OEFnUWw4o?usp=sharing), or attach the relevant document to your conversation. Opening the link in your browser doesn't prove your AI can read the content.
7. Ask the AI to read a course reference first and then call `get_teaching_plan` before it generates a ProfessorX-guided explanation.

The `get_teaching_plan` tool accepts `subject` (ESD, PAD, SES, RTES), `mode` (such as LEARN or QUIZ), and an optional `force_refresh` argument. The **tool is mandatory**; only its refresh argument is optional. It retrieves limited teaching guidance, not the instructor's private policy or reference documents. No separate student login is required for the teaching gateway, but Google Drive permissions still apply.

**Compatibility:** Local stdio MCP setup requires an AI client that supports launching local tools. Web/mobile chat interfaces do not automatically execute the local ProfessorX MCP bridge.
