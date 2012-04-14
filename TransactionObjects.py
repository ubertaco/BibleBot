class Query:
    def __init__(self, passages=[], sender):
        self.passage = passages
        self.sender = sender
        self.channel = None

    def create_response(self, text):
        return Response(text=text, recipient=self.sender)

class Response:
    def __init__(self, passage, text, recipient):
        self.passage = passage
        self.text = text
        self.recipient = recipient
        self.channel = None
