import os
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice

# INIT App
app = Chalice(app_name='straightUpBE')
app.debug = True

# Fetching Data from the Front End - CORS
app.api.cors = True

# Global Variables
dynamodb = boto3.resource('dynamodb')

# USING .ENV Variables
# dynamodb_table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])
dynamodb_table = dynamodb.Table('su_user')


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

    # Put new data in dynamo
    try:
        dynamodb_table.put_item(
            Item={
                'username': new_user_data['username'],
                'password': new_user_data['password'],
                'firstName': new_user_data['firstName'],
                'lastName': new_user_data['lastName'],
                'email': new_user_data['email'],
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    except Exception as error:
        print(error)

    # Fetch data and return it to the front end
    try:
        response = dynamodb_table.get_item(Key={'username': new_user_data['username']})
        user_elements_be = response['Item']
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return user_elements_be


@app.route('/login', methods=['POST'])
def login():
    """
    Logging in User - Given data from the Front End
    :return: User Data (Dynamo), if login is successful
    """

    # Login Data from FE
    user_data = app.current_request.json_body

    try:
        response = dynamodb_table.get_item(Key={'username': user_data['username']})
        if response['Item']:
            user_elements_be = response['Item']
            verification = verify_user(user_data, user_elements_be)
            if verification:
                return user_elements_be
        raise KeyError('User not in the system.')
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return None


def verify_user(front_end_data, back_end_data):
    """
    Verifying User Information
    :param front_end_data: Data from FE Form
    :param back_end_data: Data from Dynamo Database
    :return: Boolean value - Username and Passwords are the same
    """
    return front_end_data['username'] == back_end_data['username'] \
           and front_end_data['password'] == back_end_data['password']


if __name__ == "__main__":
    print(os.environ)
