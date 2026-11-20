# ProfessorX 🎓

**Study smarter with your own AI assistant.** ProfessorX is an open-source AI Agent Skill for students learning **ESD, PAD, SES and RTES**. It helps your AI assistant explain course concepts, work through questions, revise for exams and practise with quizzes using your course references and ProfessorX teaching guidance.

ProfessorX is **not a separate AI model or website**. It runs inside a compatible AI coding assistant such as **Claude Code, OpenAI Codex, Cursor or Gemini CLI**. You use the AI service you already have access to.

## What can ProfessorX help me do?

- **Understand topics:** request step-by-step explanations, examples and clarification.
- **Solve problems:** work through subject questions and understand the reasoning.
- **Prepare for exams:** practise exam-style responses and previous-paper questions when you supply the papers.
- **Revise:** ask for concise summaries, comparisons and concept reviews.
- **Practise quizzes:** answer questions and receive feedback, one question at a time.

Try prompts such as:

> Use ProfessorX to explain this ESD concept from my course notes, then give me a practice question.

> Use ProfessorX in REVISION mode for PAD. Summarise the important ideas in the attached chapter.

> Use ProfessorX in SOLVE mode for this SES question. Show each step and explain why it is needed.

## How it works

ProfessorX combines **three required pieces**:

1. **The public ProfessorX skill** — tells your AI assistant how to conduct a study session.
2. **The ProfessorX teaching-plan MCP tool** — required. Connect it using **either** the hosted Remote MCP (recommended) **or** the local Python MCP bridge. **Installing the skill alone is not enough.**
3. **Course reference materials** — your assistant must be able to read relevant documents through an authorized Google Drive connection or files you attach. A Drive link alone cannot give an AI access to its contents.

For a course-grounded ProfessorX answer, the assistant checks that it can access a real source **first**, then calls `get_teaching_plan`, and finally explains the answer using the retrieved references and teaching guidance.

**If the MCP tool is missing, ProfessorX setup is incomplete and the assistant must not pretend that ProfessorX teaching guidance is active.** If the course references are inaccessible, connect Drive or attach the document before asking for a reference-grounded answer.

## Before you install

You need an AI client that supports MCP tools, authorized ESD/PAD/SES/RTES reference material, and access to an AI model. Your AI also needs a copy of the ProfessorX skill instructions: install the public skill in a compatible skill-enabled client, or explicitly provide the public [SKILL.md](SKILL.md) to a client that does not install skills automatically.

**Choose one MCP connection method:**

- **Option A — Remote MCP (recommended):** no Python, Node.js or local MCP installation required **for the MCP connection**. Supports Claude Web as confirmed by our integration test and other compatible HTTP MCP clients.
- **Option B — Local MCP (alternative):** requires Python 3.11+, Git, and the instructor-provided Apps Script gateway `/exec` URL. This is for clients that launch stdio MCP servers.

For the `npx skills` installer in a terminal, you also need a compatible Node.js installation. Installing a skill and connecting MCP are separate tasks.

You need permission to read the [ProfessorX shared course reference folder](https://drive.google.com/drive/folders/1WH1i14dFTLOAKA-NQZAl279OEFnUWw4o?usp=sharing), using your college Google account, or the relevant course documents to attach to your AI chat. The MCP server **does not grant Google Drive access**.

## Installation — skill instructions + one MCP connection + course references

### Step 1 — Make the public ProfessorX skill available

For clients with the `npx skills` installer, use one applicable command:

### Step 1 — Install the single GitHub source ZIP (Claude or ChatGPT)

The repository **itself** is the plugin source. The root contains `plugin.json`, `.claude-plugin/plugin.json`, and `skills/professorx/SKILL.md`, plus remote MCP configuration. There is **no second plugin ZIP, no ZIP-generation script and no separate ChatGPT/Claude folders**.

1. Open [ProfessorX on GitHub](https://github.com/ChandraSekar30/professorX).
2. Select **Code → Download ZIP**. Keep the downloaded `professorX-main.zip` (or similarly named branch ZIP) intact; do not re-zip a subfolder.
3. In **Claude** or **ChatGPT**, use **Plugins → Upload custom plugin** where that option is available, and select the downloaded GitHub ZIP.
4. Enable ProfessorX. If the client doesn't automatically activate `get_teaching_plan`, connect the Remote MCP in Step 2. Authorize your own Google Drive account separately, or attach authorized documents.
5. Type **ProfessorX setup**. ProfessorX should verify both the source connection and MCP tool before declaring setup complete.

**Compatibility notice:** GitHub puts all source files under an outer `professorX-main/` folder. Some plugin uploaders require manifest files at the archive root and may reject a GitHub-generated ZIP. Also, ChatGPT Web may treat plugins declaring MCP in `mcp.json` / `.mcp.json` as *Desktop only*. **Direct source-ZIP installation in both clients is not yet verified.** If either installer rejects the ZIP, do not claim this distribution has passed; record the precise error for a structural fix. We won't ask students to generate another archive.

This ZIP does not authorize Google Drive or guarantee MCP connections are enabled automatically.

**Developer / terminal skill installation** (optional):

```powershell
npx skills add ChandraSekar30/professorX --agent claude-code --global
npx skills add ChandraSekar30/professorX --agent codex --global
```

For Cursor and Gemini CLI, see your client's `npx skills` support. These commands install the study skill; MCP configuration remains a separate client-specific step when not automatically provisioned.

### Step 2 — Connect the required teaching-plan MCP tool

Choose **Option A OR Option B**, not both. Both expose `get_teaching_plan`.

#### Option A — Remote MCP (recommended)

Use this exact HTTPS **MCP URL** (including `/mcp`):

```text
https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp
```

This is the Cloudflare Worker endpoint, **not** the Google Apps Script `/exec` URL. Students do not need the Apps Script URL or access to the private gateway.

**Claude Web (tested)**

1. Open [Claude Web](https://claude.ai/) → **Customize → Connectors** → **Add custom connector** (menu labels may vary).
2. Name it **ProfessorX Remote MCP**; paste the MCP URL above.
3. Choose **No sign in** and no custom headers; add the connector.
4. In a new chat enable the ProfessorX connector in **Connectors/Tools**.
5. Check that `get_teaching_plan` is available. Your Google Drive connector is a separate connection, requiring your own authorized account.

**Claude Code (HTTP MCP)**

```powershell
claude mcp add --scope user --transport http professorx "https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp"
```

Check with `claude mcp list` and `/mcp` in Claude Code.

**OpenAI Codex (HTTP MCP)**

```powershell
codex mcp add professorx --url "https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp"
```

Check with `codex mcp list` or `/mcp`.

**Other clients:** If your client supports Streamable HTTP MCP, add the same `/mcp` URL using its HTTP MCP settings. If not, choose Option B. Client availability and interface labels can change.

#### Option B — Local Python MCP (alternative)

ProfessorX also supports a local Python MCP bridge.

This is an alternative to the Remote MCP and requires
separate owner-side configuration.

For normal student installation, use Option A — Remote MCP.

Students do not need the Google Apps Script gateway URL,
local Python MCP, or owner-only credentials.

## Common problems

| Problem | What to do |
|---|---|
| Skill installed, but no `get_teaching_plan` tool | Connect **either** remote or local MCP in Step 2 and enable the connector. |
| Remote MCP unavailable | Verify the exact HTTPS URL ends with `/mcp`, and check client connection status; ask the instructor if the service is down. |
| Local MCP unavailable | Check the `/exec` gateway URL, Python environment and stdio configuration. |
| Claude Web connector works but ProfessorX style is absent | The MCP connector does not install `SKILL.md`; provide the public skill text using your available project/chat instruction feature. |
| Drive folder opens in browser but AI cannot read it | Configure an authorized Drive connection in your AI client or attach the actual course file. |
| Assistant cannot find supporting course material | It must say so; never invent citations, page numbers or source contents. |
| Client cannot use HTTP MCP | Use Option B if the client supports local stdio MCP; otherwise use a supported client. |

## Privacy and source handling

The public repository contains the student-facing skill and local MCP client, **not** the instructor's original private teaching instructions, private Drive contents, credentials or Apps Script gateway source. The MCP tool receives only limited teaching-plan guidance; that returned guidance can be inspected by your AI client. The course materials remain governed by the Google Drive permissions your instructor has assigned. ProfessorX does not independently verify student identity for its teaching gateway. The remote MCP endpoint is publicly callable; course document access must be independently enforced by the student's Drive connection. The teaching gateway returns approved limited plan fields, not protected course documents.

See the [student setup guide](docs/STUDENT_SETUP.md) for detailed installation instructions.

---

ProfessorX is an academic learning aid, not a substitute for checking your course material or your instructor's directions. It should cite only sources it has actually accessed.
