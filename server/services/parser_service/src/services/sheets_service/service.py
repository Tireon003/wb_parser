import json
import logging

from src.core import GoogleSheetsManager
from src.core.gs import InsertionError
from src.schemas import Good

log = logging.getLogger(__name__)


class SheetsService(GoogleSheetsManager):

    def insert_good_to_sheet(self, good: Good) -> None:
        """
        Method insert good to sheet. Good's data either places on a new row
        or refreshs existing row.
        :param good: instance of good schema
        :return: None
        """
        try:
            good_dict = good.model_dump()
            good_dict["specs"] = json.dumps(good_dict["specs"])
            good_dict["pictures"] = "\n".join(good_dict["pictures"])
            good_args = tuple(good_dict.values())
            self.update_row(*good_args)
        except Exception as e:
            log.error(
                "Insert good to sheet failed. Error message: %s",
                f"{e}",
            )
            raise InsertionError(detail=f"{e}")
