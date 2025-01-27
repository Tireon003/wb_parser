class ParseFailedException(Exception):
    """Exception raised if parser service return error status"""

    def __init__(self, detail: dict[str, str]) -> None:
        super().__init__()
        self.detail = detail


class SaveFailedException(Exception):
    """Exception raised if parser service can't save good to sheets"""

    def __init__(self, detail: dict[str, str]) -> None:
        super().__init__()
        self.detail = detail
