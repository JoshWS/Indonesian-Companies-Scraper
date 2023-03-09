import hashlib

from mongoengine import Document, fields
from slugify import slugify


class company(Document):
    name = fields.StringField(required=True, max_length=255, min_length=3)

    def __repr__(self):
        return self.id

    def __str__(self):
        return f"Article id: {self.article_id}: {self.name} - {self.site_name}"

    @property
    def creation_stamp(self):
        return self.id.generation_time

    @classmethod
    def create_article_slug(cls, name):
        return slugify(name)

    @classmethod
    def create_hash_id(cls, news_source_name, name):
        id = f"{news_source_name.strip()}{name.strip()}".lower()
        print(id)
        return hashlib.md5(id.encode("utf-8")).hexdigest()
