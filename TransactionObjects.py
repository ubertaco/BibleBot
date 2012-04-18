class Query:
    def __init__(self, passages, sender):
        self.passages = passages
        self.sender = sender
        self.channel = None

class Response:
    def __init__(self, passage, text, recipient):
        self.passage = passage
        self.text = text
        self.recipient = recipient
        self.channel = None
