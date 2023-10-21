def dump(messages):
    result = ""
    for message in messages:
        result += f"<|{message['role']}|>"

        if 'actions' in message:
            for action in message['actions']:
                result += f"<|{action['name']}|>"
                if 'params' in action:
                    for param, value in action['params'].items():
                        result += f"<[{param}]> {value}"
                    result += "<|endofaction|>"
        if 'message' in message:
            result += f" {message['message']}"

        result += "<|endoftext|>"

    return result

sample_data = [
    {'role': 'prompter', 'message': 'generate an image of a lecture'},
    {'role': 'assistant', 'message': 'hi there', 
     'actions': [
         {'name': 'generate_image', 
          'params': {'prompt': 'a lecture', 'aspect_ratio': '2:3'}}, 
         {'name': 'book_room', 'params': {'date': 'monday', 'time': '3am'}}
     ]
    },
]
