import boto3
import os
from dotenv import load_dotenv
from termcolor import colored

load_dotenv(verbose=True)

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
)