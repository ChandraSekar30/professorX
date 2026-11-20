from pathlib import Path
from professorx import __version__

ROOT = Path(__file__).resolve().parents[1]

def test_public_skill_copies_match():
    paths = [ROOT / "SKILL.md", ROOT / "skills/professorx/SKILL.md"]
    assert len({p.read_bytes() for p in paths}) == 1

def test_public_client_cannot_read_owner_folder():
    src = (ROOT / "src/professorx/mcp_bridge.py").read_text()
    assert "get_teaching_plan" in src
    assert "get_passage" not in src and "search_library" not in src
    assert "DriveApp" not in src

def test_public_release_has_no_owner_code_or_policy():
    assert __version__ == '2.0.0'
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


def test_unified_plugin_structure():
    import json
    root_manifest=json.loads((ROOT/'plugin.json').read_text())
    assert root_manifest['extensions']['com.openai']['onboardingSkill'] == './skills/professorx/SKILL.md'
    assert root_manifest['version'] == '2.0.0'
    assert json.loads((ROOT/'.claude-plugin/plugin.json').read_text())['version'] == '2.0.0'
    assert json.loads((ROOT/'.codex-plugin/plugin.json').read_text())['version'] == '2.0.0'
    assert (ROOT/'.claude-plugin/plugin.json').is_file()


def test_single_source_zip_no_build_script():
    import json
    import tomllib
    pkg = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    assert pkg['project']['version'] == '2.0.0'
    assert not (ROOT / 'scripts/build_plugin_zip.py').exists()
    assert not (ROOT / 'dist').exists()
    assert 'Code → Download ZIP' in (ROOT / 'README.md').read_text()
    assert 'Code → Download ZIP' in (ROOT / 'docs/STUDENT_SETUP.md').read_text()
    for manifest in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
        assert json.loads((ROOT / manifest).read_text())['version'] == '2.0.0'


def test_github_source_zip_layout_ready():
    # GitHub wraps repository files in <repo>-<branch>/; these files live at that wrapper's root.
    required = ('plugin.json', '.claude-plugin/plugin.json',
                '.codex-plugin/plugin.json', 'skills/professorx/SKILL.md',
                )
    assert all((ROOT / item).is_file() for item in required)
