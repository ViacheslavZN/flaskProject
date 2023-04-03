from combojsonapi.utils import Relationship
from marshmallow_jsonapi import Schema, fields
from flask_combo_jsonapi import ResourceDetail, ResourceList
from blog.schemas import ArticleSchema
from blog.models.database import db
from blog.models import Article



class ArticleSchema(Schema):
    class Meta:
        type_ = "article"
        self_view = "article_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "article_list"

    id = fields.Integer(as_string=True)
    title = fields.String(allow_none=False)
    body = fields.String(allow_none=False)
    dt_created = fields.DateTime(allow_none=False)
    dt_updated = fields.DateTime(allow_none=False)

    author = Relationship(
        nested="AuthorSchema",
        attribute="author",
        related_view="author_detail",
        related_view_kwargs={"id": "<id>"},
        schema="AuthorSchema",
        type_="author",
        many=False,
    )
    tags = Relationship(
        nested="TagSchema",
        attribute="tags",
        related_view="tag_detail",
        related_view_kwargs={"id": "<id>"},
        schema="TagSchema",
        type_="tag",
        many=True,
    )


class ArticleList(ResourceList):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }

class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }