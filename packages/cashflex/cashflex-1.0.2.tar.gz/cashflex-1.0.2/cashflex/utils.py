# utils.py
#
# COMMON ROUTINES
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

from gi.repository import Gtk
import re
from datetime import datetime, date

class CashflexUtils():

    unit_list = ["TERM", "DAY", "MONTH", "WEEK", "QUARTER", "YEAR"]
    class alert_types():
        NONE = 0
        WARNING = 2
        ERROR = 3

    @staticmethod
    def log(msg):
        print(datetime.now(), msg)

    @staticmethod
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def scroll_to_top(container):
        vscroll = container.get_vscrollbar()
        vadj = vscroll.get_adjustment()
        lower = vadj.get_lower()
        val = vadj.get_value()
        vadj.set_value(lower)   

    @staticmethod
    def sort_standard(a, b, d):
        return 0 if (getattr(a, d) == getattr(b, d)) else -1 if getattr(b, d) > getattr(a, d) else 1

    @staticmethod
    def validate_name(s):
        return True
    
    @staticmethod
    def validate_sort_code(s):
        if s == "":
            return True
        m = re.fullmatch(r"\d{2}-\d{2}-\d{2}", s)
        if m == None:
            return False

        return True
    
    @staticmethod
    def validate_date(s):
        m = re.fullmatch(r"(\d{1,4})[-/\\](\d{1,2})[-/\\](\d{1,2})", s)
        if m == None:
            return False
        
        year = int(m[1])
        month = int(m[2])
        day = int(m[3])
        try:
            d = date(year = year, month = month, day = day)
        except ValueError as e:
            return False
       
        return True
    
    @staticmethod
    def validate_amount(s):

        if s == "" or s == ".":
            return False
        m = re.match(r"(^[\-\+]{0,1}\d*)(\.{0,1})(\d{0,2})$", s)
        if m == None:
            return False

        return True

    @staticmethod
    def validate_integer(s):
        m = re.fullmatch(r"^[0-9]+$", s)
        if m == None:
            # s = re.sub('[^0-9a-zA-Z\s]+', '', s)
            return False

        return True 


    # return x-align value from GtkAlign constant
    @staticmethod
    def align_to_real(align):
        a = 0.0
        match align:
            case Gtk.Align.CENTER:
                a = 0.5
            case Gtk.Align.END:
                a = 1.0
            case _:
                a = 0.0
        return(a)
    
    @staticmethod
    # search row for object matching field id
    def find_row_by_id(id, model):
        i = 0
        for row in model:
            if row.id == id:
                return i
            i += 1
        return 0
    
    @staticmethod
    # search row for object matching field id
    def find_row_by_name(name, model):
        i = 0
        for row in model:
            if row.name == name:
                return i
            i += 1
        return 0
    
    @staticmethod
    # show alert dialog
    def alert( type, title, msg):

        windows = Gtk.Window.get_toplevels()
        builder = Gtk.Builder()
        builder.add_from_file("cashflex/ui/alert.ui")
        win = builder.get_object("alert_dialog")
        win.set_transient_for(windows[0])
        win.set_title(title)

        label = builder.get_object("alert_label")
        label.set_text(msg)

        def ok_clicked(item):
            win.close()
            win.destroy()

        ok = builder.get_object("ok-button")
        ok.connect("clicked", ok_clicked)

        win.present()

    @staticmethod
    # show alert dialog with cancel and ok buttons
    def alert_cancel_ok( type, title, msg, cancel_callback, ok_callback):

        windows = Gtk.Window.get_toplevels()
        builder = Gtk.Builder()
        builder.add_from_file("cashflex/ui/alert_cancel_ok.ui")
        win = builder.get_object("alert_dialog")
        win.set_transient_for(windows[0])
        win.set_title(title)

        label = builder.get_object("alert_label")
        label.set_text(msg)

        def cancel_clicked(item):
            win.close()
            win.destroy()
            cancel_callback()

        def ok_clicked(item):
            win.close()
            win.destroy()
            ok_callback()

        cancel = builder.get_object("cancel-button")
        cancel.connect("clicked", cancel_clicked)

        ok = builder.get_object("ok-button")
        ok.connect("clicked", ok_clicked)

        win.present()

    @staticmethod
    # get confirmation
    def confirm_delete(callback):

        windows = Gtk.Window.get_toplevels()
        builder = Gtk.Builder()
        builder.add_from_file("cashflex/ui/delete.ui")
        win = builder.get_object("delete_dialog")
        win.set_transient_for(windows[0])

        def cancel_clicked(item):
            win.close()
            win.destroy()
            callback(False)

        def delete_clicked(item):
            win.close()
            win.destroy()
            callback(True)

        cancel = builder.get_object("cancel-button")
        cancel.connect("clicked", cancel_clicked)

        delete = builder.get_object("delete-button")
        delete.connect("clicked", delete_clicked)

        win.present()

    

