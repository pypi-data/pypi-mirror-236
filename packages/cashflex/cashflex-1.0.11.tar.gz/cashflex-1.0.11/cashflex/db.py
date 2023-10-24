# db.py
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

import os
import sqlite3
import shutil

from utils import CashflexUtils

class CashflexDB:
    def __init__(self):
        # create a database connection to a SQLite database
        self.conn = None
        home = os.path.expanduser('~')
        path = home + "/.cashflex"
        # Check whether the specified path exists or not
        pathExists = os.path.exists(path)
        if not pathExists:
            # Create a new directory because it does not exist
            try:
                os.makedirs(path)
            except Exception as e:
                CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Database Error", "Unable to create .cashflex folder in home folder. " + str(e))
                return

        dbPath = path+"/cashflex.db"
        dbExists = os.path.exists(dbPath)
        if not dbExists:
            try:
                shutil.copy("cashflex/db/cashflex.db", path)
            except Exception as e:
                CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Database Error", "Unable to create database. " + str(e))
                return
            
        try:
            self.conn = sqlite3.connect(dbPath)
        except Exception as e:
            CashflexUtils.alert(CashflexUtils.alert_types.ERROR, "Database Error", "Unable to connect to database." + e)
            return
        


    

