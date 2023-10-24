# custom.py
#
# CUSTOMISED WIDGETS
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


from gi.repository import Gtk, Gdk, Gio, GObject, GLib
import re
import sqlite3
from utils import CashflexUtils
from datetime import datetime, date
   
# Custom entry for checkbutton linked to db table
class CustomCheckButton(Gtk.CheckButton):
    __gtype_name__ = "CustomCheckButton"
    def __init__(self, align, model, item, db, table, col):
        Gtk.CheckButton.__init__(self)
        self.align = align      # alignment
        self.model = model      # model containing source data rows
        self.item = item        # object containing data
        self.db = db            # open db connection
        self.table = table      # db table to update
        self.col = col          # db table column
        self.connect("toggled", self.cb_toggled)

        self.onFocus = None

        # look at state flags to fire focus event
    def stateChanged(self, item, flags):
        if flags & Gtk.StateFlags.FOCUS_WITHIN or flags & Gtk.StateFlags.FOCUSED:
            if self.onFocus != None:
                self.onFocus(self)

    def updateField(self, a):
        pass

    def cb_toggled(self, a):
        pos = self.item.get_position()
        p = self.model.get_item(pos)
        pid = p.id
        val = 1 if self.get_active() == 1 else 0
        setattr(p, self.col, val)    # update value in model

        # update item in database
        try:
            cur = self.db.conn.cursor()
            cur.execute("UPDATE " + self.table + " SET " + self.col + " = ? WHERE id = ?", [val, pid])
            self.db.conn.commit()
        except Exception as e:
            CashflexUtils.Alert(CashflexUtils.alert_types.ERROR, "Data Update Error", e)

class SimpleDropDownList(Gtk.DropDown):
    __gtype_name__ = "SimpleDropDownList"

    # simple object with name fields
    class DropDownObject(GObject.Object):
        name = GObject.Property(type=str)
        def __init__(self, name = "NO NAME"):
            GObject.GObject.__init__(self)
            self.name = name

    def __init__(self, list):
        Gtk.DropDown.__init__(self)
        self.list = list                # list of strings
        self.onFocus = None

        self.store = Gio.ListStore.new(self.DropDownObject)
        self.set_model(Gtk.SortListModel.new(model=self.store, sorter=None))
        self.factory = Gtk.SignalListItemFactory.new()
        self.factory.connect("setup", self.setup)
        self.factory.connect("bind", self.bind)
        self.set_factory(self.factory)

        # build list
        for v in list:
            r = self.DropDownObject(v)
            self.store.append(r)

        self.connect("notify::selected-item", self.selected)

    # look at state flags to fire focus event
    def stateChanged(self, item, flags):
        if flags & Gtk.StateFlags.FOCUS_WITHIN or flags & Gtk.StateFlags.FOCUSED:
            if self.onFocus != None:
                self.onFocus(self)

    def updateField(self, a):
        pass
                
    def setup(self, fact, item):
        item.set_child(Gtk.Label(halign=Gtk.Align.START))

    def bind(self, fact, item):
        f = item.get_child()
        f.set_label(str(getattr(item.get_item(), "name")))

    def selected(self, item, selected):

        if item.get_selected_item() == None: return
        x = item.get_selected_item()
        val = x.name

    def set_selected(self, v):
        # overrides base routine to get row id from value
        # get row containing name
        val = CashflexUtils.find_row_by_name(v, self.store)
        super().set_selected(val)

class CustomDropDownList(Gtk.DropDown):
    __gtype_name__ = "CustomDropDownList"

    # simple object with name fields
    class DropDownObject(GObject.Object):
        name = GObject.Property(type=str)
        def __init__(self, name = "NO NAME"):
            GObject.GObject.__init__(self)
            self.name = name

    def __init__(self, parent, align, model, item, db, table, col, list):
        Gtk.DropDown.__init__(self)
        self.align = align              # alignment
        self.model = model              # model containing source data rows
        self.item = item                # object containing data
        self.db = db                    # open db connection
        self.table = table              # db table to update
        self.col = col                  # db table column
        self.list = list                # list of strings
        self.parent = parent

        self.onFocus = None

        self.store = Gio.ListStore.new(self.DropDownObject)
        self.set_model(Gtk.SortListModel.new(model=self.store, sorter=None))
        self.factory = Gtk.SignalListItemFactory.new()
        self.factory.connect("setup", self.setup)
        self.factory.connect("bind", self.bind)
        self.set_factory(self.factory)

        # build list
        for v in list:
            r = self.DropDownObject(v)
            self.store.append(r)

        self.connect("notify::selected-item", self.selected)

    # look at state flags to fire focus event
    def stateChanged(self, item, flags):
    
        if flags & Gtk.StateFlags.FOCUS_WITHIN or flags & Gtk.StateFlags.FOCUSED:
            if self.onFocus != None:
                self.onFocus(self)

    def updateField(self, a):
        pass
                
    def setup(self, fact, item):
        item.set_child(Gtk.Label(halign=Gtk.Align.START))

    def bind(self, fact, item):
        f = item.get_child()
        f.set_label(str(getattr(item.get_item(), "name")))

    def selected(self, item, selected):

        if item.get_selected_item() == None: return

        pid = getattr(self.parent.get_item(), "id")
        x = item.get_selected_item()
        val = x.name
        
        setattr(self.parent.get_item(), self.col, val)

        # update item in database
        try:
            cur = self.db.conn.cursor()
            cur.execute("UPDATE " + self.table + " SET " + self.col + " = ? WHERE id = ?", [val, pid])
            self.db.conn.commit()
        except Exception as e:
            CashflexUtils.Alert(CashflexUtils.alert_types.ERROR, "Data Update Error", e)

    def set_selected(self, v):
        # overrides base routine to get row id from value
        # get row containing name
        val = CashflexUtils.find_row_by_name(v, self.store)
        super().set_selected(val)

# Custom dropdown from table with id, name, sort_order fields linked to db table
class CustomDropDownTable(Gtk.DropDown):
    __gtype_name__ = "CustomDropDownTable"

    # simple object with id and name fields
    class DropDownObject(GObject.Object):
        id = GObject.Property(type=int)
        name = GObject.Property(type=str)
        def __init__(self, id = 0, name = "NO NAME", *args):
            GObject.GObject.__init__(self)
            self.id = id
            self.name = name

    def __init__(self, parent, align, model, item, db, table, col, list_sql):
        Gtk.DropDown.__init__(self)
        self.align = align              # alignment
        self.model = model              # model containing source data rows
        self.item = item                # object containing data
        self.db = db                    # open db connection
        self.table = table              # db table to update
        self.col = col                  # db table column
        self.list_sql = list_sql        # sql to get list with id, name
        self.parent = parent

        self.onFocus = None

        self.store = Gio.ListStore.new(self.DropDownObject)
        self.set_model(Gtk.SortListModel.new(model=self.store, sorter=None))
        self.factory = Gtk.SignalListItemFactory.new()
        self.factory.connect("setup", self.setup)
        self.factory.connect("bind", self.bind)
        self.set_factory(self.factory)

        # build list

        cur = self.db.conn.cursor()
        rc = cur.execute(list_sql)

        for v in rc:
            r = self.DropDownObject(*v)
            self.store.append(r)

        self.connect("notify::selected-item", self.selected)

    # look at state flags to fire focus event
    def stateChanged(self, item, flags):
        if flags & Gtk.StateFlags.FOCUS_WITHIN or flags & Gtk.StateFlags.FOCUSED:
            if self.onFocus != None:
                self.onFocus(self)

    def setup(self, fact, item):
        item.set_child(Gtk.Label(halign=Gtk.Align.START))

    def bind(self, fact, item):
        f = item.get_child()
        f.set_label(str(getattr(item.get_item(), "name")))
        setattr(f, "pid", getattr(item.get_item(), "id"))

    def selected(self, item, selected):

        if item.get_selected_item() == None: return

        pid = getattr(self.parent.get_item(), "id")
        x = item.get_selected_item()
        #val = getattr(item.get_selected_item(), "id")
        val = x.id
        
        setattr(self.parent.get_item(), self.col, val)

        # update item in database
        try:
            cur = self.db.conn.cursor()
            cur.execute("UPDATE " + self.table + " SET " + self.col + " = ? WHERE id = ?", [val, pid])
            self.db.conn.commit()
        except Exception as e:
            CashflexUtils.Alert(CashflexUtils.alert_types.ERROR, "Data Update Error", e)

    def set_selected(self, v):
        # overrides base routine to get row id from value
        # get row containing id
        val = CashflexUtils.find_row_by_id(v, self.store)
        super().set_selected(val)
   
# Custom entry
class SimpleEntry(Gtk.Entry):
    __gtype_name__ = "SimpleEntry"
    def __init__(self, align, validate):
        Gtk.Entry.__init__(self)
        self.validate = validate # validation routine
        self.valid = True
        self.text = self.get_first_child()
        self.set_alignment(CashflexUtils.align_to_real(align))

        self.onFocus = None

        # to capture TAB key
        kc = Gtk.EventControllerKey()
        self.add_controller(kc)
        kc.connect("key-pressed", self.keyPressed)
        self.text.connect("changed", self.changedText)
        self.connect("activate", self.updateField)
        self.connect("state-flags-changed", self.stateChanged)

        if self.validate == CashflexUtils.validate_date:
            self.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "x-office-calendar-symbolic")
            self.connect("icon_release", self.iconRelease)
            calbuilder = Gtk.Builder()
            calbuilder.add_from_file("cashflex/ui/calendar.ui")
            self.calpop = calbuilder.get_object("calpop")
            self.calpop.set_parent(self)
            self.calpop.get_child().connect("day-selected", self.daySelected)

    # look at state flags to fire focus event
    def stateChanged(self, item, flags):
        if flags & Gtk.StateFlags.FOCUS_WITHIN or flags & Gtk.StateFlags.FOCUSED:
            if self.onFocus != None:
                self.onFocus(self)

    def daySelected(self, cal):
        self.calpop.popdown()
        gdate = cal.get_date()
        d = gdate.format("%Y-%m-%d")
        self.set_text(d)
        self.updateField(False)

    def iconRelease(self, item, pos):
        n = self.get_icon_name(pos)
        if n == "x-office-calendar-symbolic":
            if self.valid:
                d = self.get_text()
                d = re.sub('[/\\\]+', '-', d)
                try:
                    gdate = GLib.DateTime.new_from_iso8601(d + "T12:00:00+00:00")
                except:
                    CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Date Error", "Unable to interpret date.\n Dates should be in the format YYYY-MM-DD")
                    gdate = GLib.DateTime.new_now(GLib.TimeZone.new_local())
                cal = self.calpop.get_child();
                cal.select_day(gdate)
            self.calpop.popup()
                                             
    # capture TAB key and update if valid
    def keyPressed(self, kv, kc, state, b):
        pass
        #if not self.valid:
        #    return True
        #else:
        #    self.updateField(False)
        #return False

    def changedText(self, item):
        pos = self.get_position()
        if self.validate != None:
            valid = self.validate(item.get_text())

            # validate
            
            if not valid:
                self.valid = False
                self.add_css_class("error")

            else:

                self.valid = True
                self.remove_css_class("error")
        else:
            self.valid = True
            self.remove_css_class("error")

    def updateField(self, a):

        val = self.get_text()

        if self.valid:

            corrected = None    
            if self.validate == CashflexUtils.validate_amount:
                corrected = f"{float(val):0.2f}"
            elif self.validate == CashflexUtils.validate_date:
                val = re.sub('[/\\\]+', '-', val)
                m = re.fullmatch(r"(\d{1,4})[-/\\](\d{1,2})[-/\\](\d{1,2})", val)
                d = date(year = int(m[1]), month =int(m[2]), day = int(m[3]))
                corrected = d.strftime("%Y-%m-%d")

            if corrected != None:
                self.text.handler_block_by_func(self.changedText)
                self.set_text(corrected)
                self.text.handler_unblock_by_func(self.changedText)

# Custom entry for grids linked to db table
class CustomEntry(Gtk.Entry):
    __gtype_name__ = "CustomEntry"
    def __init__(self, align, model, item, db, table, col, validate):
        Gtk.Entry.__init__(self)
        self.align = align      # alignment
        self.model = model      # model containing source data rows
        self.item = item        # object containing data
        self.db = db            # open db connection
        self.table = table      # db table to update
        self.col = col          # db table column
        self.validate = validate # validation routine
        self.valid = True
        self.text = self.get_first_child()
        self.set_alignment(CashflexUtils.align_to_real(align))

        self.onFocus = None

        # to capture TAB key
        kc = Gtk.EventControllerKey()
        self.add_controller(kc)
        kc.connect("key-pressed", self.keyPressed)
        self.text.connect("changed", self.changedText)
        self.connect("activate", self.updateField)
        self.connect("state-flags-changed", self.stateChanged)

        if self.validate == CashflexUtils.validate_date:
            self.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "x-office-calendar-symbolic")
            self.connect("icon_release", self.iconRelease)
            calbuilder = Gtk.Builder()
            calbuilder.add_from_file("cashflex/ui/calendar.ui")
            self.calpop = calbuilder.get_object("calpop")
            self.calpop.set_parent(self)
            self.calpop.get_child().connect("day-selected", self.daySelected)

    def stateChanged(self, item, flags):

        if flags & Gtk.StateFlags.FOCUS_WITHIN or flags & Gtk.StateFlags.FOCUSED:
            if self.onFocus != None:
                self.onFocus(self)
        

    def daySelected(self, cal):
        self.calpop.popdown()
        gdate = cal.get_date()
        d = gdate.format("%Y-%m-%d")
        self.set_text(d)
        self.updateField(False)

    def iconRelease(self, item, pos):
        n = self.get_icon_name(pos)
        if n == "x-office-calendar-symbolic":
            if self.valid:
                d = self.get_text()
                d = re.sub('[/\\\]+', '-', d)
                try:
                    gdate = GLib.DateTime.new_from_iso8601(d + "T12:00:00+00:00")
                except:
                    CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Date Error", "Unable to interpret date.\n Dates should be in the format YYYY-MM-DD")
                    gdate = GLib.DateTime.new_now(GLib.TimeZone.new_local())

                # can't select day because clicking it not working when selected
                # mark_day function only for day of the month
                cal = self.calpop.get_child();
                cal.select_day(gdate)
                self.calpop.popup()
                                             
    # capture TAB key and update if valid
    def keyPressed(self, kv, kc, state, b):
        pass
        #if not self.valid:
        #    return True
        #else:
        #    self.updateField(False)
        #return False

    def changedText(self, item):
        pos = self.get_position()
        if self.validate != None:
            valid = self.validate(item.get_text())

            # validate
            
            if not valid:
                self.valid = False
                self.add_css_class("error")

            else:
                self.valid = True
                self.remove_css_class("error")
        else:
            self.valid = True
            self.remove_css_class("error")

    def updateField(self, a):
        pos = self.item.get_position()
        p = self.model.get_item(pos)
        pid = p.id

        val = self.get_text()

        if self.valid:

            # update item
            
            try:
                cur = self.db.conn.cursor()
                cur.execute("UPDATE " + self.table + " SET " + self.col + " = ? WHERE id = ?", [val, pid])
                self.db.conn.commit()
            except Exception as e:
                CashflexUtils.Alert(CashflexUtils.alert_types.ERROR, "Data Update Error", e)

            corrected = val    
            if self.validate == CashflexUtils.validate_amount:
                corrected = f"{float(val):0.2f}"
            elif self.validate == CashflexUtils.validate_date:
                val = re.sub('[/\\\]+', '-', val)
                m = re.fullmatch(r"(\d{1,4})[-/\\](\d{1,2})[-/\\](\d{1,2})", val)
                d = date(year = int(m[1]), month =int(m[2]), day = int(m[3]))
                corrected = d.strftime("%Y-%m-%d")

            if corrected != None:
                self.text.handler_block_by_func(self.changedText)
                self.set_text(corrected)
                self.text.handler_unblock_by_func(self.changedText)
                #GLib.idle_add(self.set_position, pos)

            if isinstance(getattr(p, self.col), str):
                setattr(p, self.col, str(corrected))    # update value in model
            if isinstance(getattr(p, self.col), int) :
                setattr(p, self.col, int(val))    # update value in model




