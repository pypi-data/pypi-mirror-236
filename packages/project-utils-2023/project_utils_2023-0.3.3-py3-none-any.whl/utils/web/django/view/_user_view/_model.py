from abc import ABCMeta

from django.contrib.auth.models import AbstractUser

from utils.web.django.model import BaseModel, BaseMeta


class BaseUserModel(AbstractUser, BaseModel):
    class Meta(BaseMeta):
        abstract = True
