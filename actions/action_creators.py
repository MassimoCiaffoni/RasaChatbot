from cgitb import reset
import json
from pathlib import Path
from typing import Any, Text, Dict, List
import requests
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet



class ActionGetCreator(Action):
    
    def name(self) -> Text:
        return "action_get_creator"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('creator')
        print(name)
        if name is not 'None':
            r=requests.get(url='https://api.rawg.io/api/creators?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name))
            if r.status_code ==200:
                data = r.json()
                creator_name=data['results'][0]['name']
                
            else: output = "I couldnt find this creator"
        else:
            output = "I couldnt find this creator"
        
        dispatcher.utter_message(text=output)
        return []