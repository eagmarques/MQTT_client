import json


class Read(object):

    # def parse_message(self, data):
    #
    #     try:
    #         parsed_data = str(data, "utf-8")
    #         if not is_heartbeat(parsed_data):
    #             parsed_data = parsed_data.replace("item", "E").replace("rssi", "R").replace("antenna", "A").replace(
    #                 "readerName", "N")
    #             parsed_data = parsed_data.split(",")
    #             if mac_is_present(parsed_data):
    #                     parsed_data = parsed_data[0] + "," +  parsed_data[2] + "," + parsed_data[3] + "," + parsed_data[4]
    #             json_test = json.loads(parsed_data)
    #             if((abs(json_test['R'])) <= 100):
    #                 json_test['R'] = 100*json_test['R']
    #             parsed_data = json.dumps(json_test)
    #         return parsed_data
    #     except Exception as error:
    #         print(error.__cause__)

    @staticmethod
    def parse_message(data):

        try:
            parsed_data = str(data, "utf-8")
            if not is_heartbeat(parsed_data):
                parsed_data = parsed_data.replace("item", "E").replace("rssi", "R").replace("antenna", "A").replace(
                    "readerName", "N").replace("\r", "").replace("\n", "")
                json_read = json.loads(parsed_data)
                for element in json_read:
                    if element == "mac":
                        json_read.pop('mac')
                        break
                if ((abs(json_read['R'])) <= 100):
                    json_read['R'] = 100 * json_read['R']
                return json.dumps(json_read)
        except Exception as error:
            print(error.__cause__)


def is_heartbeat(msg):
    heartbeat = ["uptime", "version"]
    for text in heartbeat:
        if text in msg:
            return True
    return False

# def mac_is_present(arr):
#
#     for text in arr:
#         if "mac" in text:
#             return True
#
#     return False
