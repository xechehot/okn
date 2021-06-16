import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load environment variable from .env
    **os.environ,  # override loaded values with environment variables
}
