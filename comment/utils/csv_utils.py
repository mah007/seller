# -*- coding: utf-8 -*-
import csv
import glob
import io


class CSVUtils:

    @classmethod
    def writeRow(cls, filename, row, is_append=True):
        option = 'a'
        if is_append == False:
            option = 'w'
        try:
            with open(filename, option) as f:
                writer = csv.writer(f)
                writer.writerow(row)
        except Exception as ex:
            NinjaLogger.instance.exception(
                "Error writting row to file %s" % ex)

    @classmethod
    def mergeCsvFiles(cls, folder, filename, is_append=True, is_header=True):
        try:
            option = 'ab'
            if is_append == False:
                option = 'wb'
            with io.open(filename, option) as f:
                writer = csv.writer(f)
                csvFiles = glob.glob("%s/*.csv" % folder)
                first_header = True
                for file in csvFiles:
                    with io.open(file, 'rb',) as fData:
                        reader = csv.reader(fData)
                        if is_header != True:
                            if first_header == True:
                                next(reader)
                                first_header = False
                        writer.writerows(reader)
        except Exception as ex:
            NinjaLogger.instance.exception("Error mergeCsvFiles file %s" % ex)
            print(ex)





