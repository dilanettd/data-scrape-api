from .. import ma


class LikerSchema(ma.Schema):
    id = ma.Str(required=True)
    name = ma.Str(required=True)
    title = ma.Str(required=True)


class PostSchema(ma.Schema):

    post_id = ma.Str(required=True)
    likers = ma.List(ma.Nested(LikerSchema), required=True)
