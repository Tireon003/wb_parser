import pygsheets
import logging

from config import settings

log = logging.getLogger(__name__)


class GoogleSheetsManager:
    """Google Sheets helper."""

    _PATH_TO_CREDENTIALS = settings.PATH_TO_CREDENTIALS
    _GOOGLE_SHEETS_NAME = settings.GOOGLE_SHEET_NAME

    def __init__(self) -> None:
        self._gc = pygsheets.authorize(service_file=self._PATH_TO_CREDENTIALS)
        self._sh = self._gc.open(self._GOOGLE_SHEETS_NAME)
        self._worksheet = self._sh.sheet1

    def _find_row(self, item_id: int) -> int:
        """
        Method search row by item_id.
        :param item_id: value in first column of the worksheet
        :return: number of found row or first empty row if not found
        """
        current_row = 2
        while True:
            header = self._worksheet.cell(f"A{current_row}")
            if str(item_id) == str(header.value) or not len(header.value):
                return current_row
            current_row += 1

    def update_row(self, *args: tuple[str]) -> None:
        """
        Method push args in a new row or updating existing row by id.
        Row id is the first element of args.
        :param args: row values of columns in concrete order
        :return: None
        """
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        col = 0
        if len(args) > len(letters):
            raise ValueError(
                "Too many args, supports from 1 to 24 args"
            )
        if len(args) < 2:
            raise ValueError(
                "Must provide at least 2 args to update row"
            )
        row_id = self._find_row(args[0])
        for letter in letters:
            self._worksheet.update_value(
                f"{letter}{row_id}",
                args[col],
            )
            col += 1
            if col > len(args) - 1:
                return
