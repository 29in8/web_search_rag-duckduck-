from flask import Blueprint, request
from m_langchain.openai_duckduck import duckduck

tools = Blueprint('tools', __name__, url_prefix='/tools')


@tools.route('/duckduck', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data['message']
        history = data['history']
        result = duckduck(message, history)
        return result['output']
    except Exception as e:
        return str(e)
