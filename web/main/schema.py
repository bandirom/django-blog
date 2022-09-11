import graphene

from api.v1.profile.schema import UserMutation
from blog.schema import CategoryMutation, CategoryQuery, PaginationCategoryQuery


class Query(CategoryQuery, PaginationCategoryQuery, graphene.ObjectType):
    pass


class Mutation(CategoryMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
