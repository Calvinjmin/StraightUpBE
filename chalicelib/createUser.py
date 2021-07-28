# Imports
from botocore.exceptions import ClientError
from dynamoVariables import dynamodb_table


# Main Method
def main(new_user_data):
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
