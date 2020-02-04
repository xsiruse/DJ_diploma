import re
from .models import Category


def category(request, *args, **kwargs):
    return {"categories": Category.objects.all()}
