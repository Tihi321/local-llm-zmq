import zmq
import langchain

# Setup ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    # Wait for the next request from the client
    message = socket.recv()
    print(f"Received request: {message}")

    # Process the message using Langchain
    processed_message = langchain.process(message)

    # Send reply back to the client
    socket.send(processed_message)
