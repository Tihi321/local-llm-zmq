import zmq
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Define the model name
model_name = "gpt2"

# Check if the model and tokenizer are downloaded, if not, download them
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Setup ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def generate_response(model, tokenizer, text, history=None, max_length=200):
    """
    Generate a response based on the text and history.

    Parameters:
    - model: The language model.
    - tokenizer: The tokenizer for the language model.
    - text (str): The input text to continue the conversation.
    - history (Tensor or None): The history of the conversation as a Tensor, or None if no history.
    - max_length (int): The maximum length of the generated text.

    Returns:
    - str: The generated response text.
    - Tensor: The updated conversation history as a Tensor.
    """
    # Encode the new user input
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")

    # If there's no history, use the input_ids directly; otherwise, concatenate them
    if history is not None:
        bot_input_ids = torch.cat([history, input_ids], dim=-1)
    else:
        bot_input_ids = input_ids

    # Generate a response
    chat_history_ids = model.generate(
        bot_input_ids, max_length=max_length, pad_token_id=tokenizer.eos_token_id
    )

    # Extract the response
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
    )

    # Update the conversation history by setting it to the generated chat history ids
    history = chat_history_ids

    return response, history


# Initialize conversation history as None
conversation_history = None

# Loop that listens to messages and uses the full list (history)
# for generating responses
print("AI Assistant: Hello! How can I help you today? (Type 'quit' to exit)")

while True:

    # Wait for the next request from the client
    message = socket.recv()
    user_input = f"You: {message.decode()}"
    print(user_input)

    if message.decode().lower() == "quit":
        socket.send_string("quit")
        break

    # Generate a response using the conversation history
    ai_response, conversation_history = generate_response(
        model, tokenizer, user_input, conversation_history
    )
    print("AI:", ai_response)

    # Send reply back to the client
    socket.send_string(ai_response)
