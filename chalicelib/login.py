# Imports
from botocore.exceptions import ClientError
from dynamoVariables import dynamodb_table


def verify_user(front_end_data, back_end_data):
    """
    Verifying User Information
    :param front_end_data: Data from FE Form
    :param back_end_data: Data from Dynamo Database
    :return: Boolean value - Username and Passwords are the same
    """
    return front_end_data['username'] == back_end_data['username'] \
           and front_end_data['password'] == back_end_data['password']


# Main Method
def main(user_data):
    """
    Logging in User - Given data from the Front End
    :return: User Data (Dynamo), if login is successful
    """
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
