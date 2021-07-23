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
    return {'BACK END AWS CHALICE - STRAIGHT UP'}


@app.route('/create_user', methods=['POST'])
def create_user():
    """
    Create Entry in Dynamo - User Data (FE)
    :return: User Information
    """

    # New Account Data from FE
    new_user_data = app.current_request.json_body

    try:
        dynamodb_table.put_item(
            Item={
                'username': new_user_data.username,
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    except Exception as error:
        print(error)


@app.route('/login', methods=['POST'])
def login():
    """
    Logging in User - Given data from the Front End
    :return: User Data (Dynamo), if login is successful
    """

    # Login Data from FE
    user_data = app.current_request.json_body

    try:
        response = dynamodb_table.get_item(Key={'username': user_data.username})
        user_elements_be = response['Item']
        verification = verify_user(user_data, user_elements_be)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if verification:
            return user_elements_be


def verify_user(front_end_data, back_end_data):
    """
    Verifying User Information
    :param front_end_data: Data from FE Form
    :param back_end_data: Data from Dynamo Database
    :return: Boolean value - Username and Passwords are the same
    """
    return front_end_data.username == back_end_data.username and front_end_data.password == back_end_data.password


if __name__ == "__main__":
    print(os.environ)
