from flask import Flask, request, jsonify, render_template
from src.memory_store import get_client, ensure_index, add_memory, delete_memory
from src.retrieval import retrieve_context, build_prompt
from src.agent import generate_response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = get_client()
index = ensure_index(client)

# home page
@app.route("/")
def home():
    return render_template("index.html")

# chat endpoint
@app.route("/chat", methods = ["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty Message"}), 400

    # retrieve relevant memories
    context = retrieve_context(index, query=user_message, top_k=5)

    # prompt
    prompt = build_prompt(context, user_message)

    # generating response
    response = generate_response(prompt)

    # store user message
    add_memory(index, role="user", text=user_message)
    
    # storing assistant response
    add_memory(index, role="assistant", text=response)

    return jsonify({"response": response})


# forget memory endpoint
@app.route("/forget", methods=["POST"])
def forget():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Empty text"}), 400

    deleted = delete_memory(index, text)
    return jsonify({"deleted": deleted})


if __name__ == "__main__":
    app.run(debug=True)