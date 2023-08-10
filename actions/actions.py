# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import json
import requests
import pandas as pd
import os.path
import sys
from typing import Dict, Text, Any, List
import logging
from dateutil import parser
import sqlalchemy as sa
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.interfaces import Action
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

class ActionShowBalance(Action):

    def name(self) -> Text:
        return "action_check_balance"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        url = 'http://localhost:3000/api/transactions/getdetails'
        ID = str(tracker.sender_id)
        # print(ID)
        headers = {'Content-Type': 'application/json', 'auth-token': ID}

        response = requests.get(url, headers=headers).json()
        # print(response)
        bankBalance = str(response["bankBalance"])
        dispatcher.utter_message("Your Balance is Rs. " + bankBalance)

        return []

class ActionTransferMoney(Action):

    def name(self) -> Text:
        return "action_transfer_money"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        amount_of_money = float(tracker.get_slot("amount_to_transfer"))
        recipient = tracker.get_slot("recipient_upi")
        recipient_name = tracker.get_slot("recipient_name")
        # pin = tracker.get_slot("pin")
        ID = str(tracker.sender_id)
        url = 'http://localhost:3000/api/transactions/transfer'
        data = {
            "toEmail": recipient,
            "amount": amount_of_money,
        }
        headers = {'Content-Type': 'application/json', 'auth-token': ID}
        response = requests.post(url, json=data, headers=headers).json()
        print(response)
        if 'err' in response:
            result = response['err']
        else:
            result = "Transaction was Successful 😎😎\n"
            if not recipient_name:
                result += "You sent ₹ {} to UPI ID -> {}".format(amount_of_money,recipient)
            else:
                result += "You sent ₹ {} to {}'s UPI ID -> {}".format(amount_of_money,recipient_name,recipient)

        # print(result)
        dispatcher.utter_message(result)

        return [AllSlotsReset()]

class ActionCheckLogs(Action):

    def name(self) -> Text:
        return "action_check_logs"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        url = 'http://localhost:3000/api/transactions/list'
        ID = str(tracker.sender_id)
        headers = {'Content-Type': 'application/json', 'auth-token': ID}

        response = requests.get(url, headers=headers).json()
        # print(response)

        c = 1
        for log in response:
            result = "Transaction Log ({}) :-\n".format(c)
            result += "From: " + log["fromEmail"] + "\n"
            result += "To: " + log["toEmail"] + "\n"
            result += "Amount: " + str(log['amount']) + "\n"
            result += "Date: " + log['date'] + "\n"
            c = c+1
            dispatcher.utter_message(result)

        return []