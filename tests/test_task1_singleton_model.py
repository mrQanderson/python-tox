"""1. Singleton pattern.
Расширить реализацию задания по Company model. Реализовать паттерн синглтон для нового класса Alex, который
наследуется от Engineer, и написать юнит-тесты для проверки того, что паттерн работает правильно."""

import pytest

from src.company.company_model import AlexSingleton


class TestAlexSingleton:
    def test_singleton_can_take_arguments_and_be_instantiated(self, alex_engineer):
        assert alex_engineer is not None
        assert alex_engineer.name == "Olexiy"
        assert alex_engineer.age == 35

    def test_singleton_cannot_be_instantiated_twice(self, alex_engineer):
        with pytest.raises(RuntimeError) as error:
            AlexSingleton(name="Kate", age=36)
        assert str(error.value) == "AlexSingleton class is already instantiated"
        assert AlexSingleton.instance().name == "Olexiy"

    def test_singleton_instance_is_accessible_using_class_method(self, alex_engineer):
        engineer_singleton = AlexSingleton.instance()
        assert engineer_singleton.name == "Olexiy"

    def test_singleton_retains_initial_property_values_after_subsequent_init_calls(
        self, alex_engineer
    ):
        with pytest.raises(RuntimeError):
            AlexSingleton(name="Boris_Jonsonuk", age=37)
        assert AlexSingleton.instance().name == "Olexiy"

    def test_singleton_instance_directly_cannot_be_accesible(self, alex_engineer):
        with pytest.raises(AttributeError) as error:
            alex_engineer.__instance
        assert (
            str(error.value)
            == f"'AlexSingleton' object has no attribute '_TestAlexSingleton__instance'"
        )

    def test_singleton_engineer_join_company(self, company, alex_engineer):
        assert not alex_engineer.is_employed
        alex_engineer.join_company(company)
        assert alex_engineer.is_employed
        assert alex_engineer.company.name == "SpaceX"

    @pytest.mark.dependency(depends=["test_singleton_engineer_join_company"])
    def test_singleton_engineer_makes_money(self, company, alex_engineer):
        assert not alex_engineer._money
        alex_engineer.do_work()
        assert alex_engineer._money == 10
