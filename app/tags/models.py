from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=255)


"""
Since we another app,to import models from store it would be clumsy
to follow concept of decoupling use Generic way yo identify object 
using TYPE (table in db) and ID (record in table)
# Type (product,video,article) 
# ID ()
import ContentType frm django contrib
"""


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
