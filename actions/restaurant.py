from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

class ActionListRestaurants(Action):
    def name(self) -> str:
        return "action_list_restaurants"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        url = 'https://restaurant-booker-rasa.replit.app/api/restaurants'
        response = requests.get(url)
        # Convert response to JSON
        data = response.json()

        # Extract restaurant names
        restaurant_names = [restaurant['name'] for restaurant in data['restaurants']]
        restaurant_list = "".join([f"- {c} \n" for c in restaurant_names ])

        return [SlotSet("restaurants", restaurant_list )]
