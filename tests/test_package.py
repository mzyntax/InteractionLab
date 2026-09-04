"""Smoke tests for the project package boundary."""


def test_package_imports() -> None:
    import interaction_lab
    import interaction_lab.debate_engine

    assert interaction_lab.__name__ == "interaction_lab"
    assert interaction_lab.debate_engine.__name__ == "interaction_lab.debate_engine"
