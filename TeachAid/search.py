from tests.keyword_test import DEVELOPER_KEY
from flask import (
    current_app, Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login.utils import login_required
from TeachAid.models import Course, Module
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

bp = Blueprint('search', __name__)

DEVELOPER_KEY = current_app.config['GOOGLE_YOUTUBE_API_KEY']

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'   

def youtube_search(keyword):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=keyword,
        part='id,snippet',
        maxResults=30,
        safeSearch='strict',
        topicId='/m/01k8wb',
        relevanceLanguage='EN'
    ).execute()

    youtube_recommendations = []
    urlvideo='https://www.youtube.com/watch?v='
    urlplaylist='https://www.youtube.com/playlist?list='
    urlchannel='https://www.youtube.com/channel/'
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        youtubeitem={}
        if search_result['id']['kind'] == 'youtube#video':
            youtubeitem['url']=urlvideo+search_result['id']['videoId']
        elif search_result['id']['kind'] == 'youtube#channel':
            youtubeitem['url']=urlchannel+search_result['snippet']['channelId']            
        elif search_result['id']['kind'] == 'youtube#playlist':
            youtubeitem['url']=urlplaylist+search_result['id']['playlistId']
        youtubeitem['title']=search_result['snippet']['title']
        youtubeitem['description']=search_result['snippet']['description']
        youtubeitem['channelTitle']=search_result['channelTitle']
        youtubeitem['imageURL']=search_result['snippet']['thumbnail']['medium']
        print(youtubeitem)
        youtube_recommendations.append(youtubeitem)
    return youtube_recommendations

@bp.route('/searchweb')
def search_web():
    return render_template('search/search.html')

bp.route('/<int:id>/getresults',methods=('GET','POST'))
@login_required
def get_recommendations(id):
    module=Module.query.filter_by(id=id).first()
    course=Course.query.filter_by(id=module.course_id).first()
    keyword=module.module_name+' '+course.title
    youtube_recommendations=youtube_search(keyword)
    if not youtube_recommendations:
        flash('Results not found')
        return redirect(url_for('index'))
    return render_template('search/moduleresults.html', youtube_recommendations=youtube_recommendations, module=module) 
