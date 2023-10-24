# forecast.py
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

import sqlite3
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import matplotlib
matplotlib.use('GTK4Agg')  # or 'GTK3Cairo'
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_gtk4agg import (FigureCanvasGTK4Agg as FigureCanvas)
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GObject

from db import CashflexDB
from custom import SimpleDropDownList, SimpleEntry
from utils import CashflexUtils

class SelectActions():
    SELECT_ALL = "A"
    INVERT_SELECTION = "I"
    INCLUDE_TOTAL = "T"
    TOTAL_ONLY = "X"

# simple object with id and name fields
class SelectObject(GObject.Object):
    id = GObject.Property(type=str)
    name = GObject.Property(type=str)
    def __init__(self, id = 0, name = "NO NAME", checked = False):
        GObject.GObject.__init__(self)
        self.id = id
        self.name = name
        self.checked = checked

# Custom dropdown from table with id, name, sort_order fields linked to db table and multi-selectable
class PocketSelectTable(Gtk.ListView):
    __gtype_name__ = "PocketSelectTable"

    def __init__(self, db, table, col):
        Gtk.ListView.__init__(self)
        self.db = db                    # open db connection
        self.col = col                  # db table column
        self.table = table              # table with id, name, sort_order fields

        self.store = Gio.ListStore.new(SelectObject)
        self.set_model(Gtk.MultiSelection.new(model=self.store))
        self.factory = Gtk.SignalListItemFactory.new()
        self.factory.connect("setup", self.setup)
        self.factory.connect("bind", self.bind)
        self.set_factory(self.factory)

        self.refresh()

    def refresh(self):

        self.store.remove_all()

        # build list
        self.store.append(SelectObject(SelectActions.SELECT_ALL, "[Select All]", False))
        self.store.append(SelectObject(SelectActions.INVERT_SELECTION, "[Invert Selection]", False))
        self.store.append(SelectObject(SelectActions.INCLUDE_TOTAL, "[Include Total]", False))
        self.store.append(SelectObject(SelectActions.TOTAL_ONLY, "[Total Only]", False))

        sql = "SELECT  id, name FROM " + self.table + " ORDER BY sort_order, name ASC"

        cur = self.db.conn.cursor()
        rc = cur.execute(sql)

        for v in rc:
            r = SelectObject(*v)
            self.store.append(r)

    # look at state flags to fire focus event
    def stateChanged(self, item, flags):
        if flags & Gtk.StateFlags.FOCUS_WITHIN:
            if self.onFocus != None:
                self.onFocus(self)

    def setup(self, fact, item):
        btn = Gtk.CheckButton()
        btn.connect("toggled", self.cb_toggled)
        item.set_child(btn)

    def bind(self, fact, item):
        pos = item.get_position()
        v = self.store.get_item(pos)
        f = item.get_child()
        setattr(f, "pid", getattr(item.get_item(), "id"))
        f.set_active(v.checked)
        f.set_label(str(getattr(item.get_item(), "name")))


    def cb_toggled(self, btn):
        pid = btn.pid

        # update value in list item
        pos = CashflexUtils.find_row_by_id(pid, self.store)
        list_item = self.store.get_item(pos)
        list_item.checked = btn.get_active() 

        match pid:
            case SelectActions.SELECT_ALL:
                for k in self:
                    cb = k.get_first_child()
                    if cb.pid.isnumeric():
                        cb.set_active(btn.get_active())

            case SelectActions.INVERT_SELECTION:
                for k in self:
                    cb = k.get_first_child()
                    if cb.pid.isnumeric():
                        cb.set_active(not cb.get_active())
            case SelectActions.INCLUDE_TOTAL:
                pass

    def set_selected(self, v):
        pass

def ForecastControls(builder, db, pocket_grid, plot_window):

    def stack_switch(stack, sig):
        if stack.get_visible_child_name() == "forecast-page":

            # get list of selected IDs
            srows = []
            srows[:] = [ r for r in pocket_selector.store ]
            pocket_selector.refresh()

            for r in srows:
                for k in pocket_selector :
                    cb = k.get_first_child()
                    if cb.pid == r.id :
                        # replace value in store
                        pos = CashflexUtils.find_row_by_id(cb.pid, pocket_selector.store)
                        list_item = pocket_selector.store.get_item(pos)
                        list_item.checked = r.checked

                        # show on checkbox
                        cb.handler_block_by_func(pocket_selector.cb_toggled)
                        cb.set_active(r.checked)
                        cb.handler_unblock_by_func(pocket_selector.cb_toggled)

    stack_selector = builder.get_object("main-stack")
    stack_selector.connect("notify", stack_switch)

    pocket_selector = PocketSelectTable(db, "pockets", "name")

    sw = Gtk.Viewport.new()
    sw.set_child(pocket_selector)
    #sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
    #sw.set_overlay_scrolling(False)

    pockets_container = builder.get_object("select-pockets-container")
    pockets_container.set_child(sw)
    pockets_container.connect("notify", pocket_selector.refresh)

    funits = SimpleDropDownList(CashflexUtils.unit_list[1::])
    funits.set_hexpand(True)
    funits.set_hexpand_set(True)
    funits_container = builder.get_object("timescale-container")
    funits_container.append(funits)

    # timescale number

    timescale_number = SimpleEntry(Gtk.Align.END, CashflexUtils.validate_integer)
    timescale_number.set_hexpand(True)
    timescale_number.set_hexpand_set(True)
    time_value_container = builder.get_object("timescale-number-container")
    time_value_container.append(timescale_number)

    # inflation number

    inflation_number = SimpleEntry(Gtk.Align.END, CashflexUtils.validate_amount)
    inflation_number.set_hexpand(True)
    inflation_number.set_hexpand_set(True)
    inflation_number_container = builder.get_object("inflation-number-container")
    inflation_number_container.append(inflation_number)

    # growth number

    #growth_number = SimpleEntry(Gtk.Align.END, CashflexUtils.validate_amount)
    #growth_number.set_hexpand(True)
    #growth_number.set_hexpand_set(True)
    #growth_number_container = builder.get_object("growth-number-container")
    #growth_number_container.append(growth_number)

    # get pocket component rows with outstanding payments at date supplied
    def get_drows(dnow = datetime.today().date(), id_list = None):
        
        sql = "SELECT id, parent, amount, frequency, frequency_unit, start_date, end_date, last_update, type, 0 as 'amount_mx', last_update AS 'new_date' " \
                "FROM pocket_components " \
                "WHERE active = 1 AND start_date <= DATE('NOW') AND end_date > DATE('NOW') AND last_update < DATE('NOW') "

        if id_list != None:
            sql = sql + " AND parent IN (" + ",".join(v.id for v in id_list) + ")" 

        db = CashflexDB()
        db.conn.row_factory = sqlite3.Row
        cur = db.conn.cursor()
        cur.execute(sql)

        rc = cur.fetchall();

        drows = [dict(row) for row in rc]

        for r in drows:
            # calculate interval since last update
            # unit_list = ["TERM", "DAY", "MONTH", "WEEK", "QUARTER", "YEAR"]

            dlast = datetime.strptime(r["last_update"], "%Y-%m-%d").date()
            dstart = datetime.strptime(r["start_date"], "%Y-%m-%d").date()
            dend = datetime.strptime(r["end_date"], "%Y-%m-%d").date()

            amount_mx = 0
            newdate = datetime.today().date()
            dnow = datetime.today().date()

            f = r["frequency"]
            fu = r["frequency_unit"]

            # for first entry last update may not be valid
            # tricky to get first event without repeats until next event
            # simply calculate fake last date

            if dlast < dstart :
                match fu:
                    case "TERM":
                        dlast = dstart
                    case "DAY":
                        dlast = dstart - relativedelta(days=f)
                    case "WEEK":
                        dlast = dstart - relativedelta(days=(f * 7))
                    case "MONTH": 
                        dlast = dstart - relativedelta(months=f)
                    case "QUARTER":          
                        dlast = dstart - relativedelta(months=(f * 3))
                    case "YEAR":
                        dlast = dstart - relativedelta(years=f)

            match fu :
                case "TERM":
                    if dnow == dend :
                        amount_mx = 1
                case "DAY":
                    delta = (dnow - dlast)
                    amount_mx = delta.days // f
                    newdate = dlast + relativedelta(days=(amount_mx * f))
                case "WEEK":
                    delta = (dnow - dlast)
                    amount_mx = delta.days // (f * 7)
                    newdate = dlast + relativedelta(weeks=(amount_mx * f))
                case "MONTH": 
                    rdelta = relativedelta(dnow, dlast)
                    delta = (rdelta.years * 12) + rdelta.months                
                    amount_mx = delta // f
                    newdate = dlast + relativedelta(months=(amount_mx * f))
                case "QUARTER":          
                    rdelta = relativedelta(dnow, dlast)
                    delta = (rdelta.years * 12) + rdelta.months           
                    amount_mx = delta // (f * 3)
                    newdate = dlast + relativedelta(months=(amount_mx * f * 3))
                case "YEAR":           
                    rdelta = relativedelta(dnow, dlast)      
                    amount_mx = delta.years // f
                    newdate = dlast + relativedelta(years=(amount_mx * f))
            
            r["amount_mx"] = amount_mx
            r["new_date"] = datetime.strftime(newdate, "%Y-%m-%d")

        drows[:] = [ r for r in drows if r["amount_mx"] > 0 ] # remove rows with zero amount multiplier
        db.conn.close()
        return drows

    def transactions_clicked(btn):

        def cancel_clicked():
            db.conn.close();
            print("CANCEL")

        def ok_clicked():
            db = CashflexDB()
            db.conn.row_factory = sqlite3.Row
            cur = db.conn.cursor()
            CashflexUtils.log("Processing outstanding transactions")

            for r in drows:
                amount  = r["amount"] * r["amount_mx"]
                cur.execute("UPDATE pockets SET balance = balance + ?  WHERE id = ?", [ amount if r["type"] == "I" else -amount, r["parent"] ])
                db.conn.commit()
                cur.execute("UPDATE pocket_components SET last_update = ? WHERE id = ?", [ r["new_date"], r["id"] ])
                db.conn.commit()
                
                sql = "SELECT pockets.name AS 'pname', pocket_components.name AS 'cname', PRINTF('%0.2f', pockets.balance) AS 'balance' " + \
                            "FROM pocket_components LEFT JOIN pockets ON pocket_components.parent = pockets.id "  + \
                            "WHERE pocket_components.id = " + str(r["id"])
                
                cur.execute(sql)
                r2 = cur.fetchone()

                CashflexUtils.log("Pocket " + r2["pname"] + " balance updated to " + r2["balance"] + " from pocket " + r2["cname"])

            db.conn.close();

            pocket_grid.populate_grid()
            pocket_grid.pocket_selected()

            CashflexUtils.alert(CashflexUtils.alert_types.NONE, "Processing Transactions", "Processing complete!")

        drows = get_drows(datetime.today().date())
        tx = len(drows)

        if tx > 0 :
            CashflexUtils.alert_cancel_ok(CashflexUtils.alert_types.NONE, "Process Transactions", "There" + (" is " if tx == 1 else " are ") + str(tx) + " transaction" + ("s " if tx > 1 else " ") + \
                                          "due to be processed." + " OK to continue?", cancel_clicked, ok_clicked)
        else:
            CashflexUtils.alert(CashflexUtils.alert_types.NONE, "Processing Transactions", "There are no transactions to process.")

    transactions_button = builder.get_object("transactions-button")
    transactions_button.connect("clicked", transactions_clicked)

    def forecast_clicked( btn):

        # get timescale parameters
        n = timescale_number.get_buffer().get_text().strip()
        n = "0" if n == None or n == "" else n 
        if not n.isnumeric():
            CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Forecasting", "Please enter a number for timescale.")
            return
        nint = int(n) + 1
        f = funits.get_selected_item().name

        # get inflation
        nif = inflation_number.get_buffer().get_text().strip()    
        nif = "0" if nif == None or nif == "" else nif   
        if not CashflexUtils.isfloat(nif):
            CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Forecasting", "Please enter a number for inflation or leave blank.")
            return
        inflation = float(nif)

        today = datetime.today().date()
        
        future_date = datetime.today().date()
        dnow = datetime.today().date()
        dateinc = relativedelta(days=1)
        match f:
            case "TERM":
                if (dnow >= dend) and (dlast < dend):
                    amount_mx = 1
            case "DAY":
                dateinc = relativedelta(days=1)
                yearfraction = (1) / (365)
                future_date = dnow + relativedelta(days=nint)
            case "WEEK":
                dateinc = relativedelta(weeks=1)
                yearfraction = (7) / (365)
                future_date = dnow + relativedelta(weeks=nint)
            case "MONTH":    
                dateinc = relativedelta(months=1)    
                yearfraction = (1) / (12)     
                future_date = dnow + relativedelta(months=nint)
            case "QUARTER":           
                dateinc = relativedelta(months=3)      
                yearfraction = (3) / (12)
                future_date = dnow + relativedelta(months=(nint * 3))
            case "YEAR":      
                dateinc = relativedelta(years=1)      
                yearfraction = (1)    
                future_date = dnow + relativedelta(years=nint)
        
        # get list of selected pockets

        srows = []
        srows[:] = [ r for r in pocket_selector.store if ((r.checked > 0) and (r.id.isnumeric())) ]
        pos = CashflexUtils.find_row_by_id(SelectActions.INCLUDE_TOTAL, pocket_selector.store)
        total_checked = pocket_selector.store.get_item(pos).checked  
        pos = CashflexUtils.find_row_by_id(SelectActions.TOTAL_ONLY, pocket_selector.store)
        total_only = pocket_selector.store.get_item(pos).checked

        if len(srows) == 0 and total_checked == False and total_only == False :
            CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Forecasting", "Please select some Pockets to include in the forecast.")
            return
        
        srows.append(SelectObject(SelectActions.INCLUDE_TOTAL, "[Include Total]", total_checked))
        
        # initialise data for plots
        plotdates = []
        plotpockets ={}

        # get base data pockets

        db = CashflexDB()
        db.conn.row_factory = sqlite3.Row
        cur = db.conn.cursor()

        sql = "SELECT id, name, balance, growth FROM pockets"
        cur.execute(sql)
        rc = cur.fetchall();
        pockets = [dict(row) for row in rc]

        for r in rc:
            plotpockets[r["id"]] = []
        plotpockets['T'] = []   # total row

        # get base data pocket_components
        sql = "SELECT id, parent, amount, frequency, frequency_unit, start_date, end_date, last_update, type, " + \
                "0 as 'amount_mx', last_update AS 'new_date', send_to, growth " + \
                "FROM pocket_components " + \
                "WHERE active = 1"

        cur.execute(sql)
        rc = cur.fetchall();
        components = [dict(row) for row in rc]
        
        periods = (0) # loop counter

        while dnow < future_date:
            
            for i, v in enumerate(components):
                dstart = datetime.strptime(v["start_date"], "%Y-%m-%d").date()
                dend = datetime.strptime(v["end_date"], "%Y-%m-%d").date()
                dlast = datetime.strptime(v["last_update"], "%Y-%m-%d").date()

                dthis = dend if dnow > dend else dnow

                fu = v["frequency_unit"]
                f = v["frequency"]

                # allow for growth

                if periods > 0 and v["growth"] != 0 :
                    v["amount"] = (v["amount"]) *(((1) + ((v["growth"] / 100) / periods)) ** (periods * yearfraction))
                    components[i]["amount"] = v["amount"]
                    print("AMOUNT", v["amount"])

                # for first entry last update is may not be valid
                # tricky to get first event without repeats until next event
                # simply calculate fake last date

                if dlast < dstart :
                    match fu:
                        case "TERM":
                            dlast = dstart
                        case "DAY":
                            dlast = dstart - relativedelta(days=f)
                        case "WEEK":
                            dlast = dstart - relativedelta(days=(f * 7))
                        case "MONTH": 
                            dlast = dstart - relativedelta(months=f)
                        case "QUARTER":          
                            dlast = dstart - relativedelta(months=(f * 3))
                        case "YEAR":
                            dlast = dstart - relativedelta(years=f)

                amount_mx = 0
                newdate = dnow

                match fu:
                    case "TERM":
                        if (dthis >= dend) and (dlast < dend):
                            amount_mx = 1
                    case "DAY":
                        delta = (dthis - dlast)
                        amount_mx = delta.days // f
                        newdate = dlast + relativedelta(days=(amount_mx * f))
                    case "WEEK":
                        delta = (dthis - dlast)
                        amount_mx = delta.days // (f * 7)
                        newdate = dlast + relativedelta(weeks=(amount_mx * f))
                    case "MONTH": 
                        rdelta = relativedelta(dthis, dlast)
                        delta = (rdelta.years * 12) + rdelta.months                
                        amount_mx = delta // f
                        newdate = dlast + relativedelta(months=(amount_mx * f))
                    case "QUARTER":          
                        rdelta = relativedelta(dthis, dlast)
                        delta = (rdelta.years * 12) + rdelta.months           
                        amount_mx = delta // (f * 3)
                        newdate = dlast + relativedelta(months=(amount_mx * f * 3))
                    case "YEAR":
                        rdelta = relativedelta(dthis, dlast)      
                        amount_mx = rdelta.years // f
                        newdate = dlast + relativedelta(years=(amount_mx * f))

                if amount_mx > 0:
                    
                    components[i]["last_update"] = datetime.strftime(newdate, "%Y-%m-%d")
                    balup = (amount_mx) * (v["amount"])
                    this_pocket = next((p for p in pockets if p["id"] == v["parent"]), None)

                    # look for target
                    target = 0
                    target_pocket = None
                    if v["send_to"] > 0 :
                        target = v["send_to"]
                        target_pocket = next((p for p in pockets if p["id"] == target), None)

                    # income transfers direct to target
                    # payments deduct and transfer to target

                    if v["type"] == "P" :
                        if this_pocket != None:
                            this_pocket["balance"] -= (balup)
                        if target_pocket != None :
                            target_pocket["balance"] += (balup)   # reverse entry
                    else: # income
                        if target_pocket != None :
                            target_pocket["balance"] += (balup)
                        else:
                            this_pocket["balance"] += (balup)


            # add data points

            plotdates.append(dnow)
            total = (0)
            
            for p in pockets:

                # adjust and inflation 
                if periods > 0:
                    p["balance"] = (p["balance"]) *(((1) + (((p["growth"] - inflation) / 100) / periods)) ** (periods * yearfraction))
                
                # print(periods, p["balance"])

                pid = p["id"]
                plotpockets[pid].append(p["balance"])
                total += p["balance"]

            plotpockets['T'].append(total)

            dnow = dnow + dateinc
            periods += 1
            # end of loop
        
        # to show stairs add final date
        plotdates.append(dnow + dateinc)

        t = plot_window.get_child()
        if t:
            plot_window.set_child(None)
        plot = ShowPlot(pockets, plotdates, plotpockets, total_checked, srows, total_only)
        plot_window.set_child(plot)

    forecast_button = builder.get_object("run-forecast-button")
    forecast_button.connect("clicked", forecast_clicked)

class ShowPlot(Gtk.Box):
    __gtype_name__ = "ShowPlot"
    def find_pocket_by_id(self, pid):
        for p in self.pockets:
            if p["id"] == pid:
                return p
        return None

    def __init__(self, pockets = None, plotdates = None, plotpockets = None, total_checked = False, srows = None, total_only = False):
        Gtk.Box.__init__(self)
        self.pockets = pockets
        self.ax = None
        self.fig = None
        if plotdates != None:

            self.fig, self.ax = plt.subplots( )
            for p in plotpockets:

                # see if plot selected
                
                if any(r.id == str(p) for r in srows) :
                    if (p == SelectActions.INCLUDE_TOTAL) and not (total_checked or total_only):
                        continue

                    label = "Empty"
                    if p == SelectActions.INCLUDE_TOTAL :
                        label = "Total"
                    else :
                        pop = self.find_pocket_by_id(p)
                        label = pop["name"]

                    if  total_only and (p != SelectActions.INCLUDE_TOTAL):
                        pass
                    else:
                        self.ax.stairs(plotpockets[p] , plotdates, label = label, baseline = None)

            
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Balance")
            self.ax.legend()
            self.ax.grid(which='major', color='#cccccc', linewidth=0.5)
            self.ax.grid(which='minor', color='#dddddd', linestyle='--', linewidth=0.5)
            self.ax.minorticks_on()
            self.ax.tick_params(which='minor', bottom=False, left=False)
            # self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1)
        else:
            self.fig = Figure(figsize=(5, 4), dpi=100)

        self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
        self.canvas.set_size_request(800, 800)
        self.append(self.canvas)
        

