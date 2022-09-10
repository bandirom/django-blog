import graphene
from graphene_django import DjangoObjectType
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from blog.models import Category, Article


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ('id', 'title', 'author')


class CategoryNode(DjangoObjectType):
    article_set = graphene.List(ArticleType)

    class Meta:
        model = Category
        filter_fields = {
            'name': ['exact', 'icontains']
        }
        interfaces = (relay.Node,)
        fields = ('id', 'name', 'article_set')

    @staticmethod
    def resolve_article_set(root, info):
        return Article.objects.all()


class CategoryQuery(graphene.ObjectType):

    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)


class CategoryMutation(graphene.ObjectType):
    pass

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
