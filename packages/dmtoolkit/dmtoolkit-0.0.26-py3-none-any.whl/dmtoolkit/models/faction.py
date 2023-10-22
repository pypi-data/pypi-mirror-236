import json
import random

from autonomous import log
from autonomous.ai import OpenAI

from dmtoolkit.models.ttrpgobject import TTRPGObject

from .character import Character


class Faction(TTRPGObject):
    attributes = TTRPGObject.attributes | {
        # character traits
        "goal": "",
        "status": "",
        "leader": None,
        "members": [],
    }
    personality = [
        "greedy",
        "generous",
        "lazy",
        "hardworking",
        "courageous",
        "cowardly",
        "creative",
        "imaginative",
        "practical",
        "rational",
        "curious",
        "nosy",
        "violent",
        "cautious",
        "careful",
        "reckless",
        "careless",
    ]

    funcobj = {
        "name": "generate_faction",
        "description": "completes Faction data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The faction's name",
                },
                "traits": {
                    "type": "array",
                    "description": "The faction's personality",
                    "items": {"type": "string"},
                },
                "desc": {
                    "type": "string",
                    "description": "A description of the members of the faction",
                },
                "backstory": {
                    "type": "string",
                    "description": "The faction's backstory",
                },
                "goal": {
                    "type": "string",
                    "description": "The faction's goal",
                },
                "status": {
                    "type": "string",
                    "description": "The faction's current status",
                },
            },
        },
    }

    @classmethod
    def generate(cls, world, description=None):
        primer = f"""
        You are an expert {world.genre} TTRPG Worldbuilding AI that generates interesting random factions and organizations for a TTRPG."
        """
        traits = ", ".join([random.choice(cls.personality) for _ in range(2)])
        prompt = f"Generate a {world.genre} faction for a TTRPG in a location described as follows: {traits}\n{description}.  The faction needs a backstory containing an unusual, wonderful, OR sinister secret that gives the Faction a goal they are working toward."
        obj_data = super().generate(primer, prompt)
        obj_data |= {"world": world, "traits": traits}
        obj = cls(**obj_data)
        obj.save()
        return obj

    def get_image_prompt(self):
        return f"A full color logo or banner for a fictional faction named {self.name} and described as {self.desc}."

    def add_member(self, character=None, leader=False):
        description = ""
        if leader:
            description = (
                f"The leader of the {self.name} faction whose goal is: {self.goal}."
            )
        if not character:
            character = Character.generate(self.world, description)
            character.save()

        if character not in self.members:
            self.members.append(character)

        if leader:
            self.leader = character

        self.save()
        return character
