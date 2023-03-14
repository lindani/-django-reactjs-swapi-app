import graphene
import requests


class Character(graphene.ObjectType):
    name = graphene.String()
    height = graphene.String()
    mass = graphene.String()
    hair_color = graphene.String()
    skin_color = graphene.String()
    eye_color = graphene.String()
    birth_year = graphene.String()
    gender = graphene.String()
    homeworld = graphene.String()
    films = graphene.List(graphene.String)
    species = graphene.List(graphene.String)
    vehicles = graphene.List(graphene.String)
    starships = graphene.List(graphene.String)
    created = graphene.String()
    edited = graphene.String()
    url = graphene.String()


class CharactersPage(graphene.ObjectType):
    count = graphene.Int()
    next = graphene.String()
    previous = graphene.String()
    results = graphene.List(Character)


class Query(graphene.ObjectType):
    all_characters = graphene.List(Character)
    character = graphene.Field(Character, id=graphene.Int())
    characters_page = graphene.Field(CharactersPage, page=graphene.Int())

    def resolve_all_characters(self, info):
        response = requests.get('https://swapi.dev/api/people/')
        data = response.json()
        return [Character(name=person['name'], height=person['height'], mass=person['mass'],
                          gender=person['gender'], homeworld=person['homeworld']) for person in data['results']]

    def resolve_character(self, info, id):
        url = f'https://swapi.dev/api/people/{id}/'
        response = requests.get(url)
        data = response.json()
        return Character(**data)

    def resolve_characters_page(self, info, page):
        url = f'https://swapi.dev/api/people/?page={page}'
        response = requests.get(url)
        data = response.json()
        characters = [Character(**item) for item in data['results']]
        return CharactersPage(count=data['count'], next=data['next'], previous=data['previous'], results=characters)


schema = graphene.Schema(query=Query)
