import graphene
import requests


class Person(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    height = graphene.String()
    mass = graphene.String()
    gender = graphene.String()
    homeworld = graphene.String()


class Query(graphene.ObjectType):
    all_people = graphene.List(Person)

    def resolve_all_people(self, info):
        response = requests.get('https://swapi.dev/api/people/')
        people = response.json()
        return [Person(id=person['id'],
                       name=person['name'],
                       height=person['height'],
                       mass=person['mass'],
                       gender=person['gender'],
                       homeworld=person['homeworld']) for person in people]


schema = graphene.Schema(query=Query)
