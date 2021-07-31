"""This module contains the REST interface of this service"""
from sanic import Sanic
from sanic.response import json

from git_uploader import GitStatitisicsUploader

app = Sanic(__name__)
git_uploader = GitStatitisicsUploader()


@app.route("/upload/<git_user>", methods=["GET"])
async def upload(request, git_user):
    resp = await git_uploader.upload_user(git_user)
    return json(resp.to_json())


@app.route("/health", methods=["GET"])
async def health(request):
    resp = await git_uploader.get_health()
    return json(resp.to_json())
