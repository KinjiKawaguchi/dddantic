import pytest

from examples import guardrails


def test_guardrails_example_runs_and_reports(capsys: pytest.CaptureFixture[str]):
    guardrails.main()
    out = capsys.readouterr().out

    # Four definition-time rejections plus the frozen-immutability rejection.
    assert out.count("rejected:") == 5
    assert "NOT rejected" not in out

    assert "value equality: Money(100, USD) == Money(100, USD) -> True" in out
    assert "identity equality: same id, different fields -> equal? True" in out
    assert "events: collected 1, pending after draining 0" in out
