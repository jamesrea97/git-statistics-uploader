"""This module contains the REST interface of this service"""
from sanic import Sanic
from sanic.response import json

from git_uploader import GitStatitisicsUploader

app = Sanic(__name__)


@app.route("/stats/<git_user>")
async def stats(request, git_user):
    git_uploader = GitStatitisicsUploader()
    resp = await git_uploader.get_statistics(git_user)
    return json(resp.to_json())


@app.route("/health")
async def health(request):
    pass
