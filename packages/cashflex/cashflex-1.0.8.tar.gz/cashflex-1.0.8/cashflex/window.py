# window.py
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


from gi.repository import Gtk, Gdk

from pockets import PocketsGrid
from forecast import ShowPlot, ForecastControls
from menu import CashflexMenu
from db import CashflexDB


__lastFocus__ = None

class CashflexWindow(Gtk.ApplicationWindow):

    def showPage(self, stack, param):
        c = stack.get_visible_child()
        p = c.get_property("name")

        match p:
            case "pockets-page":
                pass
            case "payments-page":
                pass
            case "forecast-page":
                pass
            case _:
                print("Page drawing routine not defined for " + p)

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # CSS Styling
        self.css_provider = Gtk.CssProvider()
        Gtk.CssProvider.load_from_path(self.css_provider, 'cashflex/css/cashflex.css')

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.builder = Gtk.Builder()
        self.builder.add_from_file("cashflex/ui/window.ui")

        # load menu
        menu = CashflexMenu(self.builder, app)

        p = self.builder.get_object("main-stack")
        p.connect("notify::visible-child",self.showPage)


        # fill pockets grid
        pockets_container = self.builder.get_object("pockets-container")
        pocket_income_container = self.builder.get_object("pocket-income-container")
        pocket_payments_container = self.builder.get_object("pocket-payments-container")
       
        pocket_add_button = self.builder.get_object("pocket-add-button")
        pocket_income_add_button = self.builder.get_object("pocket-income-add-button")
        pocket_payment_add_button = self.builder.get_object("pocket-payment-add-button")

        self.win = self.builder.get_object("main_window") 
        # updates fields on focus out

        def window_focus(self, flags):
            global __lastFocus__
            if flags & Gtk.StateFlags.FOCUS_WITHIN:
                item = self.get_focus()
                if __lastFocus__ != item :
                    if __lastFocus__ != None:
                        if hasattr(__lastFocus__, "updateField") :
                            __lastFocus__.updateField(False)
                        elif hasattr(__lastFocus__, "get_parent") : # entry types
                            parent = __lastFocus__.get_parent()
                            if hasattr(parent, "updateField") :
                                parent.updateField(False)

                    __lastFocus__ = item

        self.win.connect("state-flags-changed", window_focus)

        self.win.set_application(app)  # Application will close once it no longer has active windows attached to it
        self.win.present()

        db = CashflexDB()
        if db.conn == None:
            return

        pocket_grid = PocketsGrid(db, pockets_container, pocket_income_container, pocket_payments_container, \
                    pocket_add_button, pocket_income_add_button, pocket_payment_add_button)
        
        plot_window = self.builder.get_object("plot-window")
        ForecastControls(self.builder, db, pocket_grid, plot_window)
        
        ShowPlot(plot_window)





