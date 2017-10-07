

class StringUtils(object):

    @classmethod
    def toString(self, byte):
        try:
            return byte.decode('utf-8')
        except Exception as ex:
            return byte


    @classmethod
    def isEmpty(self, strValue):
        return (strValue == None or len(strValue) == 0)










