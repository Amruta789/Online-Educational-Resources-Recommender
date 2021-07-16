from flask import (
    current_app, Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login.utils import login_required
from TeachAid.models import Course, Module
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

bp = Blueprint('search', __name__)

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'   

def youtube_search(keyword, developer_key):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=developer_key)
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
    # Add each result to the appropriate list
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
        youtubeitem['channelTitle']=search_result['snippet']['channelTitle']
        youtubeitem['channelURL']=urlchannel+search_result['snippet']['channelId']
        youtubeitem['imageURL']=search_result['snippet']['thumbnails']['medium']
        print(youtubeitem)
        youtube_recommendations.append(youtubeitem)
    return youtube_recommendations

def google_search(keyword, startIndex, developer_key):
    service = build("customsearch", "v1",
            developerKey=DEVELOPER_KEY)
    search_response = service.cse().list(
        q=keyword,
        cx='54b0e5c669679dac6',
        start=startIndex,
        fields='items(link,snippet,title, pagemap/cse_image)',
        safe='high'
        ).execute()
    google_recommendations=[]
    for search_result in search_response.get('items',[]):
        googleitem={}
        googleitem['url']=search_result['link']
        googleitem['title']=search_result['title']
        googleitem['description']=search_result['snippet']
        if 'pagemap' in search_result:
            googleitem['imageUrl']=search_result['pagemap']['cse_image'][0]['src']
        print(googleitem)
        google_recommendations.append(googleitem)
    return google_recommendations

@bp.route('/searchweb')
def search_web():
    return render_template('search/search.html')

@bp.route('/<int:id>/getresults',methods=('GET','POST'))
@login_required
def get_recommendations(id):
    module=Module.query.filter_by(id=id).first()
    course=Course.query.filter_by(id=module.course_id).first()
    keyword=module.module_name+' '+course.title
    developer_key=current_app.config['GOOGLE_YOUTUBE_API_KEY']
    youtube_recommendations=youtube_search(keyword, developer_key)
    google_recommendations=google_search(keyword,1,developer_key)+google_search(keyword,11,developer_key)
    if not youtube_recommendations:
        flash('Youtube results not found')
        return redirect(url_for('index'))
    if not google_recommendations:
        flash('Google results not found')
        return redirect(url_for('index'))
    return render_template('search/moduleresults.html', google_recommendations=google_recommendations, youtube_recommendations=youtube_recommendations, module=module) 
