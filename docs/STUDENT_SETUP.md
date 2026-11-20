# Student setup — ProfessorX V1

ProfessorX needs (1) student-facing skill instructions, (2) **one** connected `get_teaching_plan` MCP tool, and (3) your authorized course references.

## Recommended: Remote MCP, no Python install

**Verified remote MCP URL:** `https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp`

1. Open [Claude Web](https://claude.ai/) and go to **Customize → Connectors → Add custom connector**.
2. Name the connector **ProfessorX V1 Remote MCP**, set the URL above, choose **No sign in** and add it.
3. In a new chat enable the ProfessorX connector; confirm `get_teaching_plan` appears.
4. Provide the public [SKILL.md](../SKILL.md) to your Claude Project/chat instructions where supported. **Adding MCP does not itself install the skill.**
5. Separately connect **Google Drive** using the account authorized for the [shared course folder](https://drive.google.com/drive/folders/1WH1i14dFTLOAKA-NQZAl279OEFnUWw4o?usp=sharing), or attach the relevant course document. The remote MCP never grants access to course files.
6. Ask ProfessorX to read an authorized course reference **before** invoking `get_teaching_plan` for a normal lesson.

### Remote MCP for other supported clients

Claude Code:

```powershell
claude mcp add --scope user --transport http professorx "https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp"
```

OpenAI Codex:

```powershell
codex mcp add professorx --url "https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp"
```

For other clients, use the HTTP MCP server URL with the client's **Streamable HTTP** connector settings. Client functionality may vary.

## Alternative: Local Python MCP

Install Python 3.11+ and Git, install the bridge, and obtain the instructor-provided Apps Script `/exec` URL:

```powershell
py -m pip install "git+https://github.com/ChandraSekar30/professorX.git"
```

Configure your compatible desktop AI client to run `py -m professorx.mcp_bridge` as a **stdio** MCP server with `PROFESSORX_APPS_SCRIPT_URL` set to the instructor-provided URL. See [full instructions](../README.md#option-b--local-python-mcp-alternative). Use **remote or local**, not both.

## Test connection

For connectivity only, request tool invocation `get_teaching_plan` with `subject=ESD`, `mode=LEARN`, `force_refresh=true` and confirm that it returns `ok=true`, `subject=ESD`, `mode=LEARN`, and exactly these plan keys: `sections`, `checks`, `source_guidance`, `interaction`.

For a normal study request, first verify an actual authorized course source. If the source or MCP is missing, do not claim ProfessorX's guided method is active.

**Privacy:** The remote MCP is public and login-free, but only exposes approved teaching-plan data. It neither verifies student identity nor bypasses Google Drive permissions. Never share owner-only policy files, Apps Script source, gateway secrets or credentials. This service is in a controlled beta; please do not bulk-call it.
