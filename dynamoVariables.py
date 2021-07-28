import boto3

# Global Variables
dynamodb = boto3.resource('dynamodb')

# USING .ENV Variables
# dynamodb_table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])
dynamodb_table = dynamodb.Table('su_user')