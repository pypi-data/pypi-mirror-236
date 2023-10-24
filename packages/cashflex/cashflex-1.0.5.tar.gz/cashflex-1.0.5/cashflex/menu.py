# menu.py
#
# Copyright 2023 gary-1959
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gio

class MenuActions:
    @staticmethod
    def about():
        print("ABOUT clicked")

    @staticmethod
    def user_manual():
        print("USER MANUAL clicked")
    

class CashflexMenu:

    def manual_menu(self, action, value):
        launcher = Gtk.UriLauncher.new("https://github.com/gary-1959/cashflex/blob/main/README.md")
        launcher.launch()

    def close_menu(self, action, value):
        self.app.quit() 

    def about_menu(self, action, value):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self.app.get_active_window())
        dialog.set_modal(True)
        dialog.set_program_name("Cashflex Money Manager")
        dialog.set_authors(["Gary Barnes"])
        dialog.set_copyright("Copyright 2023 Gary Barnes")
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_website("https://github.com/gary-1959/cashflex")
        dialog.set_website_label("Cashflex Website")
        dialog.set_version("1.0")
        logo = Gtk.Image.new_from_file("icons/128x128/uk.co.contrelec.cashflex.svg")
        dialog.set_logo(logo.get_paintable())

        dialog.set_visible(True)

    def on_menu(self, action, value):
        print('Action: {}\nValue: {}'.format(action, value))

    def __init__(self, builder, app):

        self.app = app

        mbuilder = Gtk.Builder.new_from_file("cashflex/ui/menu.ui")

        action_manual = Gio.SimpleAction.new('manual', None)
        action_manual.connect('activate', self.manual_menu)
        app.add_action(action_manual)

        action_about = Gio.SimpleAction.new('about', None)
        action_about.connect('activate', self.about_menu)
        app.add_action(action_about)

        action_close = Gio.SimpleAction.new('close', None)
        action_close.connect('activate', self.close_menu)
        app.add_action(action_close)

        menumodel = mbuilder.get_object('main-menu')
        menubar = Gtk.PopoverMenuBar.new_from_model(menumodel)

        titlebar = builder.get_object("header-bar")
        titlebar.pack_start(menubar)
        


  
