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
        return "action_find_date"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        # hardcoded profile to be used as a date
        url = base_url + '/profiles/27'

        response = requests.get(url)
        # Convert response to JSON
        resp = response.json()
        my_interests = ", ".join(resp.get('interests'))
        profile = f"{resp.get('name')}, {resp.get('age')} in {resp.get('location').get('city')}. She's into {my_interests}"

        return [SlotSet("date_profile", profile )]