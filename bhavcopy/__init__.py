import cherrypy
import os

from bhavcopy import controller

if __name__ == '__main__':

    res_path = os.path.join(os.path.dirname(__file__), 'res/')

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': res_path
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }

    cherrypy.quickstart(controller.BhavController(), '/', conf)
