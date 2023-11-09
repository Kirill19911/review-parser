import pandas as pd
import gspread
from typing import Optional
from dataclasses import dataclass
import datetime

#path to the cred file
json_keyfile = "./google_creds.json"

HOME_WORKSHEET = "https://docs.google.com/spreadsheets/d/1zOPPIcIQo33WWv5OrJA0S2-HWXiVBEnQ8399GFSPOMI"
SHEET = "Sheet1"
CELL_RANGE = "A:H"

gc = gspread.service_account(filename="./google_creds.json")


@dataclass
class ReviewDataObject:
    total_review_count: int
    one_star_reviews: int
    two_star_reviews: int
    three_star_reviews: int
    four_star_reviews: int
    five_star_reviews: int
    total_raiting: float
    timestamp: datetime = str(datetime.datetime.now())


@dataclass
class ReviewSheet:
    worksheet_url: str 
    sheet_name: str

    def _get_working_sheet(self) -> None:
        return gc.open_by_url(self.worksheet_url).worksheet(self.sheet_name)
    
    
    def add_new_sheet_row(self, review_data: ReviewDataObject, range: str) -> None:
        worksheet = self._get_working_sheet()
        worksheet.append_row(values=list(review_data.__dict__.values()), table_range=range)

        
    def print_all_non_empty_cells(self) -> None:
        print(self._get_working_sheet().get_all_values())

    

# rev = ReviewDataObject(23,4,3,5,6,7,2.0)
# review_s = ReviewSheet(HOME_WORKSHEET, SHEET)
# review_s.print_all_non_empty_cells()
# review_s.add_new_sheet_row(rev, "A:H")