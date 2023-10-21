import json
from .dump import dump

def format(conversation):
    conversation = dump(conversation)
    
    conversation_parts = conversation.split("<|assistant|>")
    formatted_conversation = []
    
    for i in range(1, len(conversation_parts)):
        input_part = "<|assistant|>".join(conversation_parts[:i]) + "<|assistant|>"
        output_part = conversation_parts[i].split("<|endoftext|>")[0] if "<|endoftext|>" in conversation_parts[i] else ""
        formatted_conversation.append({"input": input_part, "output": output_part + "<|endoftext|>"})
        
    return formatted_conversation