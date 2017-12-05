import SocketServer
import sys
from apscheduler.schedulers.background import BackgroundScheduler

from adjungo.event_handler import EventHandler
from adjungo.payload_creator import PayloadCreator
from adjungo.filehandler import FileHandler


class Adjungo(SocketServer.BaseRequestHandler):

    def __init__(self):
        self.event_handler = EventHandler()
        self.event_payload_creator = PayloadCreator()
        self.file_handler = FileHandler()
        self.status_updater_running = False

    def handle(self):
        if not self.status_updater_running:
            self.__schedule_status_updates()
            self.status_updater_running = True

        response = self.handle_message(self.request.recv(1024).strip())
        if not isinstance(response, list):
            print "(SEND) sending response to frontend with data %s" % str(response)
            self.request.sendall(str(response))
        else:
            for data in response:
                print "(SEND) sending response to frontend with data %s" % str(response)
                self.request.sendall(str(data))

    def handle_message(self, data):
        decoded = self.file_handler.parse_json(data)

        if self.event_handler.is_new_event(decoded):
            print "(RCVD) newEvent from frontend"
            event_name, identifier = self.event_handler.newEvent(decoded)
            return self.event_payload_creator.get_response_data(event_name, identifier, "")

        if self.event_handler.is_update_event(decoded):
            print "(RCVD) updateEvent from frontend"
            return self.event_handler.update_event(decoded)

        if self.event_handler.is_cancel_event(decoded):
            print "(RCVD) cancelEvent from frontend"
            return self.event_handler.cancel_event(decoded)

    def updateStatusForAllEvents(self):
        print "(INFO) Triggered sending of statusEvent for all events"
        events = list()
        for file in self.file_handler.get_all_events():
            events.append(self.event_payload_creator.get_status_data(file))
        return events

    def __schedule_status_updates(self):
        print "(INFO) Sending of statusEvent configured for every 12 hours"
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.updateStatusForAllEvents, 'interval', hours=12)
        scheduler.start()


# TODO This is not the main function anymore, replace when Router is ready
if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 8282
        server = SocketServer.TCPServer((HOST, PORT), Adjungo)
        print "(START) Adjungo server started on %s:%s..." % (HOST, PORT)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print "(EXIT) Server was interrupted and will shutdown"
        print "(EXIT) All events will be deleted..."
        # TODO: Has to remove all files nicely
        sys.exit(0)
