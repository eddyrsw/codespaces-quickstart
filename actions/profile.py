from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests
import json
import re

base_url = 'https://swipe-connect-eddyrajiah.replit.app/api'

class ActionRegisterUser(Action):
    def name(self) -> str:
        return "action_register_user"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        url = base_url + '/users/register'
        first_name = tracker.get_slot("first_name")
        # first_name = "textuser111"

        data = {
            "username": first_name,
            "email": first_name + "@swipe-connect.com",
            "password": "A12345678"
        }
        response = requests.post(url, json=data)
        # Convert response to JSON
        resp = response.json()
        user_id = resp.get('user_id')
        print(user_id)
        SlotSet("user_id", user_id )
        user_id_saved = tracker.get_slot("user_id")
        print(f'user_id_saved= {user_id_saved}')

        # return [SlotSet("response", resp )]
        return [SlotSet("user_id", user_id )]

class ActionCreateProfile(Action):
    def name(self) -> str:
        return "action_create_profile"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        url = base_url + '/profiles'

        interests = tracker.get_slot("interests")
        my_interests = re.split(r'[, ]+', interests.strip())

        data = {
            "user_id": tracker.get_slot("user_id"),
            "name": tracker.get_slot("full_name"),
            "age": tracker.get_slot("age"),
            "gender": tracker.get_slot("gender"),
            "bio": tracker.get_slot("bio"),
            "interests": my_interests,
            "preferences": {
                "gender": tracker.get_slot("prefered_gender"),
                "min_age": 25,
                "max_age": 35,
                "distance": 50
            },
            "location": {
                "lat": 40.7128,
                "lon": -74.0060,
                "city": "New York"
            },
            "photos": []
        }
        response = requests.post(url, json=data)
        # Convert response to JSON
        resp = response.json()

        return [SlotSet("response", resp )]