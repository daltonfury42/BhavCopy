import cherrypy
import jinja2
from datetime import datetime

from bhavcopy import bse
from bhavcopy.dao import securityDAO


class BhavController(object):
    jinja = jinja2.Environment(
        loader=jinja2.PackageLoader('bhavcopy', 'res/templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )

    @cherrypy.expose
    def index(self, row_size=10, date_str=None):

        if date_str is None:
            date = datetime.today()
        else:
            date = datetime.strptime(date_str, '%d%m%y')

        date_text = date.strftime('%d, %B %Y')

        try:
            equities = securityDAO.SecurityDAO().get_equities() #ToDo change to date
        except securityDAO.RedisDataNotFoundException:
            raise cherrypy.HTTPError(message="Data not found in database")


        template = self.jinja.get_template('index.html')
        return template.render(equities=equities[:row_size], date=date_text)

    @cherrypy.expose
    def detail(self, name, row_size=10):

        try:
            equities = securityDAO.SecurityDAO().get_equities(name=name)
        except securityDAO.RedisDataNotFoundException:
            raise cherrypy.HTTPError(message="Data not found in database")  #ToDo handle in UI

        template = self.jinja.get_template('detail.html')
        return template.render(equities=equities[:row_size])

    @cherrypy.expose
    def update(self, date_str=None):

        if date_str is None:
            date = datetime.today()
        else:
            date = datetime.strptime(date_str, '%d%m%y')

        try:
            equities = bse.fetch_bhav(date)
        except bse.BhavNotFoundException:
            return "Bhav not found on BSE for " + date.strftime('%d-%m-%y') + ". Try with another date."

        dao = securityDAO.SecurityDAO()

        for equity in equities:
            dao.insert_equity(equity)

        return "OK."
