from flask import request, redirect, make_response
from flask import Blueprint, render_template
from orangepages.models.models import db, User, Group, Post, Comment, Tag
from orangepages.views.util import cur_user, cur_uid, render

def add_tag(uid1, tagStr):
    user1 = User.query.get(uid1)
    post1 = Post("test post", user1, [])
    tag = Tag(tagStr)
    post1.add_tag(tag)
    
    tags = post1.get_tags()
    print(tags)

def search_tag(tagStr):
    tag = Tag.query.get(tagStr)
    posts = tag.get_posts()
    print(posts)
