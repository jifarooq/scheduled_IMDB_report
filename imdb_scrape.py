import requests
import bs4

# run scrape --> Main function
def imdb_scrape():
  content = ''
  url     = 'http://www.imdb.com/movies-in-theaters/'
  movies  = scrape_movies(url)
  movies.sort(key = lambda m: m.score, reverse = True)
  for m in movies:
    content += m.get_content()
  content += "<br>more info <a href=" + url + ">here</a><br>";
  send_simple_message(content)

# movie class
class Movie(object):
  def __init__(self, title, plot, score, director, cast):
    self.title    = title
    self.plot     = plot
    self.score    = score
    self.director = director
    self.cast     = cast

  def get_content(self):
    content  = "<b>{}</b> (Metascore: {}) - {}<br>".format(self.title, self.score, self.plot)
    content += "<em>Director</em>: {}<br>"  .format(self.director.encode('utf-8'))
    content += "<em>Actors</em>: {}<br><br>".format(self.cast.encode('utf-8'))
    return content


# all other functions
def get_director(td):
  return td.find('span', { "itemprop": "director" }).text.replace("\n", "")

def get_cast(td):
  cast_list = td.find_all('span', { "itemprop": "actors" })
  for i, actor in enumerate(cast_list):
    cast_list[i] = actor.text.replace("\n", "")
  return (", ").join(cast_list)

def scrape_movies(url):
  movies    = []
  html      = requests.get(url).text
  soup      = bs4.BeautifulSoup(html, "html.parser")
  movie_tds = soup.find_all(class_="overview-top")

  for td in movie_tds:
    title = td.find('a')['title'].upper()
    plot  = td.find(class_="outline").text.replace("\n", "")
    score = td.find('strong')
    score = int(score.text) if score else None
    movie = Movie(title, plot, score, get_director(td), get_cast(td))
    movies.append(movie)

  return movies   


# ---fire email---- 
def send_simple_message(body):
  sandbox_id = "INSERT_MAILGUN_SANDBOX_ID"
  api_url    = "https://api.mailgun.net/v3/sandbox" + sandbox_id + ".mailgun.org/messages"
  api_key    = "key-INSERT_MAILGUN_API_KEY"

  return requests.post(
    api_url,
    auth=("api", api_key),
    data={"from"   : "mailgun me <postmaster@sandbox" + sandbox_id + ".mailgun.org>",
          "to"     : "Justin <justinfarooq@gmail.com>",
          "subject": "Movie releases this week",
          "html"   : body })

imdb_scrape()