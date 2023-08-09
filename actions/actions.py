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

import requests
from typing import Dict, Text, Any, List
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.interfaces import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

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
        print(response)
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
        recipient_name = tracker.get_slot("recipient_name",None)
        # pin = tracker.get_slot("pin")
        ID = str(tracker.sender_id)
        url = 'http://localhost:3000/api/transactions/transfer'
        data = {
            "toEmail": recipient,
            "amount": amount_of_money,
        }
        headers = {'Content-Type': 'application/json', 'auth-token': ID}
        response = requests.post(url, json=data, headers=headers).json()
        if 'err' in response:
            result = response['err']
        else:
            result = "Transaction was Successful 😎😎\n"
            if not recipient_name:
                result += "You sent ₹ {} to UPI ID -> {}".format(amount_of_money,recipient)
            else:
                result += "You sent ₹ {} to {}'s UPI ID -> {}".format(amount_of_money,recipient_name,recipient)

        # print(response)
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
        print(response)

        for i in response:
            string_1 = "From:" + str(i['fromEmail']) + "\n"
            string_1 += "To: " + str(i['toEmail']) + "\n"
            string_1 += "Amount: " + str(i['amount']) + "\n"
            string_1 += "Date: " + str(i['date']) + "\n"
            string_2 = string_1.replace(",", "\n")
            dispatcher.utter_message("Transaction log ({}) : \n".format(i+1) + string_2)

        return []