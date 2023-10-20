class Configuration(object):
    """
    This class is designed for configuring the SDK by the user. It does not require instantiation,
    and all properties and methods can be accessed without creating an instance.
    """
    # An enum for API servers
    class Server(object):
        BASE_URL = 'base_url'

    # An enum for SDK environments
    class Environment(object):
        """
        Describe the setting where software and other products are actually put
        into operation for their intended uses by end users
        """
        PRODUCTION = 'production'

    # All the environments the SDK can run in
    environments = {
        Environment.PRODUCTION: {
            Server.BASE_URL: 'https://api.oursms.com',
        },
    }

    # The environment in which the SDK is running
    environment = Environment.PRODUCTION

    # The api_token to use with basic authentication
    api_token = None

    @classmethod
    def get_base_uri(cls, server=Server.BASE_URL):
        """
        This function generates the appropriate base URI for the given environment and server.
        It plays a crucial role in determining the foundation for all API requests and interactions.
        By dynamically creating the base URI, it ensures that the SDK operates seamlessly in various environments,
        adapting to the specific server requirements while maintaining a consistent and reliable connection.
        """
        return cls.environments[cls.environment][server]
