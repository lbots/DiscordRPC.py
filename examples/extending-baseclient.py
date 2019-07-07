import random
import time

import discordrpc


class CustomClient(discordrpc.BaseClient):  # Inherit from BaseClient which handles most of the hard work.

    def __init__(self, client_id):
        super().__init__(client_id)  # Fetches the connection to the locally running Discord

    def run_complete(self, func):  # So we don't have to keep typing the full thing
        return self.loop.run_until_complete(func)

    def open_connection(self):  # Makes sure that the connection has been created, and if not creates it.
        if not self.connection_open:
            self.run_complete(self.handshake())

    def send_presence(self, text):  # The function that we call when we want to set the presence
        self.open_connection()
        payload = {  # Follows the Discord docs
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": 123,  # Just a process ID, you can get a real one if you want
                "activity": {
                    "details": text
                }
            },
            "nonce": random.randint(0, 1000000000)
        }
        self.send_data(1, payload)
        return self.run_complete(self.read_output())

    def on_event(self, data):
        pass  # We're not interested in events, so just do nothing.

    def close(self):
        self.close_event_loop()  # Safely exit


client = CustomClient("MY APPLICATION ID GOES HERE")  # Create an instance of our class
loop = True
while loop:  # Set out presence once every 15 seconds until we press Ctrl + C
    try:
        client.send_presence('Playing with cats :3')
        time.sleep(15)
    except KeyboardInterrupt:
        loop = False
    finally:
        client.close()
