import pprint

from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="REPLACE ME")

  res = service.cse().list(
      q='lectures',
      cx='54b0e5c669679dac6',
      start=11,
      fields='items(link,snippet,title, pagemap/cse_image)',
      safe='high'
    ).execute()
  google_recommendations=[]
  for search_result in res.get('items',[]):
    googleitem={}
    googleitem['url']=search_result['link']
    googleitem['title']=search_result['title']
    googleitem['description']=search_result['snippet']
    if 'pagemap' in search_result:
      googleitem['imageUrl']=search_result['pagemap']['cse_image'][0]['src']
    #print(googleitem)
    google_recommendations.append(googleitem)

  pprint.pprint(google_recommendations)
  #pprint.pprint(res)

if __name__ == '__main__':
  main()