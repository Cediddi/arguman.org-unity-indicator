#!/usr/bin/python
#  -*- coding: utf-8 -*-

try:
    import appindicator
except ImportError:
    import appindicator_replacement as appindicator
from appindicator_replacement import get_icon_filename

import os
from os import path
import webbrowser
import gtk
import gobject
import appdirs
import requests


update_time = 11000

icons = [
    get_icon_filename("arguman.png"),
    get_icon_filename("arguman_b.png")
]

conf_dir = appdirs.user_config_dir("argumanorg_indicator")

if not path.exists(conf_dir):
    if path.exists(conf_dir):
        os.remove(conf_dir)
    os.mkdir(conf_dir)


def get_current_icon():
    if not path.exists(path.join(conf_dir, "icon_index")):
        set_current_icon(0)
    with open(path.join(conf_dir, "icon_index")) as f:
        output = f.read()
    if output.isdigit():
        return int(output)
    return 0


def set_current_icon(index):
    with open(path.join(conf_dir, "icon_index"), "wb") as f:
        f.write(str(index))
    return get_current_icon()

current_icon = get_current_icon()

indicator = appindicator.Indicator('wallch_indicator',
                                   icons[current_icon],
                                   appindicator.CATEGORY_APPLICATION_STATUS)
indicator.set_status(appindicator.STATUS_ACTIVE)

menu = gtk.Menu()
seperator = gtk.SeparatorMenuItem()
update_item = gtk.MenuItem('Update Now')
icon_item = gtk.MenuItem('Change Icon')
quit_item = gtk.MenuItem('Quit')

menu.append(seperator)
menu.append(update_item)
menu.append(icon_item)
menu.append(quit_item)

indicator.set_menu(menu)
seperator.show()
update_item.show()
icon_item.show()
quit_item.show()


def get_argumans():
    response = requests.get("http://arguman.org/api/v1/arguments/",
                            params={"page_size": 10})
    return response.json()


def inverse_icon(item):
    global current_icon, indicator
    current_icon = set_current_icon((current_icon+1) % 2)
    indicator.set_icon(icons[current_icon])


def quit_gtk(item):
    gtk.main_quit()


def open_webpage(item, url):
    webbrowser.open(url)


def update(item=None):
    for item in menu.get_children()[:-4]:
        menu.remove(item)

    argumans = get_argumans()["results"]
    argumans.reverse()
    for arguman in argumans:
        item = gtk.MenuItem("{title} //{uname}".format(
            title=arguman["title"], uname=arguman["user"]["username"]))
        item.connect('activate', open_webpage,
                     "http://arguman.org/"+arguman["slug"])
        menu.prepend(item)
        item.show()

gobject.timeout_add(500, update)
gobject.timeout_add(update_time, lambda: update() is None)

update_item.connect('activate', update)
icon_item.connect('activate', inverse_icon)
quit_item.connect('activate', quit_gtk)

gtk.main()