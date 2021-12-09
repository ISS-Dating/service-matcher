from typing import Final

import os


HOSTNAME: Final[str] = 'localhost:27017'
USERNAME: Final[str] = os.environ.get('MONGO_USERNAME')
PASSWORD: Final[str] = os.environ.get('MONGO_PASSWORD')
DATABASE: Final[str] = os.environ.get('MONGO_DATABASE')

CONNECTION_STR: Final[str] = f'mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}/?authSource={DATABASE}'
