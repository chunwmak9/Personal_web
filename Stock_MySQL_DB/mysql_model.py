#Author: Benny Mak
#Github: r93042004@gmail.com
#https://flaviocopes.com/mysql-how-to-install/
#https://www.guru99.com/python-mysql-example.html

import mysql.connector
import random 
import pandas 
import time

# db_connection = mysql.connector.connect(
# host = "localhost",
# user = "root",
# database='test',auth_plugin='mysql_native_password'
# ) #passwd = "password" =>NO PASSWORD


# print(db_connection)

# db_cursor = db_connection.cursor()
# db_cursor.execute("SHOW TABLES;")

# for table in db_cursor:
#     print(table)


# #Data INSERT
# # for _ in range(100):
# #     insert_data = "INSERT INTO random_number (randn) VALUES ({})".format(random.randint(0,10000))
# #     db_cursor.execute(insert_data)
# # db_connection.commit()
# # print(db_cursor.rowcount,"Record Inserted")

# db_cursor.execute("SELECT * FROM random_number")
# for line in db_cursor:
#     print(line)


#Create 
class DataModel:
    def __init__(self,database = "test"):
        self.db_connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            database =database ,auth_plugin ="mysql_native_password"
        )
        self.db_cursor = self.db_connection.cursor()
        print(str(self.db_connection),"at \"{}\" database".format(database))

    #Function: Execute SQL commands using Python syntax
    #Output: Return mysql query results
    def EXECUTE(self,command):
        output = []
        self.db_cursor.execute(command)
        for info in self.db_cursor:
            print(info)
            output.append(info)
        return output
    
    #Function: To create a table in database with pandas dataframe
    #Input: Pandas Dataframe
    #Output: Create a specific table with the table name 
    def CREATE_TABLE(self,tablename,data):
        #indexes = data.index.values
        columns = data.columns.values[:]
        s = "CREATE TABLE {}(".format(tablename)
        #ID starting from 1
        m = "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        count = 0
        m_columns = [c for c in columns]
        for c in columns:
            if len(c.split()) >1:
                columns[count] = "".join(c.split())
                c = columns[count]
            try:
                SUM = sum(data[m_columns[count]])
                m+= "{} FLOAT NOT NULL,".format(str(c))
            except:
                m+= "{} VARCHAR(30) NOT NULL,".format(str(c))
            count+=1
        m = m.rstrip(",")
        e = ")"
        create_query = s + m + e
        print("Creation query: ",create_query)
        self.EXECUTE(create_query)
        print("Table creation finished!")
        for row in range(len(data)):
            table = "{}(".format(tablename)
            for c in columns:
                table += "{},".format(str(c).replace("\'","").replace("\"",""))
            table = table.rstrip(",")
            table+=") "
            values = [] 
            #values.append(indexes[row])
            for c in m_columns:
                values.append(data.iloc[row][c])
            val = "VALUES{}".format("("+str(values).lstrip("[").rstrip("]")+")")
            insert_query = "INSERT INTO "+table+val
            print("Data insertion query: ",insert_query)
            self.EXECUTE(insert_query)
        self.db_connection.commit()
        print("Table creation finished!")
        
    #Function: Delete entire table
    def DELETE(self,tablename):
        try:
            self.EXECUTE("DROP TABLE {}".format(tablename))
            print("Table {} is deleted!".format(tablename))
        except:
            print("Table {} does not exist!".format(tablename))

    #Function: Close the database connection.
    def CLOSE(self):
        self.db_cursor.close()
        self.db_connection.close()
    
    #Function: Retrieve data from the column
    def RETRIEVE(self,tablename,*columns):
        DICT = {}
        storage = []
        try:
            if not columns:
                #Entire table will return.
                for line in self.EXECUTE("SHOW COLUMNS FROM {}".format(tablename)):
                    storage = []
                    c = line[0]
                    retrieve_query = "SELECT {} FROM {}".format(c,tablename)
                    print(retrieve_query)
                    for item in self.EXECUTE(retrieve_query):
                        storage.append(item)
                    DICT[c] = storage 
                return DICT
            else:
                for c in columns:
                    storage = []
                    retrieve_query = "SELECT {} FROM {}".format(c,tablename)
                    print(retrieve_query)
                    for item in self.EXECUTE(retrieve_query):
                        storage.append(item)
                    DICT[c] = storage 
                return DICT
            #print(self.EXECUTE("SHOW COLUMNS FROM {}".format(tablename)))    
        except:
            print("Your request does not exist.")

    #Function: Update the data row information
    def UPDATE(self,tablename,*columns,values:list):
        try:
            count = 0
            for c in columns:
                update_query = "UPDATE {} SET {} = {}".format(tablename,c,values[count])
                count+=1
                print(update_query)
                self.EXECUTE(update_query)
            self.db_connection.commit()
            print("Updated successfully.")
        except:
            print("Your request does not exist.")


        


def stock_data(name):
    import yfinance as yf
    data = yf.Ticker(name)
    data = data.history()
    return data

if __name__== "__main__":
    dm = DataModel()
    #print(dm.EXECUTE("SELECT * FROM random_number LIMIT 1"))
    stock_name = "NNDM"
    dm.DELETE(stock_name)
    stock = stock_data("{}".format(stock_name))
    dm.CREATE_TABLE(stock_name,stock)
    print(dm.RETRIEVE(stock_name,"id"))

    #print(dm.EXECUTE("SELECT * FROM {}".format(stock_name)))
    dm.CLOSE()
    # print(type(stock))
    # print(stock.columns.values)
    # for i in range(len(stock)):
    #     print(stock.iloc[i]["Open"])
    # print(len(stock))

#MySQL syntax:
"""
SELECT * FROM SOS WHERE id REGEXP '^[^2]';
SELECT * FROM SOS WHERE id NOT BETWEEN 5 AND 15 AND VOLUME >= 4154600;
SELECT id,CONCAT(Open,High,Low,Close) as stock_info FROM SOS ;
SELECT * FROM SOS WHERE SOS.Open >0.4;

#INNER, LEFT ,RIGHT JOIN IN MySQL (*No FULL OUTER JOIN)
SELECT SOS.id,SOS.Open,random_number.randn FROM SOS INNER JOIN random_number ORDER BY SOS.id;
select Dividends from SOS UNION ALL select Dividends from NNDM;
#Create a backup table in database
create table nndm_backup (id INT,stock_price INT);
INSERT INTO nndm_backup SELECT id,Open FROM NNDM;
ALTER TABLE NNDM MODIFY Open int NULL;
insert into NNDM (id,Open,High,Low,Close,Volume,Dividends,StockSplits) values (23,0,16.5,0,5.0,0,0,0);

create view id_avg_nndm as select count(id) from id_view inner join nndm_avg_price;

"""



