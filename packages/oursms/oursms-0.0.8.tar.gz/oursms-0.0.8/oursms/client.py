from oursms.configuration import Configuration
from oursms.handlers.msgs.send_sms import send_sms_handler
from oursms.requests.msgs.send_sms import SendSMSRequest


class OursmsClient(object):
    config = Configuration

    def __init__(self, api_token):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        Configuration.api_token = api_token

    def send_message(self, src, dests, body):
        """
        This API is used to send a sms to one or more recipient.

        @:param src: The number or text that will appear to the receiver on the
             mobile device as the sender (sender Id).

        @:param dests: An array of destination addresses (mobile numbers) to
               deliver the message to. It can be one destination or multiple
               destinations up to 500 per request.
               
        @:param body:  The text of the message. The text can be in any language.
               Our system will automatically detect the best encoding to
               used when delivering the message.

        :return If the request succeeded a HTTP response with the status 200 will be returned with the results
        in the body as json. However, if the request fails a failed HTTP response will be returned with a
        json body containing the error code and error description that occurred.
        """
        request = SendSMSRequest(src, dests, body)
        return send_sms_handler(request=request)
