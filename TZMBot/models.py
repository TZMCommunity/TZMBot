# -*- coding: utf-8 -*-

"""Models for TZMBot."""
from tortoise import fields
from tortoise.models import Model


class Biography(Model):
    """Biography model.

    Defines the biography for the member of the discord server. id is autoincremented, person
    represents the member discord id and the content is whatever biography text they might have.
    """

    id = fields.IntField(pk=True)
    person = fields.CharField(unique=True, max_length=50)
    content = fields.TextField(null=True)

    def __str__(self) -> str:
        """A Biography model instance representation.

        Represents a biography through a string of the member id connected to it.

        :returns: A string of the discord member id.
        :rtype: str
        """
        return str(self.person)
