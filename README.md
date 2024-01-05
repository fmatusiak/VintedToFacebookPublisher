# VintedToFacebookPublisher

The "VintedToFacebookPublisher" application is designed to extract data from the Vinted platform

using Selenium and automatically share it on a specified Facebook page through the Facebook API.

## Configuration

**Important Note:**

Before running the application, make sure you are logged in to Vinted on the specified profile in the Chrome browser

and make sure you have Python installed. Install the required dependencies using the following command:

**pip install -r requirements.txt**

The `chrome_user_data_dir` directory should contain the user data for an authenticated Vinted session.

Create a `config.json` file with the necessary access credentials:

```json
{
  "facebook": {
    "name": "Your Facebook Page Name",
    "id": "Your Facebook Page ID",
    "token": "Your Facebook Access Token"
  },
  "vinted": {
    "base_url_profile": "Your Vinted Profile URL",
    "member": "Your Vinted Member ID"
  },
  "chrome_user_data_dir": "Your Chrome User Data Directory",
  "db_host": "Your Database Host",
  "db_user": "Your Database User",
  "db_password": "Your Database Password",
  "db_name": "Your Database Name"
}
```

Replace the placeholder values with your actual credentials and information.

The application allows you to use a template configuration from a .config.json file. To view and copy the template
configuration, you can open the .config.json file and copy the content.
Alternatively, you can remove the dot (.) from .config.json and use it as a regular configuration file.

## Database Setup

Create a new database with the specified name in the config.json file.
In the CreateTablesSql directory, you will find SQL files containing table creation scripts.

Run these SQL files using a database management tool or command-line interface to create the required tables.

**Example using MySQL command-line interface:**

mysql -h YourDatabaseHost -u YourDatabaseUser -pYourDatabasePassword YourDatabaseName <
CreateTablesSql/vinted_facebook_photo.sql

## Run the application

python main.py

