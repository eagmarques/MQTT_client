import json


class Read(object):

    def __init__(self):
        self.E = ""
        self.R = ""
        self.A = ""
        self.N = ""

        # @staticmethod
    def parse_message(self, data):

        try:
            parsed_data = str(data, "utf-8")
            parsed_data = parsed_data.replace("item", "E").replace("rssi", "R").replace("antenna", "A").replace(
                "readerName", "N")
            json_test = json.loads(parsed_data)
            self.E = json_test.E
            self.R = json_test.R
            self.A = json_test.A
            self.N = json_test.N

            print(
                "------------------------------------------------------------------------------------------------------")
            print(parsed_data)
            print(
                "------------------------------------------------------------------------------------------------------")
            return self
        except Exception as error:
            print(error.__cause__)