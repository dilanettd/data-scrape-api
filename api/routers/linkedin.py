import json
from apifairy import response
from flask import Blueprint
from api.schemas.linkedin import PostSchema
from api.services.linkedin import get_linkedin_activity_data


linkedin = Blueprint("linkedin", __name__)


@response(PostSchema)
@linkedin.route("/activity/<linkedin_user_id>", methods=["GET"])
def get_activity(linkedin_user_id):
    """
    Scrape recent activity (latest 20-30 posts) of a LinkedIn user by their
    LinkedIn ID and fetch the engagement data (likers) of each post,
    including their IDs, names, and titles.
    """

    data = get_linkedin_activity_data(linkedin_user_id)
    return json.dumps(data, indent=4)
