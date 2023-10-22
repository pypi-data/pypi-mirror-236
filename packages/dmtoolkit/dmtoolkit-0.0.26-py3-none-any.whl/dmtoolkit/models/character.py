import json
import random

from autonomous import log
from autonomous.ai import OpenAI

from dmtoolkit.models.ttrpgobject import TTRPGObject


class Character(TTRPGObject):
    attributes = TTRPGObject.attributes | {
        "npc": True,
        "canon": False,
        "gender": "",
        "occupation": "",
        "goal": "",
        "race": "",
        "hp": 0,
        "str": 0,
        "dex": 0,
        "con": 0,
        "wis": 0,
        "int": 0,
        "cha": 0,
        "dob": "",
        "dod": "",
        "wealth": [],
        "inventory": [],
        "chats": {
            "history": [],
            "summary": "The beginning of a conversation between a TTRPG PC and NPC.",
            "message": "",
            "response": "",
        },
    }
    genders = ["male", "female", "non-binary"]
    personality = {
        "social": [
            "shy",
            "outgoing",
            "friendly",
            "unfriendly",
            "mean",
            "snooty",
            "aggressive",
            "kind",
            "proud",
            "humble",
            "confident",
            "insecure",
            "silly",
            "serious",
        ],
        "political": [
            "smart",
            "sneaky",
            "dumb",
            "loyal",
            "disloyal",
            "dishonest",
            "honest",
            "stubborn",
            "flexible",
            "optimistic",
            "pessimistic",
            "sensitive",
            "insensitive",
            "intuitive",
            "intelligent",
            "wise",
            "foolish",
            "patient",
            "impatient",
            "tolerant",
            "intolerant",
            "forgiving",
            "unforgiving",
        ],
        "professional": [
            "greedy",
            "generous",
            "lazy",
            "hardworking",
            "courageous",
            "cowardly",
            "creative",
            "imaginative",
            "practical",
            "logical",
            "curious",
            "nosy",
            "adventurous",
            "cautious",
            "careful",
            "reckless",
            "careless",
        ],
    }

    funcobj = {
        "name": "generate_npc",
        "description": "completes NPC data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The character's name",
                },
                "age": {
                    "type": "integer",
                    "description": "The character's age",
                },
                "gender": {
                    "type": "string",
                    "description": "The character's gender",
                },
                "race": {
                    "type": "string",
                    "description": "The character's race",
                },
                "traits": {
                    "type": "array",
                    "description": "The character's personality traits",
                    "items": {"type": "string"},
                },
                "desc": {
                    "type": "string",
                    "description": "A physical description of the character",
                },
                "backstory": {
                    "type": "string",
                    "description": "The character's backstory",
                },
                "goal": {
                    "type": "string",
                    "description": "The character's goal",
                },
                "occupation": {
                    "type": "string",
                    "description": "The character's daily occupation",
                },
                "inventory": {
                    "type": "array",
                    "description": "The character's inventory of items",
                    "items": {"type": "string"},
                },
                "str": {
                    "type": "number",
                    "description": "The amount of Strength the character has from 1-20",
                },
                "dex": {
                    "type": "integer",
                    "description": "The amount of Dexterity the character has from 1-20",
                },
                "con": {
                    "type": "integer",
                    "description": "The amount of Constitution the character has from 1-20",
                },
                "int": {
                    "type": "integer",
                    "description": "The amount of Intelligence the character has from 1-20",
                },
                "wis": {
                    "type": "integer",
                    "description": "The amount of Wisdom the character has from 1-20",
                },
                "cha": {
                    "type": "integer",
                    "description": "The amount of Charisma the character has from 1-20",
                },
            },
        },
    }

    @property
    def chat_summary(self):
        return self.chats["summary"]

    def chat(self, message):
        # summarize conversation
        primer = f"""As an expert AI in {self.world.genre} TTRPG Worldbuilding as well, use the previous chat CONTEXT as a starting point to generate a readable summary from the PLAYER MESSAGE and NPC RESPONSE that clarifies the main points of the conversation. Avoid unnecessary details. 
        """
        text = f"""
        CONTEXT:\n{self.chats["summary"]}
        PLAYER MESSAGE:\n{self.chats['message']}
        NPC RESPONSE:\n{self.chats['response']}"
        """

        self.chats["summary"] = OpenAI().summarize_text(text, primer=primer)

        primer = "You are playing the role of an TTRPG NPC talking to a PC."
        prompt = "As an NPC matching the following description:"
        prompt += f"""
            PERSONALITY: {", ".join(self.traits)}

            DESCRIPTION: {self.desc}

            BACKSTORY: {self.backstory_summary}

            GOAL: {self.goal}

        Respond to the PLAYER MESSAGE as the above described character. Use the following chat CONTEXT as a starting point:

        CONTEXT: {self.chats["summary"]}

        PLAYER MESSAGE: {message}
        """

        response = OpenAI().generate_text(prompt, primer)
        self.chats["history"].append((message, response))
        self.chats["message"] = message
        self.chats["response"] = response
        self.save()

        return self.chats

    @classmethod
    def generate(cls, world, description=None):
        age = random.randint(15, 45)
        gender = random.choices(cls.genders, weights=[4, 5, 1], k=1)[0]
        primer = primer = f"""
        As an expert AI in fictional {world.genre} worldbuilding, you generate characters appropriate to the genre with a name and full details.
        """
        traits = ", ".join(
            [random.choice(traits) for traits in cls.personality.values()]
        )
        prompt = f"As an expert AI in creating NPCs for a {world.genre} TTRPG. Generate a {gender} NPC aged {age} years with the following personality traits: {traits}. Write a detailed backstory for the NPC containing an unusual, wonderful, OR sinister secret that gives the character a goal to work toward"
        if description:
            prompt += (
                f" by incorporating the following into the backstory: {description}."
            )

        obj_data = super().generate(primer, prompt)

        obj_data |= {"world": world, "traits": traits}
        obj = cls(**obj_data)
        obj.save()
        return obj

    def get_image_prompt(self):
        style = ["Italian Renaissance", "John Singer Sargent", "James Tissot"]
        return f"A full color portrait in the style of {random.choice(style)} of a fictional {self.gender} {self.race} {self.genre} character aged {self.age} and described as {self.desc}."
