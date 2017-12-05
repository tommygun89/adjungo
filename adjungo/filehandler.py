import json
import os
import os.path
import uuid


class FileHandler:

    def __init__(self):
        self.files = list()

    def get_all_events(self):
        return self.files

    def replace_in_json(self, adict, keyIn, valueIn):
        for key in adict.keys():
            if key == keyIn:
                adict[key] = valueIn;
            elif type(adict[key]) is dict:
                self.replace_in_json(adict[key], keyIn, valueIn)

    def parse_json(self, jsonFormat):
        decoded = json.loads(str(jsonFormat)[str(jsonFormat).find("#")+1:])
        print "(INFO) Parsed JSON:"
        print self.dump_json(decoded)
        return decoded

    def dump_json(self, content):
        decoded = json.dumps(content, separators=(',',':'), indent=4)
        return decoded

    def get_json_file_name(self, name, identifier):
        return os.getcwd() + "/" + name + "_" + str(identifier) + ".json"

    def get_file_for_event(self, name, identifier):
        event_file = self.get_json_file_name(name, identifier)
        if os.path.isfile(event_file):
            return event_file
        else:
            print "(ERROR) File with name %s identifier %s not found." % (name, identifier)
            return None

    def get_json_template(self, file_name):
        template = os.getcwd() + "/../json/" + file_name
        if os.path.isfile(template):
            return template
        else:
            print "(ERROR) File %s not found" % file_name
            return None

    def create_file_for_event(self, event_name, template):
        identifier = str(uuid.uuid1())
        template_file = self.get_json_template(template)
        if template_file is None:
            print "(ERROR) Template not found, cannot create event file"
            return

        with open(str(template_file), 'r') as jsonFile:
            content = json.load(jsonFile)
            self.replace_in_json(content, "name", event_name)
            self.replace_in_json(content, "identifier", identifier)
            self.replace_in_json(content, "data", "")
            save_event = open(str(event_name) + "_" + str(identifier) + ".json", 'a')
            self.files.append(save_event)
            save_event.write(str(json.loads(content)))
            save_event.close()
            return self.parse_json(self.get_json_file_name(event_name, identifier))

    def update_file_content(self, event_file, content):
        with open(str(event_file), "r+") as json_file:
            print json_file
            data = json.load(json_file)
            for param in content:
                self.replace_in_json(data, param, content[param])
            json_file.seek(0)
            json_file.truncate()
            json_file.write(self.dump_json(data))
            json_file.close()

    def delete_all_files(self):
        for event_file in self.files:
            self.delete_file(event_file)

    @staticmethod
    def delete_file(file):
        if file is not None:
            os.remove(file)
