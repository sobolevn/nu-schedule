#!/usr/bin/python3

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import postgresql

global db
db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')

def jsn():
    tmp = open("deals.txt", "r")

    strg = tmp.read()
    tmp.close()

    x = (json.loads(strg.replace('\n', ' ')))

    for i in range(0, 500):
        try:
            print(x["result"][i]["title_short"], round(x["result"][i]["places"]
                                                       [0]["lat"], 3), "-", round(x["result"][i]["places"][0]["lon"], 3))
        except IndexError:
            print(x["result"][i]["title_short"], "Nan - Nan")
            pass

PORT = 80

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['content-length'])
        self.data_string = self.rfile.read(length)
        #print(length)
        formatd = '{"'+self.data_string.decode('utf-8').replace("&", ', "').replace("=",'":')+'}'
        #formatd = '"'+self.data_string.decode('utf-8')+'"' #this one will give me string
        #print(formatd)
        #print(self.data_string.decode('utf-8'))
        data = json.loads(formatd)
        #print(type(data))
        #print(type(x))
        #try:
        #data = json.loads(x)
        usr = data["usr"]
        num = data["len"] # refactor using array_length() method
        lat = data["lat"]
        lon = data["lon"]
        tru = db.prepare("SELECT * FROM usrs WHERE id=$1")
        upd = db.prepare("UPDATE usrs SET lat[$1] = $2, lon[$1] = $3 where id=$4")
        add = db.prepare("INSERT INTO usrs(id) VALUES ($1)" )
        if (tru(usr) != []):            
            upd(num,lat,lon,usr)
        else:
            #replace with proper registration module and moar parameters  
            add(usr)
            upd(num,lat,lon,usr)
        self.send_response(200)
        self.end_headers()

        #analytisc
        #ADD sort by distance
        src = db.prepare("SELECT id, trim(name) FROM coords WHERE power(power(abs(coords.lat - $1) , 2) + power(abs(coords.lon - $2), 2), 0.5) <= 0.0018")
#replace with dwell-enter-leave system?
#preferences system
        rows = list()
        rows = src(lat,lon)
        print("rows= ",rows)
        lik = db.prepare("SELECT id, trim(name) FROM coords where id=$1") #add preferences (how!?!)
        pref = db.prepare("SELECT pref FROM usrs WHERE usrs.id=$1")

    # does not workin version of preferences
    #    lik = db.prepare("""SELECT id, trim(name) FROM coords WHERE id=$1 
    #                        AND 
    #                        (($1::INT[0] NOT IN ()::INT[])  
    #                        OR 
    #                        (SELECT pref FROM usrs WHERE usrs.id IS NULL) ) """)

        for row in rows:
            print("row= ",row)
            for x in pref(usr):
                if x[0] == None:
                    print(row[0])
                
                #tofix custom prefences
                # else:
                #     try:
                #         x.remove(row[0])
                #         x.append(row[0]) 
                #     except ValueError:
                #         pass       
                                
    def do_GET(self):
        pass


def run():
    print('starting...')

    server_address = ('127.0.0.1', 80)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print('server is up and running')


    try:
        #db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
        db.execute("CREATE TABLE coords (id SERIAL PRIMARY KEY, "
            "fulln CHAR(640), name CHAR(64), addr CHAR(640), dtype CHAR(640), dkind CHAR(640), price INT, b4 INT, econ INT, lat FLOAT, lon FLOAT, isfree BOOLEAN, gotPic BOOLEAN, pic CHAR(640), bigPic CHAR(640) )")
        ins = db.prepare("INSERT INTO coords (fulln, name, addr, dtype, dkind, price, b4, econ, lat, lon, isFree, gotPic, pic, bigPic) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)")
        
        db.execute("CREATE TABLE usrs (usr SERIAL PRIMARY KEY, "
            "id INT, lat FLOAT[], lon FLOAT[], pref INT[] )")

        tmp = open("deals.txt", "r")

        strg = tmp.read()
        tmp.close()

        x = (json.loads(strg.replace('\n', ' ')))

        for i in range(0, 500):
            try:
                ins(
                    x["result"][i]["title"],
                    x["result"][i]["title_short"],
                    x["result"][i]["link"],
                    x["result"][i]["deal_type"],
                    x["result"][i]["deal_kind"],
                    x["result"][i]["price"],
                    x["result"][i]["full_price"],
                    x["result"][i]["economy"], 
                    round(x["result"][i]["places"][0]["lat"], 3), 
                    round(x["result"][i]["places"][0]["lon"], 3),
                    x["result"][i]["is_free"],
                    x["result"][i]["plate_image_exists"],
                    x["result"][i]["image_url"],
                    x["result"][i]["image_url_wide"]
                    )
            except IndexError:
                # ins(x["result"][i]["title_short"], "NAN", "NAN")
                pass
    except postgresql.exceptions.DuplicateTableError:
        print("no need to create")
        pass

    httpd.serve_forever()

if __name__ == '__main__':
    run()