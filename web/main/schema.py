import graphene

from blog.schema import CategoryQuery, CategoryMutation


class Query(
    CategoryQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    CategoryMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
