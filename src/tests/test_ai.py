import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.config import engine
from src.models import Base

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test():
    assert True

# TODO TEST AI