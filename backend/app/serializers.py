from rest_framework import serializers

from app.models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = (
            'id',
            'published_at',
            'modified_at',
        )
