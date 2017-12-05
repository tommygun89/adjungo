import os
import os.path
from filehandler import FileHandler


class EventHandler:

    def __init__(self):
        self.file_handler = FileHandler()

    def is_new_event(self, data):
        return self.__is_event_type(data, "newEvent")

    def is_update_event(self, data):
        return self.__is_event_type(data, "updateEvent")

    def is_cancel_event(self, data):
        return self.__is_event_type(data, "cancelEvent")

    @staticmethod
    def __is_event_type(content, event):
        if content["message-type"] == event:
            return True
        return False

    def create_event(self, event_name):
        json_file = self.file_handler.create_file_for_event(event_name, "newEvent_template.json")
        print "(INFO) JSON created for event with content\n" % json_file
        return json_file

    def update_event(self, content):
        stored_file = self.file_handler.get_file_for_event(content["name"], content["identifier"])
        if stored_file is None:
            return
        self.file_handler.update_file_content(stored_file, content)

    def cancel_event(self, content):
        event_file = self.file_handler.get_file_for_event(content["name"], content["identifier"])
        print "(INFO) File with name %s %s found and will be deleted" % \
              (content["name"], "was" if os.path.isfile(str(event_file)) else "not")
        self.file_handler.delete_file(event_file)
