import graphene

from blog.schema import CategoryQuery, CategoryMutation, PaginationCategoryQuery


class Query(
    CategoryQuery,
    PaginationCategoryQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    CategoryMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, )
