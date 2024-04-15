from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from django.core.files.uploadedfile import InMemoryUploadedFile

    from blog.models import Category


class CreateArticleT(TypedDict):
    category: "Category"
    title: str
    content: str
    image: "InMemoryUploadedFile"
    tags: list[str]
