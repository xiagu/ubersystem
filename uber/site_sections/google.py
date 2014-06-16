from uber.common import *
import subprocess

# TODO: move Gam to it's own file (probably).  or also integrate it with normal
# models.py stuff from cherrypy

class Gam:
    def __init__(self):
        # TODO: move these to main config
        self.gam_python = "python2.7"
        self.gam_path = "/home/dom/google/gam/gam.py"

    def run(self, args):
        real_args = [self.gam_python, self.gam_path]
        real_args.extend(args)
        return subprocess.check_output(real_args)

    def get_listnames(self):
        output = self.run(["print", "groups"])
        lists = output.splitlines()[1:]
        return lists


# TODO: wrong access permission level. testing only.
@all_renderable(PEOPLE)
class Root:
   
    def index(self):
        return '<a href="mailing_lists">go here</a>'

    def mailing_lists(self):
        gam = Gam()
        lists = gam.get_listnames();
        return { "lists": lists }
