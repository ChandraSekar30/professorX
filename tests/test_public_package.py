from pathlib import Path
from professorx import __version__

ROOT = Path(__file__).resolve().parents[1]

def test_public_skill_copies_match():
    paths = [ROOT / "SKILL.md", ROOT / "skills/professorx/SKILL.md",
             ROOT / "plugins/professorX/skills/professorx-study/SKILL.md"]
    assert len({p.read_bytes() for p in paths}) == 1

def test_public_client_cannot_read_owner_folder():
    src = (ROOT / "src/professorx/mcp_bridge.py").read_text()
    assert "get_teaching_plan" in src
    assert "get_passage" not in src and "search_library" not in src
    assert "DriveApp" not in src

def test_public_release_has_no_owner_code_or_policy():
    assert __version__ == '0.6.2b1'
    assert not (ROOT / "apps-script").exists()
    assert not (ROOT / "src/professorx/auth.py").exists()
    assert not (ROOT / "src/professorx/drive_sync.py").exists()
    assert not (ROOT / "docs/PRIVATE_POLICY_TEMPLATE.example.json").exists()


def test_remote_mcp_documented_and_skill_synced():
    url = "https://professorx-remote-mcp.professorx-chandrasekar.workers.dev/mcp"
    assert url in (ROOT / "README.md").read_text()
    assert url in (ROOT / "docs/STUDENT_SETUP.md").read_text()
    assert url in (ROOT / "SKILL.md").read_text()
    assert "Option A — Remote MCP" in (ROOT / "README.md").read_text()
    assert "Option B — Local Python MCP" in (ROOT / "README.md").read_text()
