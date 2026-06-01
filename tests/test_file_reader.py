from unittest.mock import Mock, patch

from src.file_reader import read_csv_transactions, read_excel_transactions


def test_read_csv_success():
    """Успешное чтение CSV."""
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    mock_df.fillna.return_value = mock_df

    with patch('pathlib.Path.exists', return_value=True):
        with patch('pandas.read_csv', return_value=mock_df):
            result = read_csv_transactions("any.csv")
            assert result == [{"id": 1, "amount": 100}]


def test_read_csv_file_not_found():
    """CSV файл не найден."""
    with patch('pathlib.Path.exists', return_value=False):
        result = read_csv_transactions("missing.csv")
        assert result == []


def test_read_csv_exception():
    """Ошибка при чтении CSV."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pandas.read_csv', side_effect=Exception("Read error")):
            result = read_csv_transactions("bad.csv")
            assert result == []


def test_read_excel_success():
    """Успешное чтение Excel."""
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1, "amount": 200}]
    mock_df.fillna.return_value = mock_df

    with patch('pathlib.Path.exists', return_value=True):
        with patch('pandas.read_excel', return_value=mock_df):
            result = read_excel_transactions("any.xlsx")
            assert result == [{"id": 1, "amount": 200}]


def test_read_excel_file_not_found():
    """Excel файл не найден."""
    with patch('pathlib.Path.exists', return_value=False):
        result = read_excel_transactions("missing.xlsx")
        assert result == []


def test_read_excel_exception():
    """Ошибка при чтении Excel."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pandas.read_excel', side_effect=Exception("Read error")):
            result = read_excel_transactions("bad.xlsx")
            assert result == []
