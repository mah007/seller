# -*- coding: utf-8 -*-
import openpyxl
from constants import Output
from constants import ExcelInputData
from model.input_model import InputModel


class ImportExcel(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def get_column_index_from_letter(self, letter):
        return openpyxl.utils.cell.column_index_from_string(letter) - 1

    def open_work_sheet(self, sheet_name):
        work_book = openpyxl.load_workbook(self.file_path, data_only=True)
        work_sheet = work_book.get_sheet_by_name(sheet_name)
        return work_sheet

    def save_work_sheet(work_sheet, file_path):
        work_sheet.save(file_path)

    def write_output_to_file(file_path, work_sheet, row_index, data):
        try:
            current_row = work_sheet.rows[row_index]
            for i in xrange(1, data.length):
                current_row[i].value = data[i]
        except Exception as e:
            raise e
        finally:
            save_work_sheet(file_path)

    def __read_input_from_work_sheet(self, sheet_name):
        datas = []
        try:
            work_sheet = self.open_work_sheet(sheet_name)
            for index, current_row in enumerate(work_sheet.rows):
                if index > 0:
                    pick_up = current_row[self.get_column_index_from_letter(
                        ExcelInputData.PICK_UP)].value
                    drop_off = current_row[self.get_column_index_from_letter(
                        ExcelInputData.DROP_OFF)].value

                    if pick_up == None or pick_up == "" or drop_off == None or drop_off == "":
                        break

                    pickup_ward = current_row[self.get_column_index_from_letter(
                        ExcelInputData.PICK_UP_WARD)].value
                    pickup_district = current_row[
                        self.get_column_index_from_letter(ExcelInputData.PICK_UP_DIST)].value
                    city = current_row[self.get_column_index_from_letter(
                        ExcelInputData.CITY)].value
                    distance = current_row[self.get_column_index_from_letter(
                        ExcelInputData.DISTANCE)].value
                    gDistance = current_row[self.get_column_index_from_letter(
                        ExcelInputData.GDISTANCE)].value
                    pick_up_lat = current_row[self.get_column_index_from_letter(
                        ExcelInputData.PICK_UP_LAT)].value
                    pick_up_long = current_row[self.get_column_index_from_letter(
                        ExcelInputData.PICK_UP_LONG)].value
                    drop_off_lat = current_row[self.get_column_index_from_letter(
                        ExcelInputData.DROP_OFF_LAT)].value
                    drop_off_long = current_row[self.get_column_index_from_letter(
                        ExcelInputData.DROP_OFF_LONG)].value

                    pair_id = index + 1
                    if pair_id < 10:
                        pair_id = "0%s" % pair_id

                    inputArgs = {
                        'pair_id': "pair%s" % (pair_id),
                        'pick_up': pick_up,
                        'drop_off': drop_off,
                        'pickup_ward': pickup_ward,
                        'pickup_district': pickup_district,
                        'city': city,
                        'distance': distance,
                        'gDistance': gDistance,
                        'pick_up_lat': pick_up_lat,
                        'pick_up_long': pick_up_long,
                        'drop_off_lat': drop_off_lat,
                        'drop_off_long': drop_off_long
                    }

                    data = InputModel(inputArgs)
                    datas.append(data)

        except Exception as e:
            raise e
        return datas

    def getInputData(self, sheet_name, isShuffle=False):
        datas = self.__read_input_from_work_sheet(sheet_name)
        if isShuffle == True:
            random.shuffle(datas)
        return datas






