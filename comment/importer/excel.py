import openpyxl
from random import randint
from config import ExcelInputData

class ImportExcel(object):

    def __init__(self):
        self.file_path = ExcelInputData.FILE_PATH

    def open_work_sheet(self, sheet_name):
        work_book = openpyxl.load_workbook(self.file_path, data_only=True)
        work_sheet = work_book.get_sheet_by_name(sheet_name)
        return work_sheet

    def get_column_by_letter(self, letter):
        return openpyxl.utils.cell.column_index_from_string(letter) - 1

    def getAccountsFromWorkSheet(self, sheet_name):
        datas = []
        try:
            work_sheet = self.open_work_sheet(sheet_name)
            for index, current_row in enumerate(work_sheet.rows):
                if index > 0:
                    name = current_row[self.get_column_by_letter(ExcelInputData.COLUMN_A)].value
                    email = current_row[self.get_column_by_letter(ExcelInputData.COLUMN_B)].value
                    password = current_row[self.get_column_by_letter(ExcelInputData.COLUMN_C)].value

                    datas.append({
                        'name': name,
                        'email': email,
                        'password': password
                    })

            return datas
        except Exception as ex:
            raise ex
            return datas

    def getAccounts(self):
        accounts = self.getAccountsFromWorkSheet(ExcelInputData.ACCOUNT_SHEET_NAME)
        return accounts

    def getCommentsFromWorkSheet(self, sheet_name):
        datas = []
        try:
            work_sheet = self.open_work_sheet(sheet_name)
            for index, current_row in enumerate(work_sheet.rows):
                if index > 0:
                    title = current_row[self.get_column_by_letter(ExcelInputData.COLUMN_A)].value
                    comment = current_row[self.get_column_by_letter(ExcelInputData.COLUMN_B)].value

                    datas.append({
                        'rating': randint(4, 5),
                        'title': title,
                        'comment': comment
                    })

            return datas
        except Exception as ex:
            raise ex
            return datas

    def getComments(self):
        comments = self.getCommentsFromWorkSheet(ExcelInputData.COMMENT_SHEET_NAME)
        return comments





