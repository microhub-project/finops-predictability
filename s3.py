from dotenv import load_dotenv
import os, boto3

load_dotenv()

def connect():
    session = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        aws_session_token=os.getenv("aws_session_token"),
        region_name="us-east-1",
    )

    return session.client("s3")