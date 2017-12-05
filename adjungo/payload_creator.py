import json

from filehandler import FileHandler


class PayloadCreator:

    def __init__(self):
        self.file_handler = FileHandler()

    def get_status_data(self, event_file):
        print "(INFO) Preparing statusEvent for file %s" % str(event_file)
        with open(str(event_file), 'r') as jsonFile:
            data = json.load(jsonFile)
            self.file_handler.replace_in_json(data, "message-type", "statusEvent")
            return data

    def get_response_data(self, event_name, identifier, data):
        print "(INFO) Preparing responseEvent for event %s with identifier %s and data %s" % \
              (event_name, str(identifier), str(data))
        template = self.get_response_template()
        if template is None:
            print "(ERROR) Template not found, cannot send response"
            return

        # TODO Double responsibility, file handling should be moved to file_handler
        with open(str(template), 'r') as jsonFile:
            content = json.load(jsonFile)
            self.file_handler.replace_in_json(content, "identifier", identifier)
            self.file_handler.replace_in_json(content, "name", event_name)
            self.file_handler.replace_in_json(content, "data", data)
            return json.dumps(content)
    
    def get_status_template(self):
        return self.file_handler.get_json_template("statusEvent_template.json")

    def get_response_template(self):
        return self.file_handler.get_json_template("rspEvent_template.json")
