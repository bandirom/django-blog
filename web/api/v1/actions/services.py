from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from actions.choices import LikeObjChoice, LikeStatus
from blog.models import Article, Comment

from main.models import UserType

User: UserType = get_user_model()


class LikeService:
    def __init__(self, user: User, vote: LikeStatus, model: LikeObjChoice, object_id: int):
        self.user = user
        self.vote = vote
        self.model = model
        self.object_id = object_id
        self.instance = self.model_instance()

    def get_content_type_for_model(self) -> ContentType:
        return ContentType.objects.get_for_model(self.model_instance())

    def get_article(self) -> Article:
        return Article.objects.get(id=self.object_id)

    def get_comment(self) -> Comment:
        return Comment.objects.get(id=self.object_id)

    def model_instance(self) -> Article | Comment:
        obj = None
        match self.model:
            case LikeObjChoice.ARTICLE:
                obj = self.get_article()
            case LikeObjChoice.COMMENT:
                obj = self.get_comment()
        return obj
