import pytest
from .company_model import Company, AlexSingleton


@pytest.fixture(name="alex_engineer", scope="session")
def create_singleton_instance():
    alex = AlexSingleton(name="Olexiy", age=35)
    return alex


@pytest.fixture(name="company", scope="function", autouse=True)
def create_company():
    space_company = Company('SpaceX', address='1 Rocket Road, East Hawthorne neighborhood, CA, Hawthorne, 90250, USA')
    return space_company
