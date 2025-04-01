from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Navigation, UserNote, UserSettings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class NavigationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    # 在创建时这些字段是必需的，但在更新时不是
    title = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    icon = serializers.CharField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Navigation
        fields = '__all__'
        
    def create(self, validated_data):
        # 创建时确保必要字段存在
        for field in ['title', 'url', 'icon', 'category']:
            if field not in validated_data:
                raise serializers.ValidationError({field: ["该字段是必填项。"]})
        return super().create(validated_data)

class UserNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNote
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 