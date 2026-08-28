"""Smoke tests for the project package boundary."""


def test_package_imports() -> None:
    import polar_debate
    import polar_debate.debate_engine

    assert polar_debate.__name__ == "polar_debate"
    assert polar_debate.debate_engine.__name__ == "polar_debate.debate_engine"
