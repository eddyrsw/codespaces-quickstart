from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

class ActionCheckProfile(Action):
    def name(self) -> str:
        return "action_check_profile"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        url = 'https://dummy-json.mock.beeceptor.com/posts/1'
        response = requests.get(url)
        return [SlotSet("my_profile", response.json())]
