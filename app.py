import os
import boto3
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
    return {'BACK END AWS CHALICE - STRAIGHT UP'}


@app.route('/create_user', methods=['POST'])
def create_user():
    # New Account Data from FE
    new_user_data = app.current_request.json_body

    try:
        dynamodb_table.put_item(
            Item={
                'username': new_user_data.username,
            }
        )
    except Exception as error:
        print(error)


if __name__ == "__main__":
    print(os.environ)
