# Tweeter

![logo](./src/media/logo.png)

Tweeter is a web app that uses AI to create tweet drafts, which you can post in a single click!

## Installation & Setup
1. Clone the repository by running the command below or clicking [here](https://github.com/vismodo/tweeter/archive/refs/heads/main.zip)
    ```bash
    $ git clone https://github.com/vismodo/tweeter.git
    ```
2. Navigate to the repository
    ```bash
    $ cd tweeter
    ```
3. Initialise a virtual environment and install the requirements
    ```bash
    $ virtualenv tweeter_env # Create a python virtual environment
    $ source twitter_env/bin/activate # On Linux
    $ tweeter_env\Scripts\activate.bat # On Windows
    $ pip install -r requirements.txt # Install dependencies
    $ cd src
    ```

4. Modify the file `src/settings.json` to match your requirements.

5. Create an app in the [Twitter Developer Dashboard](https://developer.twitter.com/en/portal/dashboard) and copy the OAuth credentials to `src/.env`

## Usage

1. Run the main server script (Using flask)
    ```bash
    $ cd tweeter/src
    $ source ../twitter_env/bin/activate # On Linux
    $ ../tweeter_env\Scripts\activate.bat # On Windows
    $ flask --app main run
    ```
    You can find the web app running at `http://localhost:5000/`
2. Run the background thinker service (optional) in a new terminal instance
    ```bash
    $ cd tweeter/src
    $ source ../twitter_env/bin/activate # On Linux
    $ ../tweeter_env\Scripts\activate.bat # On Windows
    $ python thinker.py # Run the script
    ```

## Credits

[@vismodo](https://github.com/vismodo)

## FAQ
### Can I run this on a Raspberry Pi?
> Yes, you can. Just use `--host 0.0.0.0` when running the flask server.