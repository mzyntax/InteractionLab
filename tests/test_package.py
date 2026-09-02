"""Smoke tests for the project package boundary."""


def test_package_imports() -> None:
    import model_battlegrounds
    import model_battlegrounds.debate_engine

    assert model_battlegrounds.__name__ == "model_battlegrounds"
    assert model_battlegrounds.debate_engine.__name__ == "model_battlegrounds.debate_engine"
