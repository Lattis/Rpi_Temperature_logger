import gspread
import logging
import GDocsException
from gspread.exceptions import SpreadsheetNotFound

class GDocs(object):
    
    log = logging.getLogger("GDocs")
    worksheet = None
    
    def __init__(self, email, api_key):
        self._email = email
        self._api_key = api_key
    
    def initialize(self):
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        self.gc = gspread.login(self._email, self._api_key)
        self.log.info("Connected to Google Docs.")
        
    def open_spreadsheet(self, spreadsheet_name):
        try:
            self.worksheet = self.gc.open(spreadsheet_name).sheet1
            self.log.info
        except SpreadsheetNotFound as e:
            self.log.error("Spreadsheet not found.", e)
            raise GDocsException(e)
    
    def write_value(self, col, row, value):
        self.worksheet.update_cell(row, col, value)
        self.log.debug("Value '{0}' was written into cell [{1},{2}].".format(value, col, row))
    