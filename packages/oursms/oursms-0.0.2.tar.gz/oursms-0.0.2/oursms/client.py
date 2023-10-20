from oursms.configuration import Configuration
from oursms.handlers.msgs import send_sms as handler


class OursmsClient(object):
    config = Configuration

    def __init__(self, api_token):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        Configuration.api_token = api_token

    def send_message(self, request):
        """
        This API is used to send a sms to one or more recipient
        """
        return handler.send_sms_handler(request=request)
