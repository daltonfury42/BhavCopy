import cherrypy
import os

from bhavcopy import controller

if __name__ == '__main__':

    res_path = os.path.join(os.path.dirname(__file__), 'res/')

    cherrypy.quickstart(controller.BhavController(), '/', config="config")
