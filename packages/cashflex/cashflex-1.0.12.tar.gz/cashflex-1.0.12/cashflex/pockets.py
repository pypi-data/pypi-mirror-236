# pockets.py
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


from gi.repository import Gtk, Gio, GObject, GLib

import sqlite3
import datetime

from custom import CustomDropDownTable, CustomDropDownList, CustomCheckButton, CustomEntry
from utils import CashflexUtils


class PocketDataObject(GObject.Object):
    id = GObject.Property(type=int)
    name = GObject.Property(type=str)
    sort_code = GObject.Property(type=str)
    account_code = GObject.Property(type=str)
    balance = GObject.Property(type=str)
    growth = GObject.Property(type=str)
    open_date = GObject.Property(type=str)
    sort_order = GObject.Property(type=int)


    # column order must match order of init parameters
    def __init__(self, id = 0, name = "New Pocket", description = "", type = 1, sort_code = "00-00-00", account_code = "00000000", balance= "0.00", growth = "0.00",
                 open_date = datetime.datetime.now().strftime("%Y-%m-%d"), sort_order = 100):
        GObject.GObject.__init__(self)
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.sort_code = sort_code
        self.account_code = account_code
        self.balance = balance
        self.growth = growth
        self.open_date = open_date
        self.sort_order = sort_order

class PocketComponentObject(GObject.Object):
    id = GObject.Property(type=int)
    type = GObject.Property(type=str)
    active = GObject.Property(type=int)
    parent = GObject.Property(type=int)
    name = GObject.Property(type=str)
    amount = GObject.Property(type=str)
    frequency = GObject.Property(type=int)
    frequency_unit = GObject.Property(type=str)
    start_date = GObject.Property(type=str)
    end_date = GObject.Property(type=str)
    last_update = GObject.Property(type=str)
    send_to = GObject.Property(type=int)
    growth = GObject.Property(type=str)
    sort_order = GObject.Property(type=int)


    # column order must match order of init parameters
    def __init__(self, id = 0, type="I", active = 1, parent = 0, name = "New Component", amount = "0.00", frequency = 1, frequency_unit = "MONTH",
                 start_date = datetime.datetime.now().strftime("%Y-%m-%d"), end_date = datetime.datetime.now().strftime("%Y-%m-%d"), \
                 last_update = datetime.datetime.now().strftime("%Y-%m-%d"), send_to = 0, growth = "0.00", sort_order = 100):
        GObject.GObject.__init__(self)
        self.id = id
        self.type = type
        self.active = active
        self.parent = parent
        self.name = name
        self.amount = amount
        self.frequency = frequency
        self.frequency_unit = frequency_unit
        self.start_date = start_date
        self.end_date = end_date
        self.last_update = last_update
        self.send_to = send_to
        self.growth = growth
        self.sort_order = sort_order


class PocketComponentsGrid(Gtk.ColumnView):
    __gtype_name__ = "PocketComponentsGrid"

    def __init__(self, ctype, db, container, parent, add_button, pocket_selector):
        Gtk.ColumnView.__init__(self)

        self.ctype = ctype
        self.db = db
        self.container = container
        self.parent = parent
        self.pocket_selector = pocket_selector

        # column order must match order of init parameters
        self.cols = [
            { "dbcolumn": "id",             "dbselector": "id",           "title": "ID",              "expand": False, "visible": False,   "editor": "none",      "align": Gtk.Align.END,    "validate": None },
            { "dbcolumn": "type",           "dbselector": "type",         "title": "TYPE",            "expand": False, "visible": False,   "editor": "none",      "align": Gtk.Align.CENTER, "validate": None  },
            { "dbcolumn": "active",         "dbselector": "active",       "title": "ACTIVE",          "expand": False, "visible": True,    "editor": "checkbox",  "align": Gtk.Align.CENTER, "validate": None  },
            { "dbcolumn": "parent",         "dbselector": "parent",       "title": "POCKET",          "expand": False, "visible": False,   "editor": "none",      "align": Gtk.Align.CENTER, "validate": None  },
            { "dbcolumn": "name",           "dbselector": "name",         "title": "NAME",            "expand": True,  "visible": True,    "editor": "text",      "align": Gtk.Align.START,  "validate": CashflexUtils.validate_name },
            { "dbcolumn": "amount",         "dbselector": "PRINTF('%0.2f', amount)",       "title": "AMOUNT",          "expand": False, "visible": True,    "editor": "text",      "align": Gtk.Align.END,    "validate": CashflexUtils.validate_amount },
            { "dbcolumn": "frequency",      "dbselector": "frequency",    "title": "FREQUENCY",       "expand": False, "visible": True,    "editor": "text",      "align": Gtk.Align.CENTER, "validate": CashflexUtils.validate_integer },
            { "dbcolumn": "frequency_unit", "dbselector": "frequency_unit", "title": "INTERVAL",      "expand": False, "visible": True,    "editor": "funits",    "align": Gtk.Align.START,  "validate": None  },
            { "dbcolumn": "start_date",     "dbselector": "start_date",   "title": "START DATE",      "expand": False, "visible": True,    "editor": "text",      "align": Gtk.Align.END,    "validate": CashflexUtils.validate_date },
            { "dbcolumn": "end_date",       "dbselector": "end_date",     "title": "END DATE",        "expand": False, "visible": True,    "editor": "text",      "align": Gtk.Align.END,    "validate": CashflexUtils.validate_date },
            { "dbcolumn": "last_update",    "dbselector": "last_update",  "title": "LAST UPDATE",     "expand": False, "visible": True,    "editor": "text",      "align": Gtk.Align.END,    "validate": CashflexUtils.validate_date },
            { "dbcolumn": "send_to",        "dbselector": "send_to",      "title": "SEND TO",         "expand": False, "visible": True,    "editor": "pockets",   "align": Gtk.Align.START,  "validate": None  },
            { "dbcolumn": "growth",         "dbselector": "PRINTF('%0.2f', growth)",       "title": "GROWTH",          "expand": False, "visible": True,    "editor": "text",   "align": Gtk.Align.END,  "validate": CashflexUtils.validate_amount  },
            { "dbcolumn": "sort_order",     "dbselector": "sort_order",   "title": "SORT _ORDER",     "expand": False, "visible": False,   "editor": "none",      "align": Gtk.Align.START,  "validate": None   }
        ]
        col_icon = [
            { "icon": "edit-delete-symbolic", "function": "DELETE",   "expand": False, "visible": True,   "tooltip": "Delete",    "align": Gtk.Align.CENTER }
        ]

        self.component_store = Gio.ListStore.new(PocketComponentObject)
        self.component_model = Gtk.SortListModel.new(model=self.component_store, sorter=self.get_sorter())
        
        self.component_selector = Gtk.SingleSelection.new(model=self.component_model)
        self.set_model(self.component_selector)

        self.set_single_click_activate(False)    # still needs double-click
        self.set_show_column_separators(True)
        self.set_show_row_separators(True)
        self.connect("activate", self.component_selected)

        for v in self.cols:
            factory = Gtk.SignalListItemFactory.new()
            factory.connect("setup", self.f_setup, v)
            factory.connect("bind", self.f_bind, v)

            c = Gtk.ColumnViewColumn(title=v["title"], factory=factory)
            c.set_sorter(Gtk.CustomSorter.new(CashflexUtils.sort_standard, v["dbcolumn"]))
            #c.set_id("col_" + v["dbcolumn"])
            c.set_resizable(True)

            c.set_visible(v["visible"])
            c.set_expand(v["expand"])

            self.append_column(c)

        for v in col_icon:
            factory = Gtk.SignalListItemFactory.new()
            factory.connect("setup", self.f_setup_icon, v)
            factory.connect("bind", self.f_bind_icon, v)

            c = Gtk.ColumnViewColumn(title="", factory=factory)
            c.set_visible(v["visible"])
            c.set_expand(v["expand"])

            self.append_column(c)

            # TODO: Find away to align header title
        
        add_button.connect("clicked", self.component_add_clicked)
        self.container.set_child(self)

    def component_add_clicked(self, item):

        pocket = self.pocket_selector.get_selected_item() # PocketDataObject
        pc = PocketComponentObject(parent = pocket.id, type = self.ctype)

        cur = self.db.conn.cursor()
        cur.execute("INSERT INTO pocket_components " \
                    "(active, type, parent, name, amount, frequency, frequency_unit, start_date, end_date, last_update, sort_order, send_to, growth) " \
                    "VALUES (? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                    [pc.active, pc.type, pc.parent, pc.name, pc.amount, pc.frequency, pc.frequency_unit, \
                     pc.start_date, pc.end_date, pc.last_update, pc.sort_order, pc.send_to, pc.growth])
        self.db.conn.commit()
        rc = cur.execute("SELECT last_insert_rowid()")
        
        pc.id = rc.lastrowid

        self.component_store.insert(0, pc)
        self.component_selector.select_item(0, True)
        self.component_selected()

        GLib.idle_add(CashflexUtils.scroll_to_top, self.container)
        

    def component_selected(self):
        component = self.component_selector.get_selected_item() # PocketComponentObject

    def populate_grid(self, parent):

        self.component_store.remove_all()

        # get data from database

        sql = "SELECT " + ", ".join((v["dbselector"] + " AS '" + v["dbcolumn"] + "' ") for v in self.cols) + \
                                    " FROM pocket_components " + \
                                    " WHERE parent = '" + str(parent) + "' AND type = '" + self.ctype + "' " + \
                                    " ORDER BY pocket_components.sort_order, pocket_components.name, pocket_components.id"
        cur = self.db.conn.cursor()
        rc = cur.execute(sql)

        for v in rc:
            r = PocketComponentObject(*v)
            self.component_store.append(r)

    def icon_click(self, button, function, item):
        pos = item.get_position()
        p = self.component_model.get_item(pos)
        match function:
            case "DELETE":

                def callback(response):
                    if response:
                        sql = "DELETE FROM pocket_components WHERE id=" + str(p.id)
                        cur = self.db.conn.cursor()
                        cur.execute(sql)
                        self.db.conn.commit()

                        i = 0
                        for r in self.component_store:
                            if r.id == p.id :
                                self.component_store.remove(i)
                                break
                            i += 1

                CashflexUtils.confirm_delete(callback)
            case _:
                pass        

    def f_setup(self, fact, item, v):
        match v["editor"]:
            case "text":
                f = CustomEntry( v["align"], self.component_model, item, self.db, \
                                "pocket_components", v["dbcolumn"], v["validate"])
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case "checkbox":
                f = CustomCheckButton( v["align"], self.component_model, item, self.db, \
                                        "pocket_components", v["dbcolumn"])
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case "funits":
                f = CustomDropDownList(item, v["align"], self.component_model, \
                                            item, self.db, "pocket_components", v["dbcolumn"], CashflexUtils.unit_list)
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case "pockets":
                pocket = self.pocket_selector.get_selected_item() # PocketDataObject 
                list_sql = "SELECT 0 AS 'id', ' [ Parent ] ' AS 'name', 10 AS 'sort_order' FROM pockets UNION " + \
                            "SELECT  id, name, sort_order FROM pockets WHERE id <> " + str(pocket.id) + " " \
                            "ORDER BY sort_order, name ASC"

                f = CustomDropDownTable(item, v["align"], self.component_model, \
                                            item, self.db, "pocket_components", v["dbcolumn"], list_sql)
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case _:
                item.set_child(Gtk.Label(halign=v["align"]))

    def f_bind(self, fact, item, v):
        f = item.get_child()
        match v["editor"]:
            case "text":
                f.set_text(str(getattr(item.get_item(), v["dbcolumn"])))
            case "checkbox":
                f.set_active(True if getattr(item.get_item(), v["dbcolumn"]) == 1 else False)
            case "funits":
                f.set_selected(getattr(item.get_item(), v["dbcolumn"]))
            case "pockets":
                x = item.get_item()
                f.set_selected(getattr(item.get_item(), v["dbcolumn"]))
            case _:
                f.set_label(str(getattr(item.get_item(), v["dbcolumn"])))


    def f_setup_icon(self, fact, item, v):
        b = Gtk.Button.new_from_icon_name(v["icon"])
        b.set_tooltip_text(v["tooltip"])
        b.connect("clicked",self.icon_click, v["function"], item)
        item.set_child(b)

    def f_bind_icon(self, fact, item, v):
        pass

    def itemFocussed(self, entry):
        item = entry.item
        pos = item.get_position()
        x = self.component_selector.get_selection()
        if not self.component_selector.is_selected(pos):
            self.component_selector.select_item(pos, True)
            self.component_selected()

class PocketsGrid(Gtk.ColumnView):
    __gtype_name__ = "PocketsGrid"

    def __init__(self, db, container, income_container, payments_container, pocket_add_button, pocket_income_add_button, pocket_payment_add_button):
        Gtk.ColumnView.__init__(self)
        
        self.db = db
        self.container = container
        # column order must match order of init parameters
        self.cols = [
            { "dbcolumn": "id",             "dbselector": "id",                     "title": "ID",              "expand": False,    "visible": False,   "editor": "none", "align": Gtk.Align.END,   "validate": None },
            { "dbcolumn": "name",           "dbselector": "name",                   "title": "NAME",            "expand": True,     "visible": True,    "editor": "text", "align": Gtk.Align.START, "validate": CashflexUtils.validate_name },
            { "dbcolumn": "description",    "dbselector": "description",            "title": "DESCRIPTION",     "expand": False,    "visible": True,    "editor": "text", "align": Gtk.Align.START, "validate": CashflexUtils.validate_name },
            { "dbcolumn": "type",           "dbselector": "type",                   "title": "TYPE",            "expand": False,    "visible": True,    "editor": "types","align": Gtk.Align.START, "validate": None  },
            { "dbcolumn": "sort_code",      "dbselector": "sort_code",              "title": "SORT CODE",       "expand": False,    "visible": True,    "editor": "text", "align": Gtk.Align.START, "validate": CashflexUtils.validate_sort_code  },
            { "dbcolumn": "account_code",   "dbselector": "account_code",           "title": "ACCOUNT NUMBER",  "expand": False,    "visible": True,    "editor": "text", "align": Gtk.Align.START, "validate": CashflexUtils.validate_name  },
            { "dbcolumn": "balance",        "dbselector": "PRINTF('%0.2f', balance)","title": "BALANCE",        "expand": False,    "visible": True,    "editor": "text", "align": Gtk.Align.END,   "validate": CashflexUtils.validate_amount   },
            { "dbcolumn": "growth",         "dbselector": "PRINTF('%0.2f', growth)", "title": "GROWTH",         "expand": False,    "visible": True,    "editor": "text", "align": Gtk.Align.END,   "validate": CashflexUtils.validate_amount  },
            { "dbcolumn": "open_date",      "dbselector": "open_date",              "title": "OPENED",          "expand": False,    "visible": False,   "editor": "none", "align": Gtk.Align.END,   "validate": None  },
            { "dbcolumn": "sort_order",     "dbselector": "sort_order",             "title": "SORT _ORDER",     "expand": False,    "visible": False,   "editor": "none", "align": Gtk.Align.START, "validate": None  }
        ]
        col_icon = [
            { "icon": "edit-delete-symbolic", "function": "DELETE",   "expand": False, "visible": True,   "tooltip": "Delete",    "align": Gtk.Align.CENTER }
        ]

        self.pocket_store = Gio.ListStore.new(PocketDataObject)
        self.pocket_model = Gtk.SortListModel.new(model=self.pocket_store, sorter=self.get_sorter())

        self.pocket_selector = Gtk.SingleSelection.new(model=self.pocket_model)
        self.set_model(self.pocket_selector)

        self.set_single_click_activate(False)    # still needs double-click
        self.set_show_column_separators(True)
        self.set_show_row_separators(True)
        self.connect("activate", self.pocket_selected)

        for v in self.cols:
            factory = Gtk.SignalListItemFactory.new()
            factory.connect("setup", self.f_setup, v)
            factory.connect("bind", self.f_bind, v)

            c = Gtk.ColumnViewColumn(title=v["title"], factory=factory)
            c.set_sorter(Gtk.CustomSorter.new(CashflexUtils.sort_standard, v["dbcolumn"]))
            #c.set_id("col_" + v["dbcolumn"])
            c.set_resizable(True)
            c.set_visible(v["visible"])
            c.set_expand(v["expand"])

            self.append_column(c)

        for v in col_icon:
            factory = Gtk.SignalListItemFactory.new()
            factory.connect("setup", self.f_setup_icon, v)
            factory.connect("bind", self.f_bind_icon, v)

            c = Gtk.ColumnViewColumn(title="", factory=factory)
            c.set_visible(v["visible"])
            c.set_expand(v["expand"])

            self.append_column(c)


        pocket_add_button.connect("clicked", self.pocket_add_clicked)

        self.container.set_child(self)

        self.income_grid = PocketComponentsGrid("I", self.db, income_container, self, pocket_income_add_button, self.pocket_selector)
        self.payments_grid = PocketComponentsGrid("P", self.db, payments_container, self, pocket_payment_add_button, self.pocket_selector)
        self.populate_grid()
        self.pocket_selected()

    #select subdata
    def pocket_selected(self):
        pocket = self.pocket_selector.get_selected_item() # PocketDataObject
        if pocket == None:
            id = 0          # no pocket has id zero - clears grid
        else:
            id = pocket.id
            self.income_grid.populate_grid(id)
            self.payments_grid.populate_grid(id)

    def pocket_add_clicked(self, item):
        pc = PocketDataObject()

        cur = self.db.conn.cursor()
        cur.execute("INSERT INTO pockets " \
                    "(name, description, balance, growth, type, sort_code, account_code, open_date, sort_order) " \
                    "VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)", [ pc.name, pc.description, pc.balance, pc.growth, pc.type, \
                        pc.sort_code, pc.account_code, pc.open_date, pc.sort_order ])
        self.db.conn.commit()
        rc = cur.execute("SELECT last_insert_rowid()")
        
        pc.id = rc.lastrowid

        self.pocket_store.insert(0, pc)
        self.pocket_selector.select_item(0, True)
        self.pocket_selected()

        GLib.idle_add(CashflexUtils.scroll_to_top, self.container)

    def populate_grid(self):
        
        self.pocket_store.remove_all()
        # get data from database

        sql = "SELECT " + ", ".join((v["dbselector"] + " AS '" + v["dbcolumn"] + "' ") for v in self.cols) + \
                                    " FROM pockets " + \
                                    " ORDER BY sort_order, name, id"

        cur = self.db.conn.cursor()
        rc = cur.execute(sql)

        for v in rc:
            r = PocketDataObject(*v)
            self.pocket_store.append(r)


    # make sure row is selected when widget entered
    def itemFocussed(self, entry):
        item = entry.item
        pos = item.get_position()
        x = self.pocket_selector.get_selection()
        if not self.pocket_selector.is_selected(pos):
            self.pocket_selector.select_item(pos, True)
            self.pocket_selected()

    def icon_click(self, button, function, item):
        pos = item.get_position()
        p = self.pocket_model.get_item(pos)
        match function:
            case "DELETE":

                def callback(response):
                    if response:
                        sql = "DELETE FROM pockets WHERE id=" + str(p.id)
                        cur = self.db.conn.cursor()
                        cur.execute(sql)
                        self.db.conn.commit()
                        # delete components
                        sql = "DELETE FROM pocket_components WHERE parent=" + str(p.id)
                        cur.execute(sql)
                        self.db.conn.commit()

                        i = 0
                        for r in self.pocket_store:
                            if r.id == p.id :
                                self.pocket_store.remove(i)
                                break
                            i += 1

                        #TODO: fire row selection
                        self.pocket_selected()

                CashflexUtils.confirm_delete(callback)
            case _:
                pass

    def f_setup(self, fact, item, v):
        match v["editor"]:
            case "text":
                f = CustomEntry( v["align"], self.pocket_model, item, self.db, "pockets", v["dbcolumn"], v["validate"])
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case "checkbox":
                f = CustomCheckButton( v["align"], self.pocket_model, item, self.db, "pockets", v["dbcolumn"])
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case "types":
                # f = CustomDropDownList(item, v["align"], pocket_model, \
                #                            item, db, "pockets", v["dbcolumn"], CashflexUtils.types_list)
                list_sql = "SELECT  id, name FROM pocket_types ORDER BY sort_order ASC"
                f = CustomDropDownTable(item, v["align"], self.pocket_model, \
                                            item, self.db, "pockets", v["dbcolumn"], list_sql)
                f.onFocus = self.itemFocussed
                item.set_child(f)

            case _:
                item.set_child(Gtk.Label(halign=v["align"]))


    def f_bind(self, fact, item, v):
        f = item.get_child()
        match v["editor"]:
            case "text":
                f.set_text(str(getattr(item.get_item(), v["dbcolumn"])))
            case "checkbox":
                f.set_active(True if getattr(item.get_item(), v["dbcolumn"]) == 1 else False)
            case "types":
                f.set_selected(getattr(item.get_item(), v["dbcolumn"]))
            case _:
                f.set_label(str(getattr(item.get_item(), v["dbcolumn"])))

    def f_setup_icon(self, fact, item, v):
        b = Gtk.Button.new_from_icon_name(v["icon"])
        b.set_tooltip_text(v["tooltip"])
        b.connect("clicked",self.icon_click, v["function"], item)
        item.set_child(b)

    def f_bind_icon(self, fact, item, v):
        pass

