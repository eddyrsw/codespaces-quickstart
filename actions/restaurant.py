from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

base_url = 'https://restaurant-booker-rasa.replit.app'

restaurant_data = {}

class ActionListRestaurants(Action):
    def name(self) -> str:
        return "action_list_restaurants"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        url = base_url + '/api/restaurants'
        response = requests.get(url)
        # Convert response to JSON
        global restaurant_data
        restaurant_data = response.json()

        # Extract restaurant names
        restaurants = [restaurant['name'] for restaurant in restaurant_data['restaurants']]
        restaurant_list = "".join([f"- {c} \n" for c in restaurants ])

        return [SlotSet("restaurants", restaurant_list )]

class ActionGetRestaurantDetails(Action):
    def name(self) -> str:
        return "action_get_restaurant_details"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        # print(tracker.get_slot("restaurant_name"))
        # print(restaurant_data)

        restaurant_id = next((r["id"] for r in restaurant_data['restaurants'] if r["name"].lower() == tracker.get_slot("restaurant_name").lower()), None)

        # print(restaurant_id)

        url = base_url + f'/api/restaurants/{restaurant_id}'
        response = requests.get(url)
        # Convert response to JSON
        resp = response.json()
        restaurant_details = f"{resp.get('name')}, serves {resp.get('cuisine')} food, located at {resp.get('address')}. Opens at {resp.get('opening_time')}, closes at {resp.get('closing_time')}"

        return [SlotSet("restaurant_details", restaurant_details )]
    

class ActionCreateRestaurantBooking(Action):
    def name(self) -> str:
        return "action_create_restaurant_booking"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        # print(tracker.get_slot("restaurant_name"))
        # print(restaurant_data)
        restaurant_name = tracker.get_slot("restaurant_name")

        restaurant_id = next((r["id"] for r in restaurant_data['restaurants'] if r["name"].lower() == restaurant_name.lower()), None)

        print(restaurant_id)

        data = {
            "restaurant_id": restaurant_id,
            "customer_name": "Customer name",
            "customer_email": "email@example.com",
            "customer_phone": "5128881111",
            "party_size": 2,
            "date": tracker.get_slot("booking_date"),
            "time": tracker.get_slot("booking_time"),
            "special_requests": ""
        }

        url = base_url + f'/api/bookings'
        response = requests.post(url, json=data)
        # Convert response to JSON
        resp = response.json()
        print(resp)
        restaurant_booking_details = f"I have you booked for a table for {resp.get('party_size')}, at {restaurant_name}, at {resp.get('time')} on {resp.get('date')}"

        return [SlotSet("restaurant_booking_details", restaurant_booking_details )]