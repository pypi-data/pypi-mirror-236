import json
import random

from autonomous import log
from autonomous.ai import OpenAI

from dmtoolkit.models.location import Location
from dmtoolkit.models.ttrpgobject import TTRPGObject


class City(TTRPGObject):
    attributes = TTRPGObject.attributes | {
        "population": 0,
        "traits": "",
        "factions": [],
        "locations": {},
    }

    personality = {
        "social": [
            "bohemian",
            "decedent",
            "snooty",
            "aggressive",
            "proud",
            "distrustful",
        ],
        "political": [
            "Anarchic",
            "Aristocratic",
            "Authoritarianist",
            "Bureaucratic",
            "Confederationist",
            "Colonialist",
            "Communist",
            "Democratic",
            "Fascist",
            "Kleptocratic",
            "Meritocratic",
            "Militaristic",
            "Monarchic",
            "Theocratic",
            "Totalitarian",
            "Tribalist",
        ],
        "economic": [
            "palace",
            "capitalist",
            "mercantilist",
            "proprietist",
            "fuedalist",
            "socialist",
        ],
        "size": [
            "village",
            "town",
            "city",
        ],
    }

    funcobj = {
        "name": "generate_city",
        "description": "completes City data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The city's name",
                },
                "population": {
                    "type": "integer",
                    "description": "The city's population",
                },
                "backstory": {
                    "type": "string",
                    "description": "A short history of the city in 750 words or less",
                },
                "desc": {
                    "type": "string",
                    "description": "A physical description of the appearance of the city in 500 words or less.",
                },
                "districts": {
                    "type": "array",
                    "description": "The names of the districts in the city, if present",
                    "items": {"type": "string"},
                },
            },
        },
    }

    @property
    def districts(self):
        return list(self.locations.keys())

    @classmethod
    def generate(cls, world, description=None):
        primer = f"""
        As an expert AI in Worldbuilding for {world.genre} TTRPGs, generate a fictional city complete with a name, population, description, and districts.
        """

        traits = ", ".join(
            [random.choice(traits) for traits in cls.personality.values()]
        )
        prompt = f"Generate a fictional {world.genre} city within a region described as {description}. The city should have the following characteristics: {traits}. Write a detailed city description containing an unusual, wonderful, OR sinister secret hidden within the city."

        obj_data = super().generate(primer, prompt)

        if districts := obj_data.pop("districts", None):
            obj_data["locations"] = dict(zip(districts, [[] for _ in districts]))

        obj_data |= {"world": world, "traits": traits}
        city = cls(**obj_data)
        city.save()
        return city

    def citizens(self):
        lctns = [l for locations in self.locations.values() for l in locations]
        cit = []
        for l in lctns:
            cit += l.inhabitants
        return cit

    def get_image_prompt(self):
        return f"""Create a full color, high resolution overhead illustrated map view of a {self.traits} called {self.name} of size {self.population} with the following districts: {', '.join(self.districts)}. The map should be detailed enough to use as a battlemap for a 5 person encounter. 
        """

    def add_locations(self, n=1, owner=False):
        for _ in range(n):
            ltype = random.choice(
                [
                    "An armorer shop",
                    "A weapon shop",
                    "A general store",
                    "A magic shop",
                    "A cheap inn",
                    "A seedy pub",
                    "An NPC's residence",
                    "A library",
                    "A secretive temple",
                    "A looming fortress",
                    "A prison or dungeon",
                    "An interesting and explorable point of interest that subverts expections",
                ]
            )
            district = random.choice(self.districts)
            prompt = f"{random.choice(ltype)} in the {district} district in a {', '.join(self.traits)} of size {self.population} people."
            location = Location.generate(self.world, description=prompt)
            location.add_inhabitant(owner=owner)
            self.locations[district].append(location)

        self.save()
