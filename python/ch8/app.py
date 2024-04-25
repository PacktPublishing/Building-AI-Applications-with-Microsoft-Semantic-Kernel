from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from HomeAutomation import HomeAutomation
from dotenv import load_dotenv
import logging

app = Flask(__name__)
app.secret_key = b'skb_2024'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/operate_light', methods=['POST'])
async def operate_light():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4-turbo-preview", api_key, org_id)
    kernel.add_service(gpt4)
    kernel.import_plugin_from_object(HomeAutomation(), "HomeAutomation")
    
    data = request.get_json()
    location = data['location']
    action = data['action']

    result = str(await kernel.invoke(kernel.plugins["HomeAutomation"]["OperateLight"], location=location, action=action))
    print(result)

    return jsonify({'result': result})

@app.route('/operate_garage_door', methods=['POST'])
async def operate_garage_door():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4-turbo-preview", api_key, org_id)
    kernel.add_service(gpt4)
    kernel.import_plugin_from_object(HomeAutomation(), "HomeAutomation")
    
    data = request.get_json()
    action = data['action']
    result = str(await kernel.invoke(kernel.plugins["HomeAutomation"]["OperateGarageDoor"], action=action))
    print(result)

    return jsonify({'result': result})

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)

