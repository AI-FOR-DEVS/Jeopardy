import requests

create_openai_declaration = {
    "name": "create_openai_completion",
    "description": "Answers Jeopardy! questions for Peter",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The Jeopardy! question"
            },
        }
    }
}


def create_openai_completion(question, temperature=0.7, model="local-model", base_url="http://localhost:1234/v1", api_key="not-needed"):
    messages = [
        {"role": "user", "content": f"You play Jeopardy! Formulate the question for the answer: {question}"}
    ]

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']