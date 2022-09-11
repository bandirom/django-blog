import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from blog.models import Article, Category


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ('id', 'title', 'author')


class CategoryNode(DjangoObjectType):
    article_set = graphene.List(ArticleType)

    class Meta:
        model = Category
        filter_fields = {
            'name': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)
        fields = ('id', 'name', 'article_set')

    @staticmethod
    def resolve_article_set(root, info):
        return Article.objects.all()


class CategoryQuery(graphene.ObjectType):

    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)


class CategoryConnection(relay.Connection):
    class Meta:
        node = CategoryNode


class PaginationCategoryQuery:
    categories = relay.ConnectionField(CategoryConnection)

    @staticmethod
    def resolve_categories(root, info, **kwargs):  # first, last, before, after
        return Category.objects.all()


class CategoryInput(graphene.InputObjectType):
    # id = graphene.ID()
    name = graphene.String()


class CreateCategory(graphene.Mutation):
    class Arguments:
        category_data = CategoryInput(required=True)

    category = graphene.Field(CategoryNode)


    def clean(self, category_data):
        print(f'{category_data=}')

    @staticmethod
    def mutate(root, info, category_data: CategoryInput):
        print('mutate', category_data)
        category = Category.objects.create(name=category_data.name)
        return CreateCategory(category=category)


class CategoryMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()

# class CategoryQuery(graphene.ObjectType):
# category = graphene.Field(CategoryNode, id=graphene.Int(required=False), name=graphene.String())
# all_categories = graphene.List(CategoryType)
# @staticmethod
# def resolve_all_categories(root, info):
#     return Category.objects.prefetch_related('article_set').all()

# @staticmethod
# def resolve_category(root, info: ResolveInfo, id=None, name=None):
#     print(id, name)
#     try:
#         if name:
#             return Category.objects.get(name=name)
#         elif id:
#             return Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return None
