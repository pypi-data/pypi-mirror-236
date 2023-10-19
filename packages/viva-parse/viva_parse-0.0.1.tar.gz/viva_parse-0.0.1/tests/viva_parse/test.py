import viva_parse
input_text = "<|prompter|> generate an image of a lecture<|endoftext|><|assistant|><|generate_image|><[prompt]> a lecture<[aspect_ratio]> 2:3<|endofaction|><|book_room|><[date]> monday<[time]> 3am<|endofaction|> hi there<|endoftext|>"

def test_parse_dump_equal():
    parsed = viva_parse.parse(input_text)
    output_text = viva_parse.dump(parsed)
    assert input_text == output_text
