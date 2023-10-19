#text =  "<|prompter|> generate an image of a lecture<|endoftext|><|assistant|><|generate_image|><[prompt]> a lecture<[aspect_ratio]> 2:3<|endofaction|><|book_room|><[date]> monday<[time]> 3am<|endofaction|> hi there<|endoftext|>"

from .parse import parse_messages as parse
from .dump import dump


#messages = parse.parse_messages(text)
#text = dump.dump(messages)



#action_pattern = r"<\|(?P<action>[^|]+)\|>(?P<params>[^|]*)<\|endofaction\|>"

#for match in re.finditer(action_pattern, text, re.S):
#    print(match.group("action"), "|", match.group("params"))
#print(x.group("action"), "|", x.group("params"))

#"/<\|(?<action>[^|]+)\|>(?<params>[^|]*)<\|endofaction\|>/g"
#"/<\[(?<param>[^\]]+)\]>(?<value>[^<\[]+)/g"