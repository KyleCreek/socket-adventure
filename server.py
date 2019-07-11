import socket


class Server(object):
    """
    An adventure game socket server
    
    An instance's methods share the following variables:
    
    * self.socket: a "bound" server socket, as produced by socket.bind()
    * self.client_connection: a "connection" socket as produced by socket.accept()
    * self.input_buffer: a string that has been read from the connected client and
      has yet to be acted upon.
    * self.output_buffer: a string that should be sent to the connected client; for
      testing purposes this string should NOT end in a newline character. When
      writing to the output_buffer, DON'T concatenate: just overwrite.
    * self.done: A boolean, False until the client is ready to disconnect
    * self.room: one of 0, 1, 2, 3. This signifies which "room" the client is in,
      according to the following map:
      
                                     3                      N
                                     |                      ^
                                 1 - 0 - 2                  |
                                 
    When a client connects, they are greeted with a welcome message. And then they can
    move through the connected rooms. For example, on connection:
    
    OK! Welcome to Realms of Venture! This room has brown wall paper!  (S)
    move north                                                         (C)
    OK! This room has white wallpaper.                                 (S)
    say Hello? Is anyone here?                                         (C)
    OK! You say, "Hello? Is anyone here?"                              (S)
    move south                                                         (C)
    OK! This room has brown wall paper!                                (S)
    move west                                                          (C)
    OK! This room has a green floor!                                   (S)
    quit                                                               (C)
    OK! Goodbye!                                                       (S)
    
    Note that we've annotated server and client messages with *(S)* and *(C)*, but
    these won't actually appear in server/client communication. Also, you'll be
    free to develop any room descriptions you like: the only requirement is that
    each room have a unique description.
    """

    game_name = "Realms of Venture"

    def __init__(self, port=50000):
        self.input_buffer = ""
        self.output_buffer = ""
        self.done = False
        self.socket = None
        self.client_connection = None
        self.port = port

        self.room = 0

    def connect(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)

        address = ('127.0.0.1', self.port)
        self.socket.bind(address)
        self.socket.listen(1)

        self.client_connection, address = self.socket.accept()

    def room_description(self, room_number):
        """
        For any room_number in 0, 1, 2, 3, return a string that "describes" that
        room.

        Ex: `self.room_number(1)` yields "Brown wallpaper covers the walls, bathing
        the room in warm light reflected from the half-drawn curtains."

        :param room_number: int
        :return: str
        """

        # Create a Key-Value Pairing for the difference room colors
        rooms = {0:'Green Room', 1:'Red Room', 2:'Black Room', 3:'Orange Room'}
        print("Current Rooom NUmber", self.room)
        
        return "You are in the {}".format(rooms[room_number])
        

    def greet(self):
        """
        Welcome a client to the game.
        
        Puts a welcome message and the description of the client's current room into
        the output buffer.
        
        :return: None 
        """
        self.output_buffer = "Welcome to {}! {}".format(
            self.game_name,
            self.room_description(self.room)
        )

    def get_input(self):
        """
        Retrieve input from the client_connection. All messages from the client
        should end in a newline character: '\n'.
        
        This is a BLOCKING call. It should not return until there is some input from
        the client to receive.
         
        :return: None 
        """
        # Create an empty string to store the information
        #msg = b''

        # Perform a 'while' loop to ensure all data is obtained
        #while True:
        #    data = self.client_connection.recv(16)
        #    msg += data.decode('utf8')

            # If no data is recieved, break the loop
        #    if not data:
        #        break
        # Update the input buffer
        #self.input_buffer = msg

        ### Note: Changed how The Instructor handled this, it looked
        # much cleaner, so I'll be going with that
        received = b''
        while b'\n' not in received:
            received += self.client_connection.recv(16)
        
        self.input_buffer = received.decode()

    def move(self, argument):
        """
        THis Whole Section is currently broken"""
        """
        Moves the client from one room to another.
        
        Examines the argument, which should be one of:
        
        * "north"
        * "south"
        * "east"
        * "west"
        
        "Moves" the client into a new room by adjusting self.room to reflect the
        number of the room that the client has moved into.
        
        Puts the room description (see `self.room_description`) for the new room
        into "self.output_buffer".
        
        :param argument: str
        :return: None

        """
        
        # Need to evalute the move relative to the room that the person
        # is currently in to make a decision. Copy and Pasted Instructor
        # code, to avoid tedius logic gate requirements
        print("Here is the Incoming argument", argument)
        if argument == "north":
            if self.room == 0:
                self.room = 3
        elif argument == 'south':
            if self.room == 3:
                self.room = 0
        elif argument == 'east':
            if self.room == 2:
                self.room = 0
            elif self.room == 0:
                self.room = 1
        elif argument == 'west':
            if self.room == 1:
                self.room = 0
            elif self.room == 0:
                self.room = 2
        else:
            print("Something went wrong")

        self.output_buffer = self.room_description(self.room)
        

        #if self.room == 0 and argument == "north":
        #    print("triggered 1")
        #    self.room = 3

        #elif self.room == 0 and argument == "west":
        #    print("triggered 2")
        #    self.room = 1

        #elif self.room == 0 and argument == "east":
        #    print("triggered 3")
        #    self.room = 2

        #elif self.room == 1 and argument == "east":
        #    print("triggered 4")
        #    self.room = 0

        #elif self.room == 2 and argument == "west":
        #    print("triggered 5")
        #    self.room = 0

        #elif self.room == 3 and argument == "south":
        #    print("triggered 6")
        #    self.room = 0

        #self.output_buffer = self.room_description(int(self.room))
        
        #print("Here is the output Buffer", self.output_buffer)
    
    def say(self, argument):
        """
        Lets the client speak by putting their utterance into the output buffer.
        
        For example:
        `self.say("Is there anybody here?")`
        would put
        `You say, "Is there anybody here?"`
        into the output buffer.
        
        :param argument: str
        :return: None
        """

        self.output_buffer = "You say: {}".format(argument)


    def quit(self, argument):
        """
        Quits the client from the server.
        
        Turns `self.done` to True and puts "Goodbye!" onto the output buffer.
        
        Ignore the argument.
        
        :param argument: str
        :return: None
        """

        # Flags the system to end the While Loop
        self.done = True
        # Place the final message to the user to the buffer to be sent 
        # to the client
        self.output_buffer = "Goodbye"

    def route(self):
        """
        Examines `self.input_buffer` to perform the correct action (move, quit, or
        say) on behalf of the client.
        
        For example, if the input buffer contains "say Is anybody here?" then `route`
        should invoke `self.say("Is anybody here?")`. If the input buffer contains
        "move north", then `route` should invoke `self.move("north")`.
        
        :return: None
        """

        if self.input_buffer == "quit":
            self.quit(None)
        
        # split the input from the variable
        command_list = self.input_buffer.split(' ')

        # Split list to obtain intent
        function = command_list[0]
        action = " ".join(command_list[1:])
        

        if function == 'move':
            self.move(action)
        
        if function == 'say':
            self.say(action)

    def push_output(self):
        """
        Sends the contents of the output buffer to the client.
        
        This method should prepend "OK! " to the output and append "\n" before
        sending it.
        
        :return: None 
        """

        # Takes the information from the queued output buffer to be sent
        # to the screen. Starts with "ok", takes the content of the output
        # buffer, encodes it into bits, then sends it through connection
        self.client_connection.sendall(b"OK!" + self.output_buffer.encode() + b"\n")

    def serve(self):
        # Connect to the Client
        self.connect()
        # Greet the Client
        self.greet()
        # Push initial statements in the out_put Buffer to the client
        self.push_output()

        while not self.done:
            # Obtain the input from the client
            self.get_input()
            self.route()

            # Push the information from the output_buffer to the client
            self.push_output()

        self.client_connection.close()
        self.socket.close()
