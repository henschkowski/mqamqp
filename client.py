from __future__ import print_function, unicode_literals
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import pdb

class HelloWorld(MessagingHandler):
    def __init__(self, server, address):
        super(HelloWorld, self).__init__(peer_close_is_error=True)
        self.server = server
        self.address = address
        self.container_id= "1234"
        print ("__init done...")

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.address)
        event.container.create_sender(conn, self.address)
        print ("onStart done..")

    def on_sendable(self, event):
        print ("In on_sendable")
        # MQ apparently needs the topic string in the message itself
        event.sender.send(Message(body="Hello World!", address=self.address))
        event.sender.close()

    def on_message(self, event):
        print ("In on_message")
        print(event.message.body)
        event.connection.close()

    def on_rejected(self, event):
        print ("In on_rejected")

    def on_accepted(self, event):
        print ("In on_accepted")
        
    def on_settled(self, event):
        print ("In on_settled")
        
    def on_link_error(self, event):
        print ("In on_link_error")

    def on_connection_error(self, event):
        print(event)
        print ("In on_connection_error")

    def on_session_error(self, event):
        print ("In on_session_error")

        
        
Container(HelloWorld("localhost:5672", "/examples/test")).run()