import pytest

from src.processing import filter_by_state, sort_by_date


# Параметризация для filter_by_state
@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("CANCELED", 1),
    ("PENDING", 0),
])
def test_filter_by_state(sample_transactions, state, expected_count):
    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count
    for item in result:
        assert item["state"] == state


# Параметризация для sort_by_date
@pytest.mark.parametrize("descending, expected_order", [
    (True, [1, 3, 2]),    # сначала новые (id 1,3,2 по датам)
    (False, [2, 3, 1]),   # сначала старые
])
def test_sort_by_date(sample_transactions, descending, expected_order):
    result = sort_by_date(sample_transactions, descending)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_order
