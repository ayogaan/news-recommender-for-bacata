import numpy as np
import mysql.connector
symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
berita = open("ini.txt", "r")

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="fanfanfan",
  database="news"
)

if db.is_connected():
    print("Berhasil terhubung ke database")

def dataInsert(a,b): 

    cursor = db.cursor()
    sql = "INSERT INTO dataset (label, word) VALUES (%s, %s)"
    val = (a, b)
    cursor.execute(sql, val)
    db.commit()
    print("{} data ditambahkan".format(cursor.rowcount))


for line in berita:
    toStore = "["
    for i in symbols:
         line = line.replace(i, '')
    berita = line.split()
    
    if len(berita)>0:
        category=berita[0]
    del berita[0]    
    
    for y in berita:
        toStore+="'"+y+"',"
    l = len(toStore)
    toStore = toStore[:l-1]
    toStore+="]"
    if len(toStore) > 3:
        dataInsert(category, toStore)
    
