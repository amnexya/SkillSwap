# SkillSwap

<img width="1200" height="600" alt="SkillSwap(1)" src="https://github.com/user-attachments/assets/86db152d-91bd-4bf4-9d5a-77f7f1674771" />

SkillSwap is a platform for University students to use credits in exchange for services, help with assignments, borrowing or buying used items, etc... Think Craigslist except centralised for one University.

To sign up, a university email will be required, this will place you in the correct group for your area.

## File Descriptions

`compose.yml` - template for building SkillSwap docker image.

`requirements.txt` - pip package list, install when creating a venv

`config.py` - contains flask configuration loaded from the class `Config`.

`launch.py` - wrapper for launching server, can be run with `./launch.py {args}`

`app/__init__.py` - initial setup for flask app, contains basic bootstraps to get the server up and running.

## Testing

To test the app, ensure you have a MariaDB server running on your machine, to allow SkillSwap to communicate with this server, you should create a .env file in this directory and enter the correct info as shown below.

```bash
touch /path/to/SkillSwap/.env

# open .env in your text editor of choice
nvim .env

# .env - REPLACE VALUES WITH YOUR OWN DETAILS
SKILLSWAP_DB_NAME=skillswapdb
SKILLSWAP_DB_USER=skillswap
SKILLSWAP_DB_PASS=nobodywilleverguessthis
```