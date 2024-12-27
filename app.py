from flask import Flask, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

GRAPHQL_URL = os.getenv("GRAPHQL_URL")
HEADERS = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "utf-8",
    "Referer": "https://wellfound.com/jobs/messages/966605550",
    "content-type": "application/json",
    "x-requested-with": "XMLHttpRequest",
    "x-apollo-signature": os.getenv("APOLLO_SIGNATURE"),
    "apollographql-client-name": "talent-web",
    "x-apollo-operation-name": "CandidateConversationList",
    "x-angellist-dd-client-referrer-resource": "/jobs/messages/:id?",
    "Origin": "https://wellfound.com",
    "Connection": "keep-alive",
    "Cookie": f"ajs_anonymous_id={os.getenv('AJS_ANONYMOUS_ID')}; _wellfound={os.getenv('WELLFOUND_COOKIE')}; datadome={os.getenv('DATADOME_COOKIE')}; cf_clearance={os.getenv('CF_CLEARANCE')}; _mkra_stck={os.getenv('MKRA_STCK')}",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "same-origin",
    "Sec-Fetch-Site": "same-origin",
    "DNT": "1",
    "Sec-GPC": "1",
    "Priority": "u=4"
}

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    thread_url = data.get("thread_url", "")
    response_message = data.get("response", "")
    
    if not thread_url or not response_message:
        return jsonify({"error": "Thread URL and response message cannot be empty"}), 400
    
    try:
        thread_id = thread_url.split("/")[-1]
        if not thread_id:
            return jsonify({"error": "Invalid thread URL"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid thread URL: {str(e)}"}), 400

    payload = {
        "operationName": "CreateConversationResponse",
        "variables": {
            "input": {
                "id": "966605550",
                "type": "JOBPAIRING",
                "availability": "",
                "phoneNumber": "",
                "response": response_message
            }
        },
        "extensions": {
            "operationId": "tfe/ae83816daecbdf89aa14bf87dcae8984591e62616ca1f4f51ee4484755887aa8"
        }
    }

    headers = {
        "User-Agent": os.getenv("USER_AGENT"),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "utf-8",
        "Referer": f"https://wellfound.com/jobs/messages/966605550",
        "content-type": "application/json",
        "Origin": "http://localhost:8501/",
        "Cookie": f"_wellfound={os.getenv('WELLFOUND_COOKIE')}; ajs_anonymous_id={os.getenv('AJS_ANONYMOUS_ID')}; cf_clearance={os.getenv('SEND_MESSAGE_CF_CLEARANCE')}; datadome={os.getenv('SEND_MESSAGE_DATADOME')}"
    }

    try:
        response = requests.post(GRAPHQL_URL, headers=headers, json=payload)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            try:
                response_json = response.json() 
                return jsonify({"success": True, "message": "Message sent successfully", "data": response_json}), 200
            except json.JSONDecodeError:
                return jsonify({"error": "Received non-JSON response", "details": response.text}), 400
        else:
            return jsonify({"error": "Failed to send message", "details": response.text}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500

@app.route('/display_conversation', methods=['GET'])
def display_conversation():
    response_data = {
        "data": {
            "conversation": {
                "__typename": "Conversation",
                "id": "JobPairing-966605550",
                "isNewlyAcceptedJobApplication": False,
                "messages": {
                    "__typename": "MessageConnection",
                    "edges": [
                        {
                            "__typename": "MessageEdge",
                            "node": {
                                "__typename": "Message",
                                "attachments": None,
                                "availability": None,
                                "body": None,
                                "id": "JobPairing-966605550",
                                "modelId": "966605550",
                                "modelType": "JOBPAIRING",
                                "phoneNumber": None,
                                "sender": {
                                    "__typename": "TalentUser",
                                    "avatarUrl": "https://photos.wellfound.com/users/17569213-medium_jpg?1706505550",
                                    "firstName": "AYUSH",
                                    "id": "User-17569213",
                                    "name": "AYUSH SINGH",
                                    "slug": "ayush-singh-392"
                                },
                                "sentAt": 1734963178,
                                "systemMessageType": "APPLICATION",
                                "timekitBooking": None
                            }
                        },
                        {
                            "__typename": "MessageEdge",
                            "node": {
                                "__typename": "Message",
                                "attachments": [],
                                "availability": None,
                                "body": "Hey,\nWe like your profile and believe that you could be a potential fit for the position. We invite you to complete a small task. You are to build a web application that can send a message on wellfound in this thread. You should have a python flask based backend server that will make the request to send the message here on wellfound and a simple UI to go with it where we can enter a message to send to this thread.\n\nWe expect you to complete this task in 3 days from now.\n\nOnce done, send us the repository link and a screen recording on the functional app here. For the screen recording you can use the repo itself or platforms like look, whatever is convenient to you.",
                                "id": "ConversationMessage-21324601",
                                "modelId": "21324601",
                                "modelType": "CONVERSATIONMESSAGE",
                                "phoneNumber": None,
                                "sender": {
                                    "__typename": "TalentUser",
                                    "avatarUrl": "https://photos.wellfound.com/users/15335954-medium_jpg?1665985463",
                                    "firstName": "Utsav",
                                    "id": "User-15335954",
                                    "name": "Utsav Singla",
                                    "slug": "utsav-singla-3"
                                },
                                "sentAt": 1735229388,
                                "systemMessageType": None,
                                "timekitBooking": None
                            }
                        },
                        {
                            "__typename": "MessageEdge",
                            "node": {
                                "__typename": "Message",
                                "attachments": None,
                                "availability": "",
                                "body": "Does, wellfound have any official Api's to do that?",
                                "id": "AList::ConversationResponse-1792857",
                                "modelId": "1792857",
                                "modelType": "ALIST__CONVERSATIONRESPONSE",
                                "phoneNumber": "",
                                "sender": {
                                    "__typename": "TalentUser",
                                    "avatarUrl": "https://photos.wellfound.com/users/17569213-medium_jpg?1706505550",
                                    "firstName": "AYUSH",
                                    "id": "User-17569213",
                                    "name": "AYUSH SINGH",
                                    "slug": "ayush-singh-392"
                                },
                                "sentAt": 1735286177,
                                "systemMessageType": None,
                                "timekitBooking": None
                            }
                        }
                    ]
                },
                "modelId": "966605550",
                "modelType": "JOBPAIRING",
                "status": "ACCEPTED"
            },
            "schemaVersion": 2
        }
    }

    conversation = response_data['data']['conversation']
    messages = conversation['messages']['edges']

    conversation_info = f"Conversation ID: {conversation['id']}\n"
    conversation_info += f"Status: {conversation['status']}\n"
    conversation_info += f"Newly Accepted Job Application: {conversation['isNewlyAcceptedJobApplication']}\n\n"
    
    messages_info = "Messages:\n"
    
    for message_edge in messages:
        message = message_edge['node']
        sender_name = message['sender']['name']
        message_body = message['body'] if message['body'] else "No body"
        sent_at = message['sentAt']

        messages_info += f"Sender: {sender_name}\n"
        messages_info += f"Message: {message_body}\n"
        messages_info += f"Sent at: {sent_at}\n\n"

    return jsonify({"conversation": conversation_info, "messages": messages_info})



if __name__ == '__main__':
    app.run(debug=True)
