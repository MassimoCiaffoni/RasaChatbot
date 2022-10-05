# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
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
class ActionSearchGame(Action):
    
    def name(self) -> Text:
        return "action_search_game"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('game')
        numero = tracker.get_slot('number')
        indice = tracker.get_slot('index')
        print(name)
        print(numero)
        print(indice)
        if(indice> 4):
            output="I didn't find your game try to ask me again later"
            dispatcher.utter_message(text=output)
            return[AllSlotsReset()]
        if numero == 'None':
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name)) 
            if r.status_code == 200:
                data = r.json()
                #print(len(data['results']))
                if indice > len(data['results']):
                    output="I couldn't find the game. Try to use less characters"
                else:
                    nome = data['results'][indice]['name'] #nome videogame
                    if 'None' in nome:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                        dispatcher.utter_message(text=output)
                        return [AllSlotsReset()]
                    else:
                        image = data['results'][indice]['background_image']
                        release_date = data['results'][indice]['released']
                        metacritic_score = data['results'][indice]['metacritic']
                        if data['results'][indice]['esrb_rating'] == None:
                            esb_rate= None
                        else:
                            #print(data['results'][indice]['esrb_rating'])
                            esb_rate = data['results'][indice]['esrb_rating']['name']
                        genres = data['results'][indice]['genres']
                        generi= []
                        string_genres=""
                        for elem in genres:
                            generi.append(elem['name'])
                            print(generi)
                        for elem in generi:
                            string_genres=string_genres+elem+", "
                        id_game = data['results'][indice]['id']
                        r2= requests.get(url='https://api.rawg.io/api/games/{}?key=bbac0252b5ed4a2b8286472063cb2dfe'.format(id_game))
                        game_data = r2.json()
                        print(game_data)
                        try:
                            publishers = game_data['publishers'][0]['name']
                            print(publishers)
                        except:
                            publishers = "None"
                        try: 
                            developers = game_data['developers'][0]['name']
                            print(developers)
                        except:
                            developers = "None"
                        print(publishers)
                        print(developers)
                        output="{} it's an {} game and it was developed by {} and published by {} on {}. It has a metacritc score of {} and it has been classified with this tag: {} {}. \n \n Is this the game you wanted? ".format(nome,
                            string_genres,developers, publishers, release_date, metacritic_score, esb_rate, image)
            else:
                output = "I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
        else:
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}%20{}&search_precise=true'.format(name, numero))
            if r.status_code == 200:
                data = r.json()
                #print(len(data['results']))
                if indice > len(data['results']):
                    output="I couldn't find the game. Try to use less characters"
                else:
                    nome = data['results'][indice]['name'] #nome videogame
                    if 'None' in nome:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                        dispatcher.utter_message(text=output)
                        return [AllSlotsReset()]
                    else:
                        image = data['results'][indice]['background_image']
                        release_date = data['results'][indice]['released']
                        metacritic_score = data['results'][indice]['metacritic']
                        if data['results'][indice]['esrb_rating'] == None:
                            esb_rate= None
                        else:
                            #print(data['results'][indice]['esrb_rating'])
                            esb_rate = data['results'][indice]['esrb_rating']['name']
                        genres = data['results'][indice]['genres']
                        generi = []
                        string_genres = ""
                        for elem in genres:
                            generi.append(elem['name'])
                        for elem in generi:
                            string_genres=string_genres+elem+", "
                        id_game = data['results'][indice]['id']
                        print(id_game)
                        r2= requests.get(url='https://api.rawg.io/api/games/{}?key=bbac0252b5ed4a2b8286472063cb2dfe'.format(id_game))
                        game_data = r2.json()
                        print(game_data)
                        try:
                            publishers = game_data['publishers'][0]['name']
                            print(publishers)
                        except:
                            publishers = "None"
                        try: 
                            developers = game_data['developers'][0]['name']
                            print(developers)
                        except:
                            developers = "None"
                        print(publishers)
                        print(developers)
                        output="{} it's an {} game and it was developed by {} and published by {} on {}. It has a metacritc score of {} and it has been classified with this tag: {} {}. \n \n Is this the game you wanted? ".format(nome,
                            string_genres,developers, publishers, release_date, metacritic_score, esb_rate, image)
            else:
                output = "I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"  
        dispatcher.utter_message(text=output)
        return[SlotSet("index", indice+1), SlotSet('game_id', id_game)]


class MyFallback(Action):
    
    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response = "utter_fallback")
        return []

class ActionResetIndex(Action):

    def name(self):
        return "action_reset_index"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("index", 0), SlotSet('number',None)]

class ResetSlot(Action):

    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

class ActionSearchPublisher(Action):
    
    def name(self) -> Text:
        return "action_search_publisher"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('publisher')
        print(name)
        r=requests.get(url='https://api.rawg.io/api/publishers?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name))
        if r.status_code == 200:
            data = r.json() 
            nome = data['results'][0]['name']
            print(nome)
            if 'None' in nome:
                output = "I do not know anything about , what a mistery!? Are you sure it is correctly spelled? Try to use the complete name of the publisher"  
                dispatcher.utter_message(text=output)
                return [AllSlotsReset()] 
            description=""
            games_count = data['results'][0]['games_count']
            top_game = data['results'][0]['top_games'][0]
            publisher_id=data['results'][0]['id']
            print(publisher_id)
            r2=requests.get(url='https://api.rawg.io/api/publishers/{}?key=bbac0252b5ed4a2b8286472063cb2dfe'.format(publisher_id))
            if r2.status_code == 200:
                data2 = r2.json() 
                print(data2)
                description = data2['description']
            print(top_game)
            r3= requests.get(url='https://api.rawg.io/api/games/{}?key=bbac0252b5ed4a2b8286472063cb2dfe'.format(top_game))
            if r3.status_code == 200:
                data3 = r3.json()
                game = data3['name']         
                output="{} {} realeased {} games and one of the most known game of this company is: {}. ".format(description,nome, games_count, game)
            else:
                output = "{} {} realeased {} games.".format(description,nome,games_count)
        else:
            output = "I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
            
        dispatcher.utter_message(text=output)
        return [SlotSet('publisher',None)]

class ActionSearchPlatforms(Action):
    
    def name(self) -> Text:
        return "action_search_platforms"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('game')
        indice = tracker.get_slot('index')
        numero = tracker.get_slot('number')
        print(name)
        print(indice)
        if numero=="None":
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name))
            

            if r.status_code == 200:
                if indice > 0:
                    data = r.json()
                    nome = data['results'][indice - 1]['name'] #nome videogame
                    if 'None' in nome:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    piattaforme = []
                    platforms = data['results'][indice - 1]['platforms']
                    if platforms == 'None':
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    else:
                        for elem in platforms:
                            piattaforme.append(elem['platform']['name'])
                        string_platforms =' '.join(str(elem) for elem in piattaforme)
                        print(string_platforms) 
                        output="{} has been published on the following platforms: {} ".format(nome, string_platforms)
                else:
                    data = r.json()
                    nome = data['results'][indice]['name'] #nome videogame
                    if 'None' in nome:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    piattaforme = []
                    platforms = data['results'][indice]['platforms']
                    if 'None' in platforms:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    else:
                        for elem in platforms:
                            piattaforme.append(elem['platform']['name'])
                        string_platforms =' '.join(str(elem) for elem in piattaforme)
                        print(string_platforms) 
                        output="{} has been published on the following platforms: {} ".format(nome, string_platforms)
            else:
                output = "I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
        else:   
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}%20{}&search_precise=true'.format(name, numero))
            
            if r.status_code == 200:
                if indice > 0:
                    data = r.json()
                    nome = data['results'][indice - 1]['name'] #nome videogame
                    if 'None' in nome:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    piattaforme = []
                    platforms = data['results'][indice - 1]['platforms']
                    if platforms == 'None':
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    else:
                        for elem in platforms:
                            piattaforme.append(elem['platform']['name'])
                        string_platforms =' '.join(str(elem) for elem in piattaforme)
                        print(string_platforms) 
                        output="{} has been published on the following platforms: {} ".format(nome, string_platforms)
                else:
                    data = r.json()
                    nome = data['results'][indice]['name'] #nome videogame
                    if 'None' in nome:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    piattaforme = []
                    platforms = data['results'][indice]['platforms']
                    if 'None' in platforms:
                        output="I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
                    else:
                        for elem in platforms:
                            piattaforme.append(elem['platform']['name'])
                        string_platforms =' '.join(str(elem) for elem in piattaforme)
                        print(string_platforms) 
                        output="{} has been published on the following platforms: {} ".format(nome, string_platforms)
            else:
                output = "I do not know anything about , what a mistery!? Are you sure it is correctly spelled?"
        dispatcher.utter_message(text=output)
        return []

class ActionSearchScreenshots(Action):
    
    def name(self) -> Text:
        return "action_search_screenshots"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('game')
        indice = tracker.get_slot('index')
        game_id=tracker.get_slot('game_id')
        numero=tracker.get_slot('number')
        print(name)
        print(numero)
        if name is not 'None' and numero=="None" and game_id==0:
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name))
            if r.status_code ==200:
                data = r.json()
                game_id=data['results'][indice]['id']
            else: output = "I couldnt find any screenshots"
        elif name is not 'None' and numero is not 'None' and game_id==0:
                r2=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}%20{}&search_precise=true'.format(name, numero))
                if r2.status_code ==200:
                    data2 = r2.json()
                    game_id=data2['results'][indice]['id']
                else: output = "I couldnt find any screenshots"
        r3 = requests.get(url="https://api.rawg.io/api/games/{}/screenshots?key=bbac0252b5ed4a2b8286472063cb2dfe".format(game_id))

        if r3.status_code ==200:
            data3 = r3.json()
            image = []
            images = data3['results']
            #print(images)
            for elem in images:
                if elem['is_deleted'] == False:
                    image.append(elem['image'])
            print(image)
            string_image='\n'.join(str(elem) for elem in image)
            output = "Here some screenshots: {}".format(string_image)
        else:
            output = "I couldnt find any screenshots"
        
        dispatcher.utter_message(text=output)
        return []


class ActionSearchStoreLink(Action):
    
    def name(self) -> Text:
        return "action_search_store"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('game')
        indice = tracker.get_slot('index')
        game_id=tracker.get_slot('game_id')
        numero=tracker.get_slot('number')
        print(name)
        if name is not 'None' and numero=="None" and game_id==0:
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name))
            if r.status_code ==200:
                data = r.json()
                game_id=data['results'][indice]['id']
            else: output = "I couldnt find any store which sells the game"
        elif numero!='None':
                r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}%20{}&search_precise=true'.format(name, numero))
                if r.status_code ==200:
                    data = r.json()
                    game_id=data['results'][indice]['id']
                else: output = "I couldnt find any store which sells the game"
        r = requests.get(url="https://api.rawg.io/api/games/{}/stores?key=bbac0252b5ed4a2b8286472063cb2dfe".format(game_id))

        if r.status_code ==200:
            data = r.json()
            store_urls = []
            stores = data['results']
            print(stores)
            for elem in stores:
                store_urls.append(elem['url'])            
            store_url='\n'.join(str(elem) for elem in store_urls)
            output = "The game is sold in the following stores: {} ".format(store_url)
        else:
            output = "I couldnt find any store which sells the game"
        
        dispatcher.utter_message(text=output)
        return []


class ActionGetTrailer(Action):
    
    def name(self) -> Text:
        return "action_get_trailer"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('game')
        indice = tracker.get_slot('index')
        game_id=tracker.get_slot('game_id')
        numero=tracker.get_slot('number')
        print(name)
        print(numero)
        print(game_id)
        if name is not 'None' and numero=="None" and game_id==0:
            r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}&search_precise=true'.format(name))
            if r.status_code ==200:
                data = r.json()
                game_id=data['results'][indice]['id']
            else: output = "I couldnt find any store which sells the game"
        elif numero!='None':
                print("dentro elif")
                r=requests.get(url='https://api.rawg.io/api/games?key=bbac0252b5ed4a2b8286472063cb2dfe&search={}%20{}&search_precise=true'.format(name, numero))
                if r.status_code ==200:
                    data = r.json()
                    game_id=data['results'][indice]['id']
                else: output = "I couldnt find any store which sells the game"
        r = requests.get(url="https://api.rawg.io/api/games/{}/movies?key=bbac0252b5ed4a2b8286472063cb2dfe".format(game_id))

        if r.status_code ==200:
            data = r.json()
            trailer_urls = []
            trailers = data['results']
            print(trailers)
            for elem in trailers:
                print(elem['data']['max'])
                trailer_urls.append(elem['data']['max'])            
            trailer_url='\n'.join(str(elem) for elem in trailer_urls)
            output = "Here some trailers of this game: {} ".format(trailer_url)
        else:
            output = "I couldnt find any trailer of the game"
        
        dispatcher.utter_message(text=output)
        return []