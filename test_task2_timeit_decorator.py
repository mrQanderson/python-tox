"""2. Decorator with parameters.
Реализуйте @timeit() декоратор который может принимать необязательный параметр threshold и покройте его юнит-тестами.

Пример:
@timeit(threshold=0.5)
def some_heavy_function():
    # complecated code goes here
    pass

@timeit()
def another_function():
    pass

Примечания:
•	параметр threshold принимает значение в секундах
•	декоратор должен печатать время выполнения если оно превышает значение указаное в threshold
•	если threshold не указан - декоратор должен печатать любое время выполнения"""

import time
from functools import wraps

import pytest


def timeit(threshold=None):
    def decorator(func):
        @wraps(func)
        def wrapper_func():
            if isinstance(threshold, (int, float)) or threshold is None:
                start_time = time.time()
                func()
                length_time = time.time() - start_time
                if threshold is None or length_time > threshold:
                    return length_time
                else:
                    raise RuntimeWarning(
                        "Running time is {:.3f} seconds - less than expected {:.3} seconds".format(
                            length_time, float(threshold)
                        )
                    )
            else:
                raise TypeError(
                    "Threshold has to be type int or float. Please check input type."
                )

        return wrapper_func

    return decorator


class TestTimeitDecorator:
    @pytest.mark.parametrize(
        "threshold,sleep_time",
        [
            pytest.param(None, 2, id="Threshold isn't defined"),
            pytest.param(1, 2, id="Threshold is less than runtime"),
        ],
    )
    def test_timeit_decorator_returns_func_runtime(self, threshold, sleep_time):
        @timeit(threshold=threshold)
        def hello_world():
            """Original function"""
            time.sleep(sleep_time)
            return "Hello"

        runtime = hello_world()
        assert (
            runtime > sleep_time
        ), f"Running time less than define as {threshold} seconds"
        assert hello_world.__name__ == "hello_world"
        assert hello_world.__doc__ == "Original function"

    @pytest.mark.parametrize(
        "threshold,sleep_time",
        [pytest.param(2.0, 1, id="Threshold is bigger than runtime")],
    )
    def test_timeit_decorator_returns_runtime_error(self, threshold, sleep_time):
        @timeit(threshold=threshold)
        def hello_world():
            """Original function"""
            time.sleep(sleep_time)
            return "Hello"

        with pytest.raises(RuntimeWarning) as error:
            hello_world()
        assert f"less than expected {threshold} seconds" in str(error.value)

    @pytest.mark.parametrize(
        "threshold,sleep_time", [pytest.param("1", 2, id="Threshold arg is str type")]
    )
    def test_timeit_decorator_returns_type_error(self, threshold, sleep_time):
        @timeit(threshold=threshold)
        def hello_world():
            """Original function"""
            time.sleep(sleep_time)
            return "Hello"

        with pytest.raises(TypeError) as error:
            hello_world()
        assert (
            str(error.value)
            == f"Threshold has to be type int or float. Please check input type."
        )
