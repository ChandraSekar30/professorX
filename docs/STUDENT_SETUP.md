# Student setup — ProfessorX V2.0.0

ProfessorX needs (1) student-facing skill instructions, (2) **one** connected `get_teaching_plan` MCP tool, and (3) your authorized course references.

## Recommended: Download one ZIP from GitHub

1. Open [ProfessorX on GitHub](https://github.com/ChandraSekar30/professorX) → **Code → Download ZIP**.
2. In **Claude** or **ChatGPT**, choose **Plugins → Upload custom plugin** (when available) and select that *same downloaded source ZIP*. **Do not extract it, re-zip folders, copy `SKILL.md`, or run a build script.**
3. Enable ProfessorX. If the MCP tool is not automatically connected, connect the **ProfessorX Remote MCP** using the URL below.
4. Connect **Google Drive** using your authorized college account, or attach the relevant course materials.
5. Type **ProfessorX setup**. Confirm that a course reference can be read and that `get_teaching_plan` can be invoked.

**Remote MCP URL:** `https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp`

**Claude connector:** Customize → Connectors → Add custom connector → paste the URL → No sign in, when manual connection is necessary. **ChatGPT:** connect or approve the MCP if the interface permits it; account/workspace capabilities differ.

**Beta compatibility note:** GitHub's ZIP wraps the repository inside one directory. Some plugin uploaders do not unwrap it. ChatGPT Web can also label plugins declaring MCP servers as *Desktop only*. The direct GitHub ZIP must pass in **both** ChatGPT and Claude before we call one-ZIP installation verified. No private policy, Apps Script URL, credential or course document is included.

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
