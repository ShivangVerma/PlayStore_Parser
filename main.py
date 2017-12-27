import urllib
from bs4 import BeautifulSoup
import urllib2
import webapp2

import jinja2
import os
import webapp2
import logging


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


def parse(link):
    text = urllib2.urlopen(link).read()
    soup = BeautifulSoup(text, 'html.parser')
    titles = soup.find_all("a", class_="title")
    data = {}
    for title in titles:
        data[title.get_text()] = {}

    for title in titles:
        data[title.get_text()]["Title"] = title['title']
        test = title.get_text().split('.')[0]
        data[title.get_text()]["Rank"] = int(test.split(' ')[1])
        data[title.get_text()]["id"] = title['href'].split('?id=')[1]

        image = soup.find("img", alt=title['title'])['src']

        if image[0:2] == 'ht':
            data[title.get_text()]["Image"] = image

        else:
            data[title.get_text()]["Image"] = 'https:' + image

    subtitles = soup.find_all("a", class_="subtitle")
    details = soup.find_all("div", class_="details")
    for detail in details:
        te = detail.find_all('a')
        data[te[1].get_text()]["SubTitle"] = te[2].get_text()

    l = data.keys()
    l.sort()
    new_dict = {}

    for item in l:
        new_dict[data[item]['id']] = data[item]

    data = new_dict
    return data


class Handler(webapp2.RequestHandler):

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class Data_New(db.Model):
    Title = db.StringProperty()
    Developer = db.StringProperty()
    Image = db.StringProperty()
    Rank = db.IntegerProperty()
    id_ = db.StringProperty()


class MainPage(Handler):
    Country = {'Albania': 'al', 'Algeria': 'dz', 'Angola': 'ao', 'Antigua': 'ag', 'Argentina': 'ar', 'Armenia': 'am',
               'Aruba': 'aw', 'Australia': 'au', 'Austria': 'at', 'Azerbaijan': 'az', 'Bahamas': 'bs', 'Bahrain': 'bh',
               'Bangladesh': 'bd', 'Belarus': 'by', 'Belgium': 'be', 'Belize': 'bz', 'Benin': 'bj', 'Bolivia': 'bo',
               'Bosnia': 'ba', 'Botswana': 'bw', 'Brazil': 'br', 'Bulgaria': 'bg', 'Burkina': 'bf', 'Cambodia': 'kh',
               'Cameroon': 'cm', 'Canada': 'ca', 'Cape': 'cv', 'Chile': 'cl', 'Colombia': 'co', 'Costa': 'cr',
               'Cote': 'ci', 'Croatia': 'hr', 'Cyprus': 'cy', 'Czech': 'cz', 'Denmark': 'dk', 'Dominican': 'do',
               'Ecuador': 'ec', 'Egypt': 'eg', 'El': 'sv', 'Estonia': 'ee', 'Fiji': 'fj', 'Finland': 'fi',
               'France': 'fr', 'Gabon': 'ga', 'Germany': 'de', 'Ghana': 'gh', 'Greece': 'gr', 'Guatemala': 'gt',
               'Guinea-Bissau': 'gw', 'Haiti': 'ht', 'Honduras': 'hn', 'Hong': 'hk', 'Hungary': 'hu', 'Iceland': 'is',
               'India': 'in', 'Indonesia': 'id', 'Ireland': 'ie', 'Israel': 'il', 'Italy': 'it', 'Jamaica': 'jm',
               'Japan': 'jp', 'Jordan': 'jo', 'Kazakhstan': 'kz', 'Kenya': 'ke', 'Kuwait': 'kw', 'Kyrgyzstan': 'kg',
               'Laos': 'la', 'Latvia': 'lv', 'Lebanon': 'lb', 'Liechtenstein': 'li', 'Lithuania': 'lt',
               'Luxembourg': 'lu', 'Macedonia': 'mk', 'Malaysia': 'my', 'Mali': 'ml', 'Malta': 'mt', 'Mauritius': 'mu',
               'Mexico': 'mx', 'Moldova': 'md', 'Morocco': 'ma', 'Mozambique': 'mz', 'Namibia': 'na', 'Nepal': 'np',
               'Netherlands': 'an', 'New': 'nz', 'Nicaragua': 'ni', 'Niger': 'ne', 'Nigeria': 'ng', 'Norway': 'no',
               'Oman': 'om', 'Pakistan': 'pk', 'Panama': 'pa', 'Papua': 'pg', 'Paraguay': 'py', 'Peru': 'pe',
               'Philippines': 'ph', 'Poland': 'pl', 'Portugal': 'pt', 'Qatar': 'qa', 'Romania': 'ro', 'Russia': 'ru',
               'Rwanda': 'rw', 'Saudi': 'sa', 'Senegal': 'sn', 'Serbia': 'rs', 'Singapore': 'sg', 'Slovakia': 'sk',
               'Slovenia': 'si', 'South': 'kr', 'Spain': 'es', 'Sri': 'lk', 'Sweden': 'se', 'Switzerland': 'ch',
               'Taiwan': 'tw', 'Tajikistan': 'tj', 'Tanzania': 'tz', 'Thailand': 'th', 'Togo': 'tg', 'USA': 'us'}
    URL_dict = {'Top Free in Android Apps': 'https://play.google.com/store/apps/collection/topselling_free',
                'Top Paid in Android Apps': 'https://play.google.com/store/apps/collection/topselling_paid',
                'Top Grossing Android Apps': 'https://play.google.com/store/apps/collection/topgrossing',
                'Top Free in Games': 'https://play.google.com/store/apps/category/GAME/collection/topselling_free',
                'Top Grossing Games': 'https://play.google.com/store/apps/category/GAME/collection/topselling_paid'
                }

    def write_form_out(self, _id_="", Title="", Developer="", Rank="", Image=""):
        self.render("sample.html", _id_=_id_, Title=Title, Developer=Developer, Rank=Rank, Image=Image)

    def write_form(self, Category="", Country=""):
        self.render("test.html", Category=Category, Country=Country)

    def get(self):
		self.write_form()

    def post(self):

        URL_key = self.request.get('URL_key')
        country = self.request.get('Country')
        country_code = self.Country[country]

        num = 99

        start1 = self.request.get('start')
        if start1:
            pass
        else:
            start1 = 0

        start = int(start1)
        self.response.out.write(
            '<span style="font-size:30px">Location: %s </span><span style="font-size:30px; margin-left:280px">Category: %s</span><br><br><br>' % (
            country, URL_key))

        while start < 200:

            args = {'gl': country_code, 'num': num, 'start': start}
            URL = self.URL_dict[URL_key] + "?" + urllib.urlencode(args)
            data = parse(URL)

            l = sorted(data, key=lambda x: (data[x]['Rank']))

            for item in l:
                Title = data[item]["Title"]
                Developer = data[item]["SubTitle"]
                Image = data[item]["Image"]
                Rank = data[item]["Rank"]
                id_ = data[item]["id"]
                # Data_entity = Data_New(Title = Title, Developer = Developer, Image = Image, Rank = Rank, id_ = id_)
                # Data_entity.put()
                _id_ = "https://play.google.com/store/apps/details?id=" + str(id_)
                self.write_form_out(_id_=_id_, Title=Title, Developer=Developer, Rank=Rank, Image=Image)

            if start == 199:
                break;

            start = start + 99
            if start > 199:
                start = 199
                num = 120


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

