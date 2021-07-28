# Base Imports
import os
from chalice import Chalice

# Function Imports
from chalicelib import login, createUser

# INIT App
app = Chalice(app_name='straightUpBE')
app.debug = True

# Fetching Data from the Front End - CORS
app.api.cors = True


@app.route('/')
def index():
    """
    :return: INTRO to Chalice Deploy
    """
    return 'BACK END AWS CHALICE - STRAIGHT UP'


@app.route('/create_user', methods=['POST'])
def create_user():
    """
    Create Entry in Dynamo - User Data (FE)
    :return: User Information
    """

    # New Account Data from FE
    new_user_data = app.current_request.json_body
    createUser.main(new_user_data)


@app.route('/login', methods=['POST'])
def login():
    """
    Logging in User - Given data from the Front End
    :return: User Data (Dynamo), if login is successful
    """

    # Login Data from FE
    user_data = app.current_request.json_body
    login.main(user_data)


if __name__ == "__main__":
    print(os.environ)
