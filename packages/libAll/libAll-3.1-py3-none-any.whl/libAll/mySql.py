import pymysql

class mySql_C():
    soutput = True
    stable = None
    output = None
    cursor = None
    dbc = None

    def connect(self, host, port, user, password, database, output=None, table_name=None):
        try:
            # global dbc
            # global cursor
            if output != None:
                self.soutput = False
            if table_name != None:
                self.stable = table_name

            self.dbc = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.dbc.cursor()
        except Exception as ex:
            if self.soutput == True:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def createTable(self, name_table, table_sql):
        try:
            query_sql = f"CREATE TABLE {name_table} ({table_sql});"
            self.cursor.execute(query_sql)
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def addTable(self, text):
        try:
            self.cursor.execute(text)
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def addElement(self, table_name, names, values):
        try:
            self.cursor.execute(f"INSERT INTO {table_name} ({names}) VALUES ({values})")
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def destroyT(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE {table_name}")
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def destroyE(self, table_name, column_name='id', sources=0):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE {table_name}.{column_name} = '{sources}';")
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def screach(self, table_name, column_name='id', sources=0, columnsc=None):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name}='{sources}';")
            inputp = self.cursor.fetchall()
            if inputp != ():
                if columnsc != None and columnsc in inputp[0]:
                    return inputp[0][columnsc]
                else:
                    return inputp[0]
            else:
                return None
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def printT(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            inputp1 = self.cursor.fetchall()
            if inputp1 != ():
                if len(inputp1) > 1:
                    return inputp1
                else:
                    return inputp1[0]
            else:
                return None
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def change(self, table_name, column_name_value, value, column_name_screach = "id", value_screach = 0):
        self.cursor.execute(f"UPDATE {table_name} SET {column_name_value} = '{value}' WHERE {table_name}.{column_name_screach} = '{value_screach}'")

    def collect_info(self, table_name, column_name):
        self.cursor.execute(f"SELECT {column_name} FROM {table_name}")
        array_fetchall = self.cursor.fetchall()
        array_values165 = []
        for i in array_fetchall:
            array_values165.append(list(i.values()))
        array_values165 = sum(array_values165, [])
        return array_values165


    def do(self, text):
        try:
            self.cursor.execute(text)
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"




    def feturn(self):
        try:
            return self.cursor.fetchall()
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def apply(self):
        try:
            self.dbc.commit()
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def close(self):
        try:
            self.dbc.close()
        except Exception as ex:
            if self.soutput != False:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"
