import json
import re

from autonomous import log
from autonomous.ai import OpenAI
from autonomous.storage.markdown import Page
from autonomous.model.automodel import AutoModel
from autonomous.storage.cloudinarystorage import CloudinaryStorage
from slugify import slugify


class TTRPGObject(AutoModel):
    _storage = CloudinaryStorage()
    _wiki_api = Page
    attributes = {
        "name": "",
        "_image": {"url": "", "asset_id": 0, "raw": None},
        "backstory": "",
        "_bs_summary": "",
        "desc": "",
        "dod": "",
        "dob": "",
        "traits": [],
        "world": None,
        "wiki_ids": {},
    }

    def __getattr__(self, key):
        if key == "genre" and self.world:
            return self.world.genre
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{key}'"
        )

    @property
    def story(self):
        return self.backstory

    @story.setter
    def story(self, value):
        self.backstory = value

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def backstory_summary(self):
        if not self._bs_summary:
            primer = "As an expert AI in fictional Worldbuilding fof TTRPGs, summarize the following backstory into a concise paragraph, creating a readable summary that could help a person understand the main points of the backstory. Avoid unnecessary details."

            self._bs_summary = OpenAI().summarize_text(self.backstory, primer=primer)
            self.save()
        return self._bs_summary

    def save(self):
        if self._image.get("raw"):
            self.image(update=True)
        return super().save()

    def image(self, url=None, update=False):
        if url:
            self._image["url"] = url

        if update or not self._image["url"]:
            if not self._image.get("raw"):
                resp = OpenAI().generate_image(
                    self.get_image_prompt(),
                    n=1,
                )
                # log(resp)
                self._image["raw"] = resp[0]

            if self.world:
                img_path = f"ttrpg/{self.world.slug}/{self.__class__.__name__.lower()}"
            else:
                img_path = f"ttrpg/{self.slug}/{self.__class__.__name__.lower()}"

            self._image = self._storage.save(
                self._image["raw"],
                folder=img_path,
                context={"caption": self.get_image_prompt()[:500]},
            )
        if self._image["url"]:
            self._image["raw"] = None
        return self._image["url"]

    def get_image_prompt(self):
        raise NotImplementedError

    @classmethod
    def generate(cls, prompt, primer):
        if hasattr(cls, "funcobj"):
            cls.funcobj["parameters"]["required"] = list(
                cls.funcobj["parameters"]["properties"].keys()
            )
            response = OpenAI().generate_text(prompt, primer, functions=cls.funcobj)
        else:
            response = OpenAI().generate_text(prompt, primer)

        json_invalid_count = 10
        json_valid = False
        while not json_valid:
            try:
                obj_data = json.loads(response, strict=False)
                json_valid = True
            except json.JSONDecodeError as e:
                response = response[: e.pos] + response[e.pos + 1 :]
                log(e, response)
                if json_invalid_count == 0:
                    if hasattr(cls, "funcobj"):
                        cls.funcobj["parameters"]["required"] = list(
                            cls.funcobj["parameters"]["properties"].keys()
                        )
                        response = OpenAI().generate_text(
                            prompt, primer, functions=cls.funcobj
                        )
                    else:
                        response = OpenAI().generate_text(prompt, primer)
                    json_invalid_count = 10
                else:
                    json_invalid_count -= 1
        return obj_data

    def canonize(self, api=None, path="ttrpg"):
        wrld = self.world.name if self.world else self.name
        config = {
            self.name: {
                "Meta": [f"Genre: {self.genre}", f"World: {wrld}"],
                "Details": self,
            }
        }
        model = self.__class__.__name__.lower()
        world = self.world.name.lower() if self.world else self.name.lower()
        if not api:
            api = self._wiki_api

        key = api.__class__.__name__.lower()
        if key not in self.wiki_ids:
            res = api.push(
                config,
                title=self.name,
                path=f"{path}/{model}/{self.slug}",
                description=self.desc[: self.desc.find(".") + 1],
                tags=[model, world, "ttrpg"],
            )
            self.wiki_ids[key] = res.id
            self.save()
        else:
            res = api.push(
                config,
                title=self.name,
                id=self.wiki_ids[key],
            )
        return res
