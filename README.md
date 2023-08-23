# Telegram Bot Tester

Telegram Bot Tester is a set of tools designed to help developers test their Telegram bots more efficiently. Using a combination of a Telethon-based user-bot and a Redis queue, the Telegram Bot Tester automates interaction with your bot for more streamlined testing.
Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

<a name="features"></a>
## Features

- Automated interaction with Telegram bots.
- Telethon-based user-bot to send/receive messages.
- Redis queue integration to manage message traffic.
- Independent of the environment of use (programming language or other tool)

<a name="instalation"></a>
## Installation

_Work in progress_

<a name="usage"></a>
## Usage

### Register user bot
Follow the instructions from [telegram.org](https://core.telegram.org/api/obtaining_api_id) to create you Telegram Application for get `api_id` and `api_hash` values.

### Start redis server
You need to start or use an existing redis server. You will need **ip** and **port** to configure the bot.

### Edit config file
Add all available information to the .env file. Refer to the [Configuration](#configuration) section for more details.

### Start tester bot

### Create connection with tests

> **Note!** You can use the bot for **any tool and programming language** where you can create a Redis client. Below is an example for Python tests

Create fixture with RedisClient. Here`s example

```python
from pytest import fixture

from utils.redis_controller import RedisController

@fixture(scope='function')
def tester_bot():
    redis = RedisController(
        host='localhost',
        port=6379,
    )
    redis.clear_all()
    yield redis
    redis.clear_all()
```

### Use
Use this fixture in your tests

```python
import time


def test_example(tester_bot):
    tester_bot.send_message()
    assert tester_bot.get_last_message() == "Hello, I am a bot!"
```

<a name="configuration"></a>
## Configuration

(TODO: Information on configuring the bot, perhaps using a configuration file or command line arguments. Mention any important settings or options that the user should be aware of.)

<a name="contributing"></a>
## Contributing

Contributions are welcomed! If you have suggestions, bug reports, or would like to contribute code, please open an issue or a pull request.

<a name="license"></a>
## License

This project is licensed under the MIT License - see the LICENSE file for details.

<a name="contact"></a>
## Contact

For questions or feedback, please reach out at Telegram @dikobra4 :)

## TODO
- [ ] Add a logging system for logging the interaction between the test bot and the bot under test
- [ ] Add the ability to use other tools for transferring messages (RabbitMQ. Kafka, ZeroMQ, NATS)
- [ ] Add helpers to create waits in tests (e.g., waiting for messages to appear in the queue)
- [ ] Consider having the bot interact with callback buttons and send media 