"""Small example of a dashboard that allows subscribing/unsubscribing from SNS topics."""

from os import environ as ENV

from dotenv import load_dotenv
import streamlit as st
from boto3 import client

def verify_email(email: str, config):

    ses = client("ses", aws_access_key_id=config["AWS_KEY"], aws_secret_access_key=config["AWS_SECRET"])

    if email not in ses.list_identities(IdentityType = 'EmailAddress')["Identities"]:
        res = ses.verify_email_identity(EmailAddress=email)
        return res

def subscribe_to_topic(email: str, config):

    sns = client("sns", aws_access_key_id=config["AWS_KEY"], aws_secret_access_key=config["AWS_SECRET"])

    result = sns.subscribe(
        TopicArn=config["TOPIC_ARN"],
        Protocol='email',
        Endpoint=email,
        ReturnSubscriptionArn=True
    )

    # sns.publish(TopicArn=config["TOPIC_ARN"],
    #             Message=f"New subscriber: {email}",
    #             Subject="New subscriber!")
    
    return result

if __name__ == "__main__":

    load_dotenv()

    st.title("Newsletter subscription")
    st.subheader("All the updates, all the time!")

    email = st.text_input("Enter your email to win BIG PRIZES!")
    clicked = st.button("Subscribe NOW", on_click=lambda: subscribe_to_topic(email, ENV))
    if clicked:
        st.write("Congratulations! Today is the first day of the rest of your life!")
        st.write("Check your email to confirm.")