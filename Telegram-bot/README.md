# Telegram Bot

## Description
A simple Telegram bot for user registration and verification.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/telegram-bot.git
    cd telegram-bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on `.env.example` and fill in your details:
    ```sh
    cp .env.example .env
    ```

## Usage
1. Run the bot:
    ```sh
    python app/main.py
    ```

2. Interact with the bot on Telegram using the commands:
    - `/start` - Start the bot
    - `/register` - Register a user
    - `/admin` - Admin commands

## Testing
Run the tests using:
```sh
python -m unittest discover tests
```

## Docker
1. Build the Docker image:
    ```sh
    docker build -t telegram-bot .
    ```

2. Run the Docker container:
    ```sh
    docker run -d --name telegram-bot telegram-bot
    ```