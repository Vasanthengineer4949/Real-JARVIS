import pyperclip
def get_clipboard():
    cc = pyperclip.paste()
    if isinstance(cc, str):
        return cc
    else:
        return "Nothing is there in clipboard"
    
def clipboard_prompt(question):
    input_prompt = question + ":\nClipboard content: " + get_clipboard()
    return input_prompt