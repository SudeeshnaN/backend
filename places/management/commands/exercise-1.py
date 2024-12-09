from ....places.models import *
from typing import Dict,List, Tuple


data=[{"name": "india", "country_code": "IN", "phone_code": "91"},
      {"name": "USA", "country_code": "US", "phone_code": "1"},
      {"name": "United Kingdom", "country_code": "UK", "phone_code": "34"},]


# insert single entry
for i in data:
    country = Country.objects.create(name=i['name'], country_code=i['country_code'], phone_code=i['phone_code'])


# insert bulk entries
countries=[]
for i in data:
    countries.append(Country(name=i['name'], country_code=i['country_code'], phone_code=i['phone_code']))
Country.objects.bulk_create(countries)

# fetch all countries, cities, state
Country.objects.all()
State.objects.all()
City.objects.all()

# fetch all cities of a state
state='telangana'
City.objects.filter(state__name=state)

# fetch all states of country
country='india'
states_cou = State.objects.filter(country__name=country)

# fetch all cities of a country
City.objects.filter(state__in= states_cou)


# fetch a city with min and max population
max_city = City.objects.filter(state__country__name=country).order_by('population').first()
min_city = City.objects.filter(state__country__name=country).order_by('-population').first()



# fetch all countries and order by population
countries = Country.objects.all()
states = State.objects.all()
City.objects.annotate()



# Type hint
def greet(name: str) -> str:
    return f"Hello, {name}!"

def calculate_sum(numbers: List[int]) -> int:
    return sum(numbers)

def nums() -> Tuple[float, float]:
    return 3.1,3.6

class MyDict:
    def __init__(self, dict: Dict[str,int]):
        self.dict = dict

my_dict = MyDict({"a": 1, "b": 2})
print(my_dict.data)