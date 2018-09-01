from django.core import serializers

def dump(query_set):
    return serializers.serialize("json", query_set)