class chatResponse:
    def __init__(self, code: int, message: str, c_id: str, messages: [], prompt: str, response: str) -> None:
        self.code = code
        self.message = message
        self.c_id = c_id
        self.messages = messages
        self.prompt = prompt
        self.response = response