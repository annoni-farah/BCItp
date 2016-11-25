import os
from utils.standards import PATH_TO_SESSION

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty


class StartScreen(Screen):
    # layout
    session_name = ObjectProperty(None)
    label_msg = StringProperty('')

    def __init__(self, session_header, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.sh = session_header

    def change_to_gen_settings(self, *args):
        self.manager.current = 'GeneralSettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self, *args):

        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'left'

    def save_session_name(self, *args):

        sname = self.session_name.text

        if not os.path.isdir(PATH_TO_SESSION):
            os.makedirs(PATH_TO_SESSION)

        if sname == '':
            # if no session_name is provided, use latest modified folder in
            # data/session
            all_subdirs = []
            for d in os.listdir(PATH_TO_SESSION + '.'):
                bd = os.path.join(PATH_TO_SESSION, d)
                if os.path.isdir(bd):
                    all_subdirs.append(bd)
            sname = max(all_subdirs, key=os.path.getmtime).split('/')[-1]

        self.sh.info.name = sname

        if os.path.isdir(PATH_TO_SESSION + sname):

            self.label_msg = "Session " + sname \
                + " already exists. Data will be overwritten"
            self.sh.loadFromPkl()

        else:
            os.makedirs(PATH_TO_SESSION + sname)
            self.sh.saveToPkl()
            self.label_msg = "Session Saved as: " + sname
            self.sh.info.flag = True
