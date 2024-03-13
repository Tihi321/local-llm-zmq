import zmq

# Setup ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    # Ask the user for a message
    message = input("Enter a message to send to the server: ")

    # Send the message to the server
    socket.send_string(message)

    # Wait for the response from the server
    response = socket.recv()

    if response.decode().lower() == "quit":
        break

    # Print the response
    print(f"Received response: {response.decode()}")
