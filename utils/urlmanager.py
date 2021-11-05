decode = {
    '%21': '!', '%23': '#', '%24': '$',
    '%26': '&', '%27': "'",
    '%28': '(', '%29': ')', '%2A': '*',
    '%2B': '+', '%2C': ',', '%2F': '/',
    '%3A': ':', '%3B': ';', '%3D': '=',
    '%3F': '?', '%40': '@', '%5B': '[',
    '%5D': ']',
    
    '%0A': '\n', '%0D': '\n', '%0D%0A': '\n',
    '%20': ' ', '%22': '"', '%2D': '-',
    '%2E': '.', '%5C': '\'', '%5E': '^', '%5F': '_',
    '%60': '`', '%7B': '{', '%7D': '}', '%7C': '|',
    '%7E': '~', 
}

encode = {}

# Preparando dicionário para encode
for k,v in decode.items():
    encode[v] = k


class URL:
    def encode(self, text: str):
        for k,v in encode.items():
            text = text.replace(k, v)

        return text

    
    def decode(self, text: str):
        for k, v in decode.items():
            text = text.replace(k, v)

        return text
        