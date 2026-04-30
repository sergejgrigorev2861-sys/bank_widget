"""
Тесты для модуля decorators.
"""

import os
import tempfile

import pytest

from src.decorators import log


def test_log_to_console_success(capsys):
    """Проверяет вывод в консоль при успешном выполнении."""

    @log()
    def add(a, b):
        return a + b

    result = add(3, 5)
    captured = capsys.readouterr()

    assert result == 8
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys):
    """Проверяет вывод в консоль при ошибке."""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


def test_log_to_file_success():
    """Проверяет запись в файл при успешном выполнении."""
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp:
        tmp_path = tmp.name

    @log(filename=tmp_path)
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)
    assert result == 20

    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "multiply ok" in content
    os.unlink(tmp_path)


def test_log_to_file_error():
    """Проверяет запись в файл при ошибке."""
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp:
        tmp_path = tmp.name

    @log(filename=tmp_path)
    def subtract(a, b):
        return a - b

    with pytest.raises(TypeError):
        subtract("10", 5)

    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "subtract error: TypeError. Inputs: ('10', 5), {}" in content
    os.unlink(tmp_path)


def test_log_preserves_function_name():
    """Проверяет, что декоратор сохраняет имя функции."""

    @log()
    def test_func():
        pass

    assert test_func.__name__ == "test_func"
