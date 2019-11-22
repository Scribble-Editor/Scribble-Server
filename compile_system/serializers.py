from compile_system.models import Scribblet
from rest_framework import serializers

class ScribbletSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Scribblet
    fields = ['url', 'username', 'scribbletId', 'name', 'target', 'language', 'content']
