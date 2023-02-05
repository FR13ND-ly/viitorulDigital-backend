from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import os
from django.contrib.auth.models import User
from .models import Article, Like, Comment, Profile
from rest_framework import status

@csrf_exempt
def login(request):
    data = JSONParser().parse(request)
    user, created = User.objects.get_or_create(
        first_name=data['displayName'],
        email=data['email']
    )
    if (created):
        user.username = data['uid']
        user.save()
    profile, created = Profile.objects.get_or_create(
        token = data['uid'],
        user = user
    )
    profile.save()
    response = {
        "isStaff" : user.is_staff,
    }
    return JsonResponse(response, status = status.HTTP_200_OK)

def getUserAuthorization(request, token):
    if not Profile.objects.filter(token = token).exists():
        return JsonResponse({}, status = status.HTTP_200_OK)    
    profile = Profile.objects.get(token = token)
    response = {
        "isStaff" : profile.user.is_staff,
    }
    return JsonResponse(response, status = status.HTTP_200_OK)


def getArticle(request, id):
    if (id == 'new'):
        return JsonResponse({
            "id": 'new',
            "title": '',
            "text": '',
            "subtitle": '',
            "imageUrl": ''
        }, safe=False)
    article = Article.objects.filter(id=id)
    if (not article.count()):
        return JsonResponse("404", safe=False)
    article = article[0]
    response = {
        "id": article.id,
        "title": article.title,
        "text": article.text,
        "subtitle": article.subtitle,
        "imageUrl": article.imageUrl
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
def getArticlesList(request):
    response = []
    articles = Article.objects.all()
    for article in articles:    
        response.append({
        "id": article.id,
        "title": article.title,
        "text": article.text,
        "subtitle": article.subtitle,
        "imageUrl": article.imageUrl
    })
    return JsonResponse(response, safe=False)

@csrf_exempt
def editArticle(request):
    data = JSONParser().parse(request)
    article = Article.objects.create() if data['id'] == 'nou' else Article.objects.get(id = data['id'])
    article.title = data['title']
    article.subtitle = data['subtitle']
    article.text = data['text']
    article.imageUrl = data['imageUrl']
    article.save()
    return JsonResponse("ok", safe=False)

@csrf_exempt
def getLikesInfo(request):
    data = JSONParser().parse(request)
    articleId = data['articleId']
    userToken = data['token']
    response = {
        'liked' : bool(Like.objects.filter(article = articleId, user = userToken).count()),
        'count' : Like.objects.filter(article = articleId).count()
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
def addLike(request):
    data = JSONParser().parse(request)
    like, created = Like.objects.get_or_create(article=data['articleId'], user=data['token'])
    if (created):
        like.save()
    else:
        like.delete()
    return JsonResponse("ok", safe=False)

def getComments(request, id):
    response = []
    for comment in Comment.objects.filter(article = id).order_by("-date"):
        response.append({
            "id" : comment.id,
            "author" : comment.author,
            "text" : comment.text,
            "imageUrl" : comment.imageURL,
        })
    return JsonResponse(response, safe=False)

@csrf_exempt
def addComment(request):
    data = JSONParser().parse(request)
    Comment.objects.create(
        author=data['author'],
        text=data['text'],
        article=data['articleId'],
        imageURL=data['imageUrl']
    ).save()
    response = []
    for comment in Comment.objects.filter(article = data['articleId']).order_by("-date"):
        response.append({
            "id" : comment.id,
            "author" : comment.author,
            "text" : comment.text,
            "imageURL" : comment.imageURL,
        })
    return JsonResponse(response, safe=False)
