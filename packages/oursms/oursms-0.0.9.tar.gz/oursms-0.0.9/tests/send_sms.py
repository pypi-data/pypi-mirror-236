from oursms.client import OursmsClient


def send_sms():
    """
    This API is used to send a sms to one or more recipient
    """
    api_token = input("Please Enter the api token:")
    src = input("Please Enter the src:")
    dests = input("Please Enter the dests:")
    body = input("Please Enter the body:")
    return OursmsClient(api_token=api_token).send_message(src, dests, body)


if __name__ == '__main__':
    send_sms()
