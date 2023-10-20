from dash import Dash
from .Theme import Theme
from .DvpLayout import DvpLayout
from .DvpAffix import DvpAffix
from .DvpContent import DvpContent
from .DvpMenu import DvpMenu
from .DvpSpinner import DvpSpinner


class App(Dash):
    def __init__(
            self,
            menu={
                'id': 'dvp-top-nav',
                'currentKey': 'home',
                'menuItems': [],
            },
            content=[],
            *args,
            **kwargs
    ):
        self.suppress_callback_exceptions = True
        self.debug = True
        Dash.__init__(self, *args, **kwargs)
        setattr(
            self,
            'layout',
            Theme(
                DvpSpinner(
                    DvpLayout(
                        [
                            DvpAffix(
                                DvpMenu(
                                    id=menu['id'],
                                    isTopNav=True,
                                    mode='horizontal',
                                    currentKey=menu['currentKey'],
                                    menuItems=menu['menuItems'],
                                    domain='http://123.com/'
                                )
                            ),
                            DvpContent(content)
                        ],
                        id='biu'
                    ),
                    spinning=True, fullScreen=True, delay=5000, debug=True
                )
            )
        )
