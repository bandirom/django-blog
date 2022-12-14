import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

User = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class CreateUserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    password_2 = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = CreateUserInput(required=True)

    user = graphene.Field(UserNode)

    @staticmethod
    def mutate(root, info, user_data: CreateUserInput):
        print(f'{user_data=}')
        return None


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
