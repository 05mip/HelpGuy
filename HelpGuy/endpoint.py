import logging
from uagents import Agent, Bureau, Context, Model
from uagents.resolver import RulesBasedResolver
from Agents import yellow_mm, red_mm, green_mm, endpointID, Message
from flask import Flask, request, jsonify
from uagents.context import send_sync_message
import asyncio
from uagents.crypto import Identity

resolver = RulesBasedResolver({red_mm.address:'http://127.0.0.1:8000/submit',
                               yellow_mm.address:'http://127.0.0.1:8000/submit',
                               green_mm.address:'http://127.0.0.1:8000/submit'})

user_prompt = ''

app = Flask(__name__)

@app.route('/search', methods=['GET'])
async def search():
    query = request.args.get('q')
    global user_prompt
    user_prompt = query
    print(query)
    if query:
        response = await send_sync_message(
            yellow_mm.address, Message(message=[user_prompt]), 
            response_type=Message, resolver=resolver, sender=endpointID
        )
        return jsonify({"response": response.message[0]})
    else:
        return jsonify({"error": "No query parameter provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)