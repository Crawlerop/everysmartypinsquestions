# https://github.com/komoot/staticmap
# https://api.mapbox.com/styles/v1/user12435235124125235824592457/ckaksz0ab1wbf1iqvfbm1g0l8/tiles/256/0/0/0@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import staticmap
import json
from PIL import Image, ImageTk
import binascii
import io
import os, glob
import datetime
import random
import copy
import sys
import csv
from types import SimpleNamespace

lastsave = SimpleNamespace(prev=None)

def checkpos(s):
    if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-', ';', ",", " "]:
        return True
    return False

def checkrange(s):
    if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
        return True
    return False

def checkzoom(s):
    if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    return False

def checkmp(s):
    if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ".", ",", "-", " "]:
        return True
    return False

def checkmpz(s):
    if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ".", ",", "-", " ", "z"]:
        return True
    return False

def checkpossibility(s):
    if s in ['1', '2', '3', '4', '5']:
        return True
    return False

def main():

    template = ''' 
    <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                
                <link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />

                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
                <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js" integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew==" crossorigin=""></script>
                <style>
                    body {
                        padding: 0;
                        margin: 0;
                    }
                    html, body, #mapid {
                        height: 100%;
                        width: 100%;
                    }
                </style>
                
            </head>
            <body>
                <div id="mapid"></div>
                <script>
                    var data = L.layerGroup()
                
                    m = L.marker([([ANSLAT]), ([ANSLNG])])
                        
                    m.on('click', function(e){
                        mymap.setView([([ANSLAT]), ([ANSLNG])], 19); 
                    })
                        
                    m.bindPopup("<b>([BQUESTION])</b><br />The answer is: ([BANSWER])<br /><br /> Hint: ([BHINT])").addTo(data)
                        
                    L.polygon([[([NELAT]), ([NELNG])], [([SWLAT]),([NELNG])], [([SWLAT]),([SWLNG])], [([NELAT]),([SWLNG])]]).bindPopup("Region boundary").addTo(data)

                    c = L.circle([([ANSLAT]), ([ANSLNG])], ([MINDIST]), {color: 'green', fillColor: '#0f0', fillOpacity: 0.3})
                    c.on('click', function(e){
                        mymap.setView([([ANSLAT]), ([ANSLNG])], 15);
                    })

                    c.bindPopup("Answer range").addTo(data)

                    mapboxattr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' + 'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'

                    gmapsattr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' + 'Imagery © <a href="https://maps.google.com/">Google Maps</a>'

                    normal = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    satellite = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'user12435235124125235824592457/ckanekpxi1o3y1ipkm8tl6v3i',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    gmapsnormal = L.tileLayer('https://www.google.com/maps/vt?pb=!1m4!1m3!1i{z}!2i{x}!3i{y}!2m2!2sm!3i504221335!3m7!2sen-US!5i1105!12m4!1i68!2m2!1sset!2sTerrain!5m1!5f4.0!23i1358902', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    gmapssatellite = L.tileLayer('https://mt{s}.googleapis.com/vt?lyrs=y&hl=en-US&x={x}&y={y}&z={z}', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckanekpxi1o3y1ipkm8tl6v3i',
                        tileSize: 256,
                        zoomOffset: 0,
                        subdomains: ["0", "1", "2", "3"]
                    })

                    var mymap = L.map('mapid', {
                        center: [0.0, 0.0],
                        zoom: 15,
                        layers: [normal, data]
                    })

                    var l1 = L.latLng(([NELAT]), ([NELNG]))
                    var l2 = L.latLng(([SWLAT]), ([SWLNG]))
                    bounds = L.latLngBounds(l1, l2)
                    mymap.panTo(bounds.getCenter())
                    mymap.fitBounds(bounds)
                    mymap.setZoom(mymap.getZoom() + 1)

                    var layernames = {
                        "Mapbox Normal": normal,
                        "Google Maps Normal": gmapsnormal,
                        "Mapbox Satellite": satellite,
                        "Google Maps Satellite": gmapssatellite
                    }
                    
                    var dataset = {
                        "Smarty Pins data": data
                    }
                
                    layers = L.control.layers(layernames, dataset)
                    layers.addTo(mymap)		
                </script>
            </body>
        </html>
    '''

    pinicon = binascii.a2b_base64('''
    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
    ''')
    
    root = tk.Tk()
    def tick():
        root.after(1, tick)
    frmb = tk.Frame()
    frmb2 = tk.Frame()
    menu = tk.Menu(root)
    filemenu = tk.Menu(menu, tearoff=0)
    scrollbar = tk.Scrollbar(frmb)
    scrollbar.pack( side = tk.RIGHT, fill = tk.Y, expand="YES")
    frm1 = tk.Listbox(frmb, yscrollcommand=scrollbar.set, bd=2, height=32,width=50)
    frm1.pack(side=tk.LEFT, fill=tk.BOTH, expand="YES")
    frmb.grid(row=0, column=0)
    scrollbar.config(command = frm1.yview) 

    startpicture = Image.new("RGB", (400,400), "white")
    starttk = ImageTk.PhotoImage(startpicture)
    lbl = tk.Label(frmb2, image=starttk)
    lbl.photo = starttk
    lbl.pack(side=tk.TOP)

    fields = tk.Frame(frmb2)
    fields.pack(side=tk.LEFT)

    tk.Label(fields, text="Question").grid(row=0)
    question = tk.Entry(fields, width=15)
    question.grid(row=0, column=1)

    tk.Label(fields, text="Hint").grid(row=0, column=2)
    hint = tk.Entry(fields, width=15)
    hint.grid(row=0, column=3)
    
    #checkcmd = (root.register(checkpos), "%S")
    #checkcmd2 = (root.register(checkrange), "%S")
    #checkcmd3 = (root.register(checkmpz), "%S")
    #checkcmd4 = (root.register(checkmp), "%S")
    #checkcmd5 = (root.register(checkpossibility), "%S")

    tk.Label(fields, text="Region").grid(row=1)
    bbox = tk.Entry(fields, width=15)
    bbox.grid(row=1, column=1)

    tk.Label(fields, text="MinRange").grid(row=1, column=2)
    minrange = tk.Entry(fields, width=15)
    minrange.grid(row=1, column=3)

    tk.Label(fields, text="QuestionFocus").grid(row=3)
    focus = tk.Entry(fields, width=15)
    focus.grid(row=3, column=1)

    tk.Label(fields, text="OnlyFor").grid(row=3, column=2)
    enabledfor = tk.Entry(fields, width=15)
    enabledfor.grid(row=3, column=3)

    diftext = tk.StringVar()

    def character_limit(entry_text):
        if len(entry_text.get()) > 1:
            entry_text.set(entry_text.get()[0])

    diftext.trace("w", lambda *args: character_limit(diftext))

    tk.Label(fields, text="Difficulty").grid(row=4)
    difficulty = tk.Entry(fields, width=1, textvariable=diftext)
    difficulty.grid(row=4, column=1, sticky=tk.W)

    tk.Label(fields, text="Answer").grid(row=5)
    answer = tk.Entry(fields, width=15, validate='key')
    answer.grid(row=5, column=1)

    tk.Label(fields, text="AnswerPos").grid(row=5, column=2)
    answerpos = tk.Entry(fields, width=15)
    answerpos.grid(row=5, column=3)

    tk.Label(fields, text="Categories").grid(row=6, column=0)
    categories = tk.Entry(fields, width=15)
    categories.grid(row=6, column=1)

    tk.Label(fields, text="ID").grid(row=6, column=2)
    itemid = tk.Entry(fields, width=15)
    itemid.grid(row=6, column=3)

    '''
    def toggle(var):
        var.set(not var.get())
    '''
    isstandard = tk.IntVar()
    

    tk.Label(fields, text="Standard").grid(row=4, column=2, sticky=tk.W)
    standard = tk.Checkbutton(fields, activeforeground='white',selectcolor="black", variable=isstandard)
    standard.grid(row=4, column=3, sticky=tk.W)

    tk.Label(fields, text="MapsZoom").grid(row=7, column=0)
    zoom = tk.Entry(fields, width=2)
    zoom.grid(row=7, column=1)

    tk.Label(fields, text="ShortName").grid(row=7, column=2)
    shortname = tk.Entry(fields, width=15)
    shortname.grid(row=7, column=3)
    '''
    lastvar = isstandard

    def refetch():
        nonlocal standard, lastvar
        if lastvar != isstandard:
            lastvar = isstandard
            standard.grid_forget()
            standard.grid(row=4, column=3, sticky=tk.W)
        standard.after(1, refetch)

    standard.after(1, refetch)
    '''

    frmb2.grid(row=0, column=1)

    lst = []
    lst2 = {"a": []}
    last = -1

    stopped = False

    def replace(ob, text):
        ob.delete(0, tk.END)
        ob.insert(0, text)

    zoomlastpos = None

    rnd = None

    def updatelst(nof):
        nonlocal lst2, pinicon, lbl, last, lst, question, hint, bbox, minrange, focus, enabledfor, difficulty, standard, answer, answerpos, categories, itemid, zoom, zoomlastpos, rnd, shortname
        if lst == []: return False
        
        if last == -1 or last != nof:
            last = nof
            replace(question, lst[nof]["title"])
            replace(hint, lst[nof]["hint"])
            replace(bbox, str(lst[nof]["region"]["northeast"]["lat"]) + "," + str(lst[nof]["region"]["northeast"]["lng"]) + ";" + str(lst[nof]["region"]["southwest"]["lat"]) + "," + str(lst[nof]["region"]["southwest"]["lng"]))
            replace(minrange, str(lst[nof]["answer"]["minimum_distance"]))
            replace(focus, str(lst[nof]["region"]["focus"]["lat"]) + "," + str(lst[nof]["region"]["focus"]["lng"]) + "," + str(lst[nof]["region"]["zoom"]) + "z")
            replace(enabledfor, ";".join(lst[nof]["locales"]))
            replace(difficulty, str(lst[nof]["difficulty"]))
            replace(answerpos, str(lst[nof]["answer"]["location"]["lat"]) + "," + str(lst[nof]["answer"]["location"]["lng"]))

            if lst[nof]["standard"]:
                standard.select()
            else:
                standard.deselect()

            replace(answer, lst[nof]["answer"]["title"])
            r = []
            for category in lst[nof]["categories"]:
                r.append(str(category))
            replace(categories, ";".join(r))
            replace(itemid, int(lst[nof]["id"]))
            replace(zoom, str(17))

            dxp = ("-".join(lst[nof]["title"].split()[:15]))[-24:].lower().replace("'", "-") + "-tht-" + ("-".join(lst[nof]["hint"].split()[:24]))[-24:].lower().replace("'", "-")
            iout = []

            for char in dxp:
                if char in allowed:
                    iout.append(char)

            replace(shortname, "".join(iout))            
            #print(f'''Update! {lst[nof]["title"]}''')

        if json.dumps({"a": [lst[nof]["answer"]["location"]["lng"], lst[nof]["answer"]["location"]["lat"]]}) != json.dumps(lst2) or zoom.get() != zoomlastpos:
            if json.dumps({"a": [lst[nof]["answer"]["location"]["lng"], lst[nof]["answer"]["location"]["lat"]]}) != json.dumps(lst2):
                lst2 = {"a": [lst[nof]["answer"]["location"]["lng"], lst[nof]["answer"]["location"]["lat"]]}
                #rnd = staticmap.StaticMap(400,400, tile_size=512, url_template="https://api.mapbox.com/styles/v1/user12435235124125235824592457/ckaksz0ab1wbf1iqvfbm1g0l8/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw")
                rnd = staticmap.StaticMap(400, 400, tile_size=512, url_template="https://api.mapbox.com/styles/v1/user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw")
                ha = io.BytesIO(pinicon)
                hsk = io.BytesIO()
                himg = Image.open(ha)
                himg.thumbnail((himg.width/50,himg.height/50))
                himg.save(hsk, "png")
                hsk.seek(0)

                pina = staticmap.IconMarker((lst[nof]["answer"]["location"]["lng"], lst[nof]["answer"]["location"]["lat"]), hsk, 200, 200)

                rnd.add_marker(pina)

            outp = rnd.render(zoom=int(zoom.get()))
            zoomlastpos = zoom.get()
            outptk = ImageTk.PhotoImage(outp)

            lbl.config(image=outptk)
            lbl.photo = outptk

        return True

    def doupdate():
        nonlocal lst, frm1, question, hint, bbox, minrange, focus, enabledfor, difficulty, standard, answer, answerpos, isstandard, itemid, stopped
        #if stopped: print("Stopped now"); return
        try:
            if not updatelst(frm1.index(tk.ACTIVE)): root.after(1, doupdate); return
            lat, lng = tuple(answerpos.get().split(","))
            lst[frm1.index(tk.ACTIVE)]["answer"]["location"]["lat"] = float(lat)
            lst[frm1.index(tk.ACTIVE)]["answer"]["location"]["lng"] = float(lng)
            lst[frm1.index(tk.ACTIVE)]["title"] = question.get()
            #s = lst[frm1.index(tk.ACTIVE)]["slug"]
            lst[frm1.index(tk.ACTIVE)]["slug"] = "-".join(question.get().split()[:6]).lower().replace("'", "-")
            #d = lst[frm1.index(tk.ACTIVE)]["slug"]
            #if d != s:
                #print(f"{s} -> {d}")
            lst[frm1.index(tk.ACTIVE)]["hint"] = hint.get()
            bboxne, bboxsw = tuple(bbox.get().split(";"))
            bboxnepos = tuple(bboxne.split(","))
            bboxswpos = tuple(bboxsw.split(","))
            lst[frm1.index(tk.ACTIVE)]["region"]["northeast"]["lat"] = float(bboxnepos[0])
            lst[frm1.index(tk.ACTIVE)]["region"]["northeast"]["lng"] = float(bboxnepos[1])
            lst[frm1.index(tk.ACTIVE)]["region"]["southwest"]["lat"] = float(bboxswpos[0])
            lst[frm1.index(tk.ACTIVE)]["region"]["southwest"]["lng"] = float(bboxswpos[1])
            lst[frm1.index(tk.ACTIVE)]["answer"]["minimum_distance"] = float(minrange.get())
            focuslat, focuslng, focuszoom = tuple(focus.get().split(","))
            lst[frm1.index(tk.ACTIVE)]["region"]["focus"]["lat"] = float(focuslat)
            lst[frm1.index(tk.ACTIVE)]["region"]["focus"]["lng"] = float(focuslng)
            lst[frm1.index(tk.ACTIVE)]["region"]["zoom"] = int(focuszoom[:-1])
            lst[frm1.index(tk.ACTIVE)]["locales"] = enabledfor.get().split(";")
            lst[frm1.index(tk.ACTIVE)]["difficulty"] = int(difficulty.get())
            lst[frm1.index(tk.ACTIVE)]["standard"] = bool(isstandard.get())
            lst[frm1.index(tk.ACTIVE)]["answer"]["title"] = answer.get()
            c = categories.get().split(";")
            f = []
            for ct in c:
                f.append(int(ct))
            lst[frm1.index(tk.ACTIVE)]["categories"] = f
            lst[frm1.index(tk.ACTIVE)]["id"] = int(itemid.get())
        except Exception:
            #print(f"Error: {e}")
            pass
        root.after(1, doupdate)


    root.after(1, doupdate)

    lastname = ""

    def savefile():
        nonlocal lst, lastname
        if lst == []: return False
        if not lastname:
            fnd = tk.filedialog.asksaveasfilename(title="Save Smarty Pins question file.", filetypes=(("Smarty Pins JSON file", "*.json"),))
        else:
            fnd = lastname
        if not fnd: return False
        try:
            open(fnd, "w").write(json.dumps({"items": lst, "count": len(lst)}))
        except:
            messagebox.showerror(message=f"Cannot write {fnd}")
            return False
        lastsave.prev = copy.deepcopy({"a": lst})
        return True

    def savefileas():
        nonlocal lst, lastname
        if lst == []: return False
        fnd = tk.filedialog.asksaveasfilename(title="Save Smarty Pins question file.", filetypes=(("Smarty Pins JSON file", "*.json"),))
        if not fnd: return False
        try:
            open(fnd, "w").write(json.dumps({"items": lst, "count": len(lst)}))
        except:
            messagebox.showerror(message=f"Cannot write {fnd}")
            return False
        lastsave.prev = copy.deepcopy({"a": lst})
        lastname = fnd
        return True

    def checksave():
        nonlocal lst
        i = 0
        for idp in lst:
            lastsave.prev["a"][i]["id"] = idp["id"]
            i += 1
            if i >= len(lastsave.prev["a"]): break
        '''
        print("s")
        print()
        print({"a": lst})
        print()
        print(lastsave.prev)
        print()
        '''
        if lastsave.prev != None and json.dumps({"a": lst}) != json.dumps(lastsave.prev):
            res = tk.messagebox.askyesnocancel("Unsaved changes", "There are unsaved changes to this file, clicking no will result loss.", icon="warning")
            if res == None:
                return False
            elif res == True:
                if not savefile(): return False
        elif lastsave.prev != None:
            lst = lastsave.prev["a"]
            lastsave.prev["a"] = lst
        return True

    def newfile():
        nonlocal lst, frm1, last, stopped, root
        if not checksave(): return
        stopped = True
        lst = []
        lastsave.prev = None
        frm1.delete(0, tk.END)
        last = -1
        lst.append({
            "id":random.randint(100000000000000,1000000000000000),
            "published":datetime.datetime.now().replace(microsecond=0).isoformat() + "Z",
            "locales":[
                "en-US",
                "en-GB",
                "en-AU",
            ],
            "categories":[
                0
            ],
            "standard":True,
            "title":"New Question 1",
            "slug":"new-question-1",
            "hint":"New Hint 1",
            "difficulty":1,
            "region":{
                "northeast":{
                    "lat":180.0,
                    "lng":180.0
                },
                "southwest":{
                    "lat":-180.0,
                    "lng":-180.0
                },
                "focus":{
                    "lat":0.0,
                    "lng":0.0
                },
                "zoom":2
            },
            "answer":{
                "title":"New Answer 1",
                "location":{
                    "lat":0.0,
                    "lng":0.0
                },
                "minimum_distance":1e+45
            }
        })
        lastsave.prev = copy.deepcopy({"a": lst})
        '''
        print()
        print({"a": lst})
        print()
        print(lastsave.prev)
        print()
        '''
        frm1.insert(tk.END, lst[0]["title"])
        frm1.see(0)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(0, 0)
        frm1.event_generate("<<ListboxSelect>>")
        #frm1.activate(0)

        updatelst(0)
        last = 0
        root.after(300, opendelay)
        #print(lastsave)

    def newquestion():
        nonlocal lst, frm1
        if lst == []: return
        lst.append({
            "id":random.randint(100000000000000,1000000000000000),
            "published":datetime.datetime.now().replace(microsecond=0).isoformat() + "Z",
            "locales":[
                "en-US",
                "en-GB",
                "en-AU",
            ],
            "categories":[
                0
            ],
            "standard":True,
            "title":f"New Question {len(lst)+1}",
            "slug":f"new-question-{len(lst)+1}",
            "hint":f"New Hint {len(lst)+1}",
            "difficulty":1,
            "region":{
                "northeast":{
                    "lat":180.0,
                    "lng":180.0
                },
                "southwest":{
                    "lat":-180.0,
                    "lng":-180.0
                },
                "focus":{
                    "lat":0,
                    "lng":0
                },
                "zoom":2
            },
            "answer":{
                "title":f"New Answer {len(lst)+1}",
                "location":{
                    "lat":0,
                    "lng":0
                },
                "minimum_distance":1e+45
            }
        })
        frm1.insert(tk.END, lst[-1]["title"])

    def opendelay():
        nonlocal stopped
        stopped = False
        root.after(1, doupdate)

    def openfile(filename=None):
        nonlocal lst, frm1, root, stopped, last, lastname
        global lastsave
        if not checksave(): return
        stopped = True
        if filename:
            fnd = filename
        else:
            fnd = tk.filedialog.askopenfilename(title="Open Smarty Pins question file.", filetypes=(("Smarty Pins JSON file", "*.json"),))
            if not fnd: root.after(300, opendelay); return
        lst = []
        lastsave.prev = None
        try:
            dta = json.loads(open(fnd, "r").read())
        except:
            messagebox.showerror(message=f"Cannot load {fnd}")
            root.after(300, opendelay)
            return


        if int(dta["count"]) != len(dta["items"]):
            messagebox.showerror(message="Truncated file")
            root.after(300, opendelay)
            return

        if dta["items"] == []:
            messagebox.showerror(message="There's no questions on this file")
            root.after(300, opendelay)
            return

        lst = dta["items"]
        lastsave.prev = copy.deepcopy({"a": lst})

        frm1.delete(0, tk.END)
        last = -1

        for item in dta["items"]:
            frm1.insert(tk.END, item["title"])

        frm1.see(0)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(0, 0)
        frm1.event_generate("<<ListboxSelect>>")
        #frm1.activate(0)
        updatelst(0)
        last = 0
        lastname = fnd

        root.after(300, opendelay)

    def exportitem():
        nonlocal lst, frm1, template
        if lst == []: return
        if not checksave(): return
        idx = frm1.index(tk.ACTIVE)
        fnd = tk.filedialog.asksaveasfilename(title="Save Smarty Pins HTML item file.", filetypes=(("HTML file", "*.html"),))
        if not fnd: return
        item = lst[idx]
        #print(item)
        lat = item["answer"]["location"]["lat"]
        lng = item["answer"]["location"]["lng"]
        ans = item["answer"]["title"].replace("\"", "\\\"")
        qus = item["title"].replace("\"", "\\\"")
        hnt = item["hint"].replace("\"", "\\\"")
        radius = item["answer"]["minimum_distance"]
        nelat = item["region"]["northeast"]["lat"]
        nelng = item["region"]["northeast"]["lng"]
        swlat = item["region"]["southwest"]["lat"]
        swlng = item["region"]["southwest"]["lng"]
        '''
        focuslat = item["region"]["focus"]["lat"]
        focuslng = item["region"]["focus"]["lng"]
        focuszoom = item["region"]["zoom"]
        '''
        xpr1 = qus.encode('unicode-escape').decode('ascii').replace("\\\\\"", "\\\"")
        xpr2 = ans.encode('unicode-escape').decode('ascii').replace("\\\\\"", "\\\"")
        standard = item["standard"]
        stdtext = "Non-standard question"
        if standard:
            stdtext = "Standard question"
        output = template
        output = output.replace("([ANSLAT])", str(lat))
        output = output.replace("([ANSLNG])", str(lng))
        output = output.replace("([BQUESTION])", xpr1)
        output = output.replace("([BANSWER])",xpr2)
        output = output.replace("([BHINT])", hnt + "<br /><br /> " + stdtext + "<br /><br /> Appears in region: " + ",".join(item["locales"]) + f"<br /><br /><a href=\\\"https://virtualglobetrotting.com/ll/{lat},{lng}/\\\">Look on VirtualGlobeTrotting</a>")
        output = output.replace("([NELAT])", str(nelat))
        output = output.replace("([NELNG])", str(nelng))
        output = output.replace("([SWLAT])", str(swlat))
        output = output.replace("([SWLNG])", str(swlng))
        output = output.replace("([MINDIST])", str(radius))
        open(fnd, "w").write(output)

    allowed = []
    for r in range(ord("a"), ord("z")+1):
        allowed.append(chr(r))
    for r in range(ord("0"), ord("9")+1):
        allowed.append(chr(r))
    allowed.append("-")

    def exportitems():
        nonlocal lst, frm1, allowed
        if lst == []: return
        if not checksave(): return
        #idx = frm1.index(tk.ACTIVE)
        fnd = tk.filedialog.askdirectory(title="Save Smarty Pins HTML item files.")
        if not fnd: return
        if not os.path.exists(fnd): os.mkdir(fnd)

        flist = glob.glob(os.path.join(fnd, "*.*"))
        for f in flist:
            os.remove(f)

        isd = 0

        for item in lst:
            try:
                #print(item)
                lat = item["answer"]["location"]["lat"]
                lng = item["answer"]["location"]["lng"]
                ans = item["answer"]["title"].replace("\"", "\\\"")
                qus = item["title"].replace("\"", "\\\"")
                hnt = item["hint"].replace("\"", "\\\"")
                radius = item["answer"]["minimum_distance"]
                nelat = item["region"]["northeast"]["lat"]
                nelng = item["region"]["northeast"]["lng"]
                swlat = item["region"]["southwest"]["lat"]
                swlng = item["region"]["southwest"]["lng"]
                '''
                focuslat = item["region"]["focus"]["lat"]
                focuslng = item["region"]["focus"]["lng"]
                focuszoom = item["region"]["zoom"]
                '''
                xpr1 = qus.encode('unicode-escape').decode('ascii').replace("\\\\\"", "\\\"")
                xpr2 = ans.encode('unicode-escape').decode('ascii').replace("\\\\\"", "\\\"")

                standard = item["standard"]
                stdtext = "Non-standard question"
                if standard:
                    stdtext = "Standard question"
                output = template
                output = output.replace("([ANSLAT])", str(lat))
                output = output.replace("([ANSLNG])", str(lng))
                output = output.replace("([BQUESTION])", xpr1)
                output = output.replace("([BANSWER])",xpr2)
                output = output.replace("([BHINT])", hnt + "<br /><br /> " + stdtext + "<br /><br /> Appears in region: " + ",".join(item["locales"]) + f"<br /><br /><a href=\\\"https://virtualglobetrotting.com/ll/{lat},{lng}/\\\">Look on VirtualGlobeTrotting</a>")
                output = output.replace("([NELAT])", str(nelat))
                output = output.replace("([NELNG])", str(nelng))
                output = output.replace("([SWLAT])", str(swlat))
                output = output.replace("([SWLNG])", str(swlng))
                output = output.replace("([MINDIST])", str(radius))

                itmname = ("-".join(qus.split()[:15]))[-24:].lower().replace("'", "-") + "-tht-" + ("-".join(hnt.split()[:24]))[-24:].lower().replace("'", "-")
                iout = []
                

                for char in itmname:
                    if char in allowed:
                        iout.append(char)

                '''
                if "liar" in qus:
                    print("".join(iout))
                '''


                open(fnd+"/"+"questionmaps.txt", "a+").write(str(isd)+"\n\n"+"".join(iout) + " -> " + json.dumps(item) + "\n\n")
                open(fnd+"/"+"".join(iout)+".html", "w").write(output)
                isd += 1
            except Exception as e:
                #print(a)
                print(f"Item errored: {item}: {e}")
                raise
        print(f"Save finished for {fnd}")

    def doquit():
        nonlocal root
        if not checksave(): return
        root.destroy()

    def findquestioncaseback():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find backwards (case-sensitive)", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff-1
        found = False
        l = lst[:soff]
        l.reverse()
        for item in l:
            if searchto in item["title"]:
                found = True
                break
            idx += 1
        if not found:
            messagebox.showinfo("Find backwards (case-sensitive)", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findquestionback():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find backwards", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff-1
        found = False
        l = lst[:soff]
        l.reverse()
        for item in l:
            if searchto.lower() in item["title"].lower():
                found = True
                break
            idx -= 1
        if not found:
            messagebox.showinfo("Find backwards", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findquestioncase():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find (case-sensitive)", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff+1
        found = False
        for item in lst[soff+1:]:
            if searchto in item["title"]:
                found = True
                break
            idx += 1
        if not found:
            messagebox.showinfo("Find (case-sensitive)", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findquestion():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff+1
        found = False
        for item in lst[soff+1:]:
            if searchto.lower() in item["title"].lower():
                found = True
                break
            idx += 1
        if not found:
            messagebox.showinfo("Find", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findhintscaseback():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find backwards (case-sensitive)", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff-1
        found = False
        l = lst[:soff]
        l.reverse()
        for item in l:
            if searchto in item["hint"]:
                found = True
                break
            idx += 1
        if not found:
            messagebox.showinfo("Find backwards (case-sensitive)", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findhintsback():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find backwards", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff-1
        found = False
        l = lst[:soff]
        l.reverse()
        for item in l:
            if searchto.lower() in item["hint"].lower():
                found = True
                break
            idx -= 1
        if not found:
            messagebox.showinfo("Find backwards", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findhintscase():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find (case-sensitive)", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff+1
        found = False
        for item in lst[soff+1:]:
            if searchto in item["hint"]:
                found = True
                break
            idx += 1
        if not found:
            messagebox.showinfo("Find (case-sensitive)", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def findhints():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff+1
        found = False
        for item in lst[soff+1:]:
            if searchto.lower() in item["hint"].lower():
                found = True
                break
            idx += 1
        if not found:
            messagebox.showinfo("Find", "Item not found")
            root.after(300, doupdate)
            return
        
        frm1.see(idx)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(idx)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(idx)
        #frm1.
        last = -1
        updatelst(idx)
        last = idx
        root.after(300, doupdate)

    def gotoquestion():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        goto = simpledialog.askinteger("Goto", "Go to?")
        if not goto: root.after(300, doupdate); return
        
        if goto >= len(lst):
            messagebox.showerror("Goto", "Out of range")
            root.after(300, doupdate)
            return

        frm1.see(goto)
        frm1.selection_clear(0, tk.END)
        frm1.selection_set(goto)
        frm1.event_generate("<<ListboxSelect>>")
        frm1.activate(goto)
        #frm1.
        last = -1
        updatelst(goto)
        last = goto
        root.after(300, doupdate)

    def exportcsv():
        nonlocal lst, lastname
        if lst == []: return
        if not checksave(): return
        fnd = tk.filedialog.asksaveasfilename(title="Save Smarty Pins CSV file.", filetypes=(("CSV sheet", "*.csv"),))
        if not fnd: return
        try:
            data = open(fnd, "w")
            fields = ['answer_name', 'counts', 'indexlist']
            writer = csv.DictWriter(data, fieldnames=fields)
            cnt = 0
            ansmap = {}
            for q in lst:
                a = q["answer"]["title"]
                if not a in ansmap:
                    ansmap[a] = {"index": [cnt], "count": 1}
                else:
                    ansmap[a]["index"].append(cnt)
                    ansmap[a]["count"] += 1
                cnt += 1
            writer.writeheader()

            for k in sorted(ansmap, key=lambda k: ansmap[k]["count"], reverse=True):
                writer.writerow({"answer_name": k, "counts": ansmap[k]["count"], "indexlist": ansmap[k]["index"]})
        except Exception as e:
            print(f"Cannot export: {e}")
            raise
        print(f"CSV exported as {fnd}")

    filemenu.add_command(label="New", command=newfile)
    filemenu.add_command(label="New Question", command=newquestion)
    filemenu.add_command(label="Open", command=openfile)
    filemenu.add_command(label="Save", command=savefile)
    filemenu.add_command(label="Save As", command=savefileas)
    filemenu.add_command(label="Export as CSV", command=exportcsv)
    filemenu.add_command(label="Export item", command=exportitem)
    filemenu.add_command(label="Export all", command=exportitems)
    filemenu.add_command(label="Exit", command=doquit)
    root.protocol("WM_DELETE_WINDOW", doquit)

    datamenu = tk.Menu(menu, tearoff=0)
    datamenu.add_command(label="Find", command=findquestion)
    datamenu.add_command(label="Find (case-sensitive)", command=findquestioncase)
    datamenu.add_command(label="Find Backwards", command=findquestionback)
    datamenu.add_command(label="Find Backwards (case-sensitive)", command=findquestioncaseback)
    datamenu.add_command(label="Find by Hints", command=findhints)
    datamenu.add_command(label="Find by Hints (case-sensitive)", command=findhintscase)
    datamenu.add_command(label="Find by Hints Backwards", command=findhintsback)
    datamenu.add_command(label="Find by Hints Backwards (case-sensitive)", command=findhintscaseback)
    datamenu.add_command(label="Goto", command=gotoquestion)

    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Data", menu=datamenu)

    root.config(menu=menu)
    if len(sys.argv) >= 2:
        openfile(sys.argv[1])
    root.after(1, tick)
    root.mainloop()

if __name__ == "__main__":
    main()