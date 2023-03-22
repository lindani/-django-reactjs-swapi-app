import uuid
import graphene
import requests
import jwt
from graphene_django.types import DjangoObjectType
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class Person(graphene.ObjectType):
    id = graphene.ID()
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

    def resolve_id(self, info):
        # Generate a dynamic ID for the Person
        return uuid.uuid4()


class PersonPage(graphene.ObjectType):
    count = graphene.Int()
    next = graphene.String()
    previous = graphene.String()
    results = graphene.List(Person)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(UserType)

    def mutate(self, info, email, username, password):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return RegisterUser(user=user)


class Token(graphene.ObjectType):
    token = graphene.String()


class Authenticate(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = Token

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception('Invalid username or password')
        token = jwt.encode({'username': user.username},
                           settings.SECRET_KEY, algorithm='HS256')
        return Token(token=token)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    authenticate = Authenticate.Field()


class Query(graphene.ObjectType):
    people = graphene.Field(
        PersonPage, page=graphene.Int(), search=graphene.String())
    # all_characters = graphene.List(Character, name=graphene.String())
    # character = graphene.Field(Character, id=graphene.Int())

    def resolve_people(self, info, page, search=None):

        url = f'https://swapi.dev/api/people/?page={page}'
        if search:
            url += f'&search={search}'
        response = requests.get(url)
        data = response.json()
        return PersonPage(count=data['count'], next=data['next'], previous=data['previous'], results=[Person(id=uuid.uuid4(), **person)
                                                                                                      for person in data['results']])

    # def resolve_all_characters(self, info, name=None):
    #     url = f'https://swapi.dev/api/people/?'
    #     if name:
    #         url += f'&search={name}'
    #     response = requests.get(url)
    #     data = response.json()
    #     characters = []
    #     for index, person in enumerate(data['results']):
    #         character = Character(id=index+1, name=person['name'], height=person['height'], mass=person['mass'],
    #                               gender=person['gender'], homeworld=person['homeworld'])
    #         characters.append(character)
    #     return characters

    # def resolve_character(self, info, id):
    #     url = f'https://swapi.dev/api/people/{id}/'
    #     response = requests.get(url)
    #     data = response.json()
    #     return Character(**data)


schema = graphene.Schema(query=Query, mutation=Mutation)
