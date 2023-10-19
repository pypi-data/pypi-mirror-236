import pytest

try:
    from ampel.contrib.hu.t2.T2RunParsnip import T2RunParsnip
except ImportError as exc:
    pytest.skip(f"could not import T2RunParsnip: {exc}")


@pytest.fixture(scope="session")
def parsnip_model():
    ...

def test_parsnip():

    T2RunParsnip()