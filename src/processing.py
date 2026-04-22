from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    return [item for item in transactions if item.get('state') == state]


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    return sorted(transactions, key=lambda x: x.get('date', ''), reverse=descending)