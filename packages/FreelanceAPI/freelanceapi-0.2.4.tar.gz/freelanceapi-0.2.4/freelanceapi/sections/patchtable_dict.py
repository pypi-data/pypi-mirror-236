from typing import Dict

from ..utils import Classify, dict_zip_data
from .__SectionDict import __SectionDict


class PatchtableDict(__SectionDict):
    """
    AreaDict A Area string is converted to a Dict.
    """

    __keys: list[str] = [
        "ID", "NA", "MT", "LB", "NI1", "NI2", "NI3", "NI4", "PO", "NI5", "NI6", "NI7", "NI8", "NI9", "NI10", "NI11",
        "NI12", "NI13", "NI14", "NI15", "NI16", "NI17", "NI18"
        ]

    def merge_dict(self, splitted_data: tuple[str]) -> Dict[str, str]:
        print(len(self.__keys))
        """
        merge_dict Merge data for Dataprocessing.
        Returns:
            Dict: A ProjectDict separated by the predefined separator
        """
        data_as_dict = {}
        classify = Classify(splitted_data)
        return data_as_dict | classify.execute(dict_zip_data(self.__keys))
