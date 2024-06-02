from .. import ma


class LikerSchema(ma.Schema):
    """
    Schema for the Liker model.
    """

    id = ma.Str(required=True)  # ID of the liker
    name = ma.Str(required=True)  # Name of the liker
    title = ma.Str(required=True)  # Title of the liker


class PostSchema(ma.Schema):
    """
    Schema for the Post model.
    """

    post_id = ma.Str(required=True)  # ID of the post
    likers = ma.List(
        ma.Nested(LikerSchema), required=True
    )  # List of likers associated with the post
