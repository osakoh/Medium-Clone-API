from rest_framework import serializers

from .models import Tag

"""
.to_representation() and .to_internal_value() methods: used to convert between the initial datatype, and a primitive, 
serializable datatype. 
- Primitive datatypes will typically be any of a number, string, boolean, date/time/datetime or None. 
They may also be any list or dictionary like object that only contains other primitive objects. 
Other types might be supported, depending on the renderer that you are using.
"""


class TagRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        """
        Handles the data sent from outside to the model i.e. CREATE/POST

        called to restore a primitive datatype into its internal python representation.
        Method should raise a serializers.ValidationError if the data is invalid, that is, it's used to
        validate the update request for a serializer, for example, it will help to check if the request for updating the
        relatedField is present in the other table or not.
        """
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())
        return tag

    def to_representation(self, value):
        """
        Handles the data sent from model to outside world i.e. GET/LIST

        Used to convert the initial datatype into a primitive, serializable datatype
        Also, to modify the GET body for your API
        """
        return value.tag


"""
********************** In articles.TagRelatedField::to_internal_value ******************************
tag: query
created: True
********************** In articles.TagRelatedField::to_internal_value ******************************

********************** In articles.TagRelatedField::to_internal_value ******************************
tag: unchanging
created: True
********************** In articles.TagRelatedField::to_internal_value ******************************

********************** In articles.TagRelatedField::to_internal_value ******************************
tag: dict
created: True
********************** In articles.TagRelatedField::to_internal_value ******************************
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
********************** In articles.TagRelatedField::to_representation ******************************
value: dict
value.tag: dict
********************** In articles.TagRelatedField::to_representation ******************************

********************** In articles.TagRelatedField::to_representation ******************************
value: query
value.tag: query
********************** In articles.TagRelatedField::to_representation ******************************

********************** In articles.TagRelatedField::to_representation ******************************
value: unchanging
value.tag: unchanging
********************** In articles.TagRelatedField::to_representation ******************************

"""
