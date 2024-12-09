from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        user = get_user_model().objects.create(email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class CitySerializer(serializers.ModelSerializer):
    my_state__name = serializers.ReadOnlyField(source='state.name')
    state_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), required=True)
    class Meta:
        model = City
        fields = ["id", "name", "city_code", "population", "avg_age", "num_of_adult_males", "num_of_adult_females", "my_state__name", "state_id"]

    def create(self, validated_data):
        validated_data['state_id'] = validated_data['state_id'].id
        city = City.objects.create(**validated_data)
        return city


class StateSerializer(serializers.ModelSerializer):
    my_country__name = serializers.ReadOnlyField(source='country.name')
    my_country__my_user__name = serializers.ReadOnlyField(source='country.my_user.name')
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True)
    cities = CitySerializer(many=True, required=False)

    class Meta:
        model = State
        fields = ["id", "name", "state_code", "phone_code", "gst_code", "cities", "my_country__my_user__name", "my_country__name", "country_id"]

    def validate_states(self, cities):
        city_names = set()
        city_codes = set()
        for city_data in cities:
            city_name = city_data.get('name')
            city_code = city_data.get("city_code")   
            if city_name in city_names:
                raise serializers.ValidationError(f"Duplicate city name '{city_name}'")
            city_names.add(city_name)
            if city_code in city_codes:
                raise serializers.ValidationError(f"Duplicate city code '{city_code}'")
            city_codes.add(city_code)
        return cities

    def create(self, validated_data):
        cities_data = list(map(lambda v: City(**v), validated_data.pop('cities', [])))
        validated_data['country_id'] = validated_data['country_id'].id
        state = State.objects.create(**validated_data)
        City.objects.bulk_create(cities_data)
        return state
    

    def update(self, instance, validated_data):
        City.objects.filter(my_state__name=instance.name).delete()

        instance.country = validated_data.get('country', instance.country)
        instance.name = validated_data.get('name', instance.name)
        instance.state_code = validated_data.get('state_code', instance.state_code)
        instance.phone_code = validated_data.get('phone_code', instance.phone_code)
        instance.gst_code = validated_data.get('phone_code', instance.gst_code)
        instance.save()
        
        cities_data = list(map(lambda v: City(**v), validated_data.pop('cities', [])))
        State.objects.create(**validated_data)
        City.objects.bulk_create(cities_data)

        return instance

class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, required=False)


    class Meta:
        model = Country
        fields = ["id", "name", "country_code", "phone_code", "my_user", "states"]

    def validate_states(self, states):
        state_names = set()
        for state_data in states:
            state_name = state_data.get('name')
            if state_name in state_names:
                raise serializers.ValidationError(f"Duplicate state name '{state_name}'")
            state_names.add(state_name)
        return states
    

    def create(self, validated_data):
        states_data = list(map(lambda v: State(**v), validated_data.pop('states', [])))
        cities_data = []

        for state in states_data:
            cities_data.append(City(**state.pop('cities')))

        country = Country.objects.create(**validated_data)
        State.objects.bulk_create(states_data)
        City.objects.bulk_create(cities_data)
        return country

    def update(self, instance, validated_data):

        City.objects.filter(my_state__name=instance.name).delete()
        State.objects.filter(my_country__name=instance.name).delete()

        instance.name = validated_data.get('name', instance.name)
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.phone_code = validated_data.get('phone_code', instance.phone_code)
        instance.my_user = validated_data.get('my_user', instance.my_user)
        instance.save()
        
        states_data = list(map(lambda v: State(**v), validated_data.pop('states', [])))
        cities_data = []

        for state in states_data:
            cities_data.append(City(**state.pop('cities')))

        Country.objects.create(**validated_data)
        State.objects.bulk_create(states_data)
        City.objects.bulk_create(cities_data)

        return instance
