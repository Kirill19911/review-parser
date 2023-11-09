from parsing import ReviewProcessor

import gspread
import os
import logging
import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
import json

load_dotenv()
LINK_TO_PARSE = os.environ["LINK_TO_PARSE"]
HOME_WORKSHEET = os.environ["HOME_WORKSHEET"]
SHEET = os.environ["SHEET"]
CELL_RANGE = os.environ["CELL_RANGE"]
JSON_GOOGLE_CREDS =json.loads(os.environ["JSON_GOOGLE_CREDS"])


logging.basicConfig(level=logging.INFO)
gc = gspread.service_account_from_dict(JSON_GOOGLE_CREDS)


@dataclass
class ReviewSheet:
    worksheet_url: str 
    sheet_name: str

    def _get_working_sheet(self) -> None:
        return gc.open_by_url(self.worksheet_url).get_worksheet(self.sheet_name)
    
    def add_new_sheet_row(self, review_data: list, range: str) -> None:
        worksheet = self._get_working_sheet()
        worksheet.append_row(values=review_data, table_range=range)
 
    def print_all_non_empty_cells(self) -> None:
        print(self._get_working_sheet().get_all_values())


def main():
    
    rp = ReviewProcessor(LINK_TO_PARSE)
    rp.init_soup()

    all_data_dict = {}

    all_data_dict.update(rp.get_per_star_review_count())
    all_data_dict.update(rp.get_total_review_count())
    all_data_dict.update(rp.get_rating())
    all_data_dict["update_time"] = str(datetime.datetime.now())
    logging.info(f"{all_data_dict}: data for adding to Google sheets")

    rs = ReviewSheet(HOME_WORKSHEET, int(SHEET))
    rs.add_new_sheet_row(review_data=list(all_data_dict.values()), range=CELL_RANGE)
    logging.info(f"A new row has been added")

if __name__ == "__main__":
    main()
