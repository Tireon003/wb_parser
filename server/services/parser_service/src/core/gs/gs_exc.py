class InsertionError(Exception):
    """Exception raises when insertion to Google Sheets failed"""

    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail
