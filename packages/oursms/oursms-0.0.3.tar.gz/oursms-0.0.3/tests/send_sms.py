from oursms.client import OursmsClient
from oursms.requests.msgs import send_sms as send_sms_request


def send_sms():
    """
    This API is used to send a sms to one or more recipient
    """
    api_token = input("Please Enter the api token:")
    src = input("Please Enter the src:")
    dests = input("Please Enter the dests:")
    body = input("Please Enter the body:")

    client = OursmsClient(api_token=api_token)
    request = send_sms_request.SendSMSRequest(src, dests, body)
    return client.send_message(request)


if __name__ == '__main__':
    send_sms()
