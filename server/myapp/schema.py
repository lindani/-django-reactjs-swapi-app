import graphene
import requests


class Person(graphene.ObjectType):
    name = graphene.String()
    height = graphene.String()
    mass = graphene.String()
    gender = graphene.String()
    homeworld = graphene.String()


class Query(graphene.ObjectType):
    all_people = graphene.List(Person)

    def resolve_all_people(self, info):
        response = requests.get('https://swapi.dev/api/people/')
        data = response.json()
        people = data['results']
        return [Person(name=person['name'], height=person['height'], mass=person['mass'], gender=person['gender'], homeworld=person['homeworld']) for person in people]


schema = graphene.Schema(query=Query)
