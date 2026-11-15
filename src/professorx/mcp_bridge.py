"""Public ProfessorX student-side MCP bridge.

This runs on the student's computer. It only requests selected teaching plans
from the owner's remote gateway, not files from the private teaching Drive.
"""
from __future__ import annotations

from .teaching_client import request_teaching_plan


def main():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("ProfessorX Study")

    @mcp.tool()
    def get_teaching_plan(subject: str, mode: str = "LEARN", force_refresh: bool = False) -> dict:
        """Get limited ProfessorX teaching guidance for ESD/PAD/SES/RTES.

        Use once at session start after checking actual reference availability.
        Refresh when subject/mode changes, at new sessions, or after context
        loss; cached results can be reused for related questions.
        This tool never retrieves the owner's original private policy file.
        """
        return request_teaching_plan(subject, mode, force_refresh)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
