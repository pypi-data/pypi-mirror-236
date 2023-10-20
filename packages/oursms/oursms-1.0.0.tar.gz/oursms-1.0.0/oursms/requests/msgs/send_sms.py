class SendSMSRequest(object):
    """
    This API is used to send a message to one or more recipients
    """
    SRC = 'src'
    DESTS = 'dests'
    BODY = 'body'

    def __init__(self, src: str, dests: list, body: str):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        if not isinstance(dests, list):
            dests = [dests]

        self.src = src
        self.dests = dests
        self.body = body

    def to_dictionary(self):
        """
        Return the property of the object as a dictionary
        """
        return {self.SRC: self.src, self.DESTS: self.dests, self.BODY: self.body}

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Creates an instance of this model from a dictionary
        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        src = dictionary.get(cls.SRC)
        dests = dictionary.get(cls.DESTS)
        body = dictionary.get(cls.BODY)

        # Return an object of this model
        return cls(src=src, dests=dests, body=body)
