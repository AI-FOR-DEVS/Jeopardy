from database import get_random_question, get_random_question_declaration, update_player_score, update_player_score_delaration, get_player_score, get_player_score_declaration
from autogen import GroupChatManager, GroupChat, UserProxyAgent, AssistantAgent, config_list_from_json
from chat_completion import create_openai_completion, create_openai_declaration
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Setting up the configurations

local_config = [
    {
        "model": 'gpt-3.5',
        "base_url": "http://localhost:1234/v1"
    }
]

config_list_gpt3_turbo = config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

config_list_gpt4_turbo = config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"],
    },
)

config_list = config_list_from_json('OAI_CONFIG_LIST')
llm_config = {"config_list": config_list}


# Monkey patch to redirect the agents messages

def new_print_received_message(self, message, sender):
    print(f"PATCHED {sender.name}: {message.get('content')}")
    socketio.emit('message', {"sender": sender.name,
                  "content": message.get('content')})

GroupChatManager._print_received_message = new_print_received_message


# Define the agents

moderator = AssistantAgent(
    'moderator',
    system_message="""
            As the Jeopardy! moderator, wait for a category choice, then ask a random question from it. 
            After a player answers, update their score if correct. Periodically, add a brief joke to keep things lively. Keep it short.
        """,
    llm_config={"config_list": config_list_gpt4_turbo,
                "functions": [get_random_question_declaration, update_player_score_delaration, get_player_score_declaration]},
    function_map={
        "get_random_question": get_random_question,
        "update_player_score": update_player_score,
        "get_player_score": get_player_score
    }
)

peter = AssistantAgent(
    'peter',
    system_message="""
        As Peter, a contestant in Jeopardy!, select a category when it's your turn.
        If you know the answer to a question, respond with 'BUZZER' and then provide your brief answer. 
        Use the 'create_openai_completion' function for research your responses.
        """,
    llm_config={"config_list": config_list,
                "functions": [create_openai_declaration]},
    function_map={
        "create_openai_completion": create_openai_completion
    }
)

bob = AssistantAgent(
    'bob',
    system_message="""
        As Bob, participating in Jeopardy!, choose a category when prompted.
        If you know an answer, say 'BUZZER' followed by your concise response.
        Your role is to select categories and answer questions.
        """,
    llm_config={"config_list": config_list_gpt4_turbo}
)

user_proxy = UserProxyAgent(
    'user_proxy',
    system_message="You are the boss",
    human_input_mode="NEVER"
)

groupchat = GroupChat(
    agents=[moderator, bob, peter, user_proxy], messages=[], max_round=50
)

manager = GroupChatManager(
    groupchat=groupchat, llm_config=llm_config
)

# Define the endpoint

@app.route('/run', methods=['GET'])
def run():
    user_proxy.initiate_chat(
        manager, message=f""""
          Game Process:

            1. Category Selection: Players (excluding the moderator) choose a category such as 'Literature', 'History', 'Geography', or 'Science'.

            2. Question Round: The moderator then poses a question related to the selected category, phrased as: "Here's your question in the category of [chosen category]: ..."

            3. Answering: Players take turns to provide their answers. Alternating responses keeps the game fair and engaging.

            4. Answer Reveal: Once the players have answered, the moderator discloses the correct answer.

            5. Scoring: If a player's answer is correct, they earn 100 points.

            6. Score Update: After each round, the moderator updates the score, announcing it like: "Peter now has [total points] points."

            Repeat the process starting from step 1 for continuous gameplay. This keeps the game dynamic and allows for multiple rounds of fun and learning!

        """
    )

    return jsonify({"status": "ok"})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
