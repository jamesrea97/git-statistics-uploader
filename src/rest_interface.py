"""This module contains the REST interface of this service"""
from sanic import Sanic
from sanic.response import json

from git_service import GitStatitisicsUploader
app = Sanic(__name__)


@app.route("/stats/<git_user>")
async def stats(request, git_user):
    git_uploader = GitStatitisicsUploader()

    git_uploader.get_statistics(git_user)
    return json({"response": f"Hello {git_user}"})


@app.route("/health")
async def stats(request):
    pass


app.run()
