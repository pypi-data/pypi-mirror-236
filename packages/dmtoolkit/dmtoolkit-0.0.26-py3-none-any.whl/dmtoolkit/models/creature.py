import json
import random

from autonomous import log
from autonomous.ai import OpenAI

from dmtoolkit.models.ttrpgobject import TTRPGObject


class Creature(TTRPGObject):
    attributes = TTRPGObject.attributes | {
        "type": "",
        "size": "",
        "goal": "",
        "hit_points": 0,
        "abilities": [],
        "inventory": [],
        "str": 0,
        "dex": 0,
        "con": 0,
        "wis": 0,
        "int": 0,
        "cha": 0,
    }

    funcobj = {
        "name": "generate_creature",
        "description": "completes Creature data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The character's name",
                },
                "type": {
                    "type": "integer",
                    "description": "The type of creature",
                },
                "traits": {
                    "type": "array",
                    "description": "The unique features of the creature, if any",
                    "items": {"type": "string"},
                },
                "size": {
                    "type": "string",
                    "description": "huge, large, medium, small, or tiny",
                },
                "desc": {
                    "type": "string",
                    "description": "A physical description of the creature",
                },
                "backstory": {
                    "type": "string",
                    "description": "The creature's backstory",
                },
                "goal": {
                    "type": "string",
                    "description": "The creature's goal",
                },
                "hit_points": {
                    "type": "number",
                    "description": "Creature's hit points",
                },
                "abilities": {
                    "type": "array",
                    "description": "The creature's abilities in combat",
                    "items": {"type": "string"},
                },
                "inventory": {
                    "type": "array",
                    "description": "The creature's inventory of items",
                    "items": {"type": "string"},
                },
                "str": {
                    "type": "number",
                    "description": "The amount of Strength the creature has from 1-20",
                },
                "dex": {
                    "type": "integer",
                    "description": "The amount of Dexterity the creature has from 1-20",
                },
                "con": {
                    "type": "integer",
                    "description": "The amount of Constitution the creature has from 1-20",
                },
                "int": {
                    "type": "integer",
                    "description": "The amount of Intelligence the creature has from 1-20",
                },
                "wis": {
                    "type": "integer",
                    "description": "The amount of Wisdom the creature has from 1-20",
                },
                "cha": {
                    "type": "integer",
                    "description": "The amount of Charisma the creature has from 1-20",
                },
            },
        },
    }

    def get_image_prompt(self):
        description = self.desc or random.choice(
            [
                "A renaissance portrait",
                "An action movie poster",
                "Readying for battle",
            ]
        )
        style = random.choice(
            [
                "The Rusted Pixel style digital",
                "Albrecht Dürer style photorealistic colored pencil sketched",
                "William Blake style watercolor",
            ]
        )
        return f"A full color {style} portrait of a {self.name} type {self.world.genre} creature with the following description: {self.desc or description}"

    @classmethod
    def generate(cls, world, description="aggressive and hungry"):
        primer = f"""
        As an expert AI in fictional {world.genre} worldbuilding, you generate creatures appropriate to the genre with a name and description.
        """
        prompt = f"As an expert AI in creating enemies for a {world.genre} TTRPG, generate an creature with the following description:{description}. Write a detailed backstory for the creature containing an unusual, wonderful, OR sinister secret that gives the creature a goal to work toward."

        obj_data = super().generate(primer, prompt)

        obj_data["world"] = world
        obj = cls(**obj_data)
        obj.save()
        return obj
