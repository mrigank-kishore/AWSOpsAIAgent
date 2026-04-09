from pathlib import Path


def test_core_docs_exist() -> None:
    assert Path("README.md").exists()
    assert Path("requirement.md").exists()
    assert Path("AGENT_GUIDE.md").exists()
