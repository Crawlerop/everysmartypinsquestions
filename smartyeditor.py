# https://api.mapbox.com/styles/v1/user12435235124125235824592457/ckaksz0ab1wbf1iqvfbm1g0l8/tiles/256/0/0/0@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw

# for deps: pip install requests, pillow

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, dialog
import requests
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

    hsession = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=128,
        pool_maxsize=128
    )
    hsession.mount("http://", adapter)
    hsession.mount("https://", adapter)

    alloweds = []
    for r in range(ord("a"), ord("z")+1):
        alloweds.append(chr(r))
    for r in range(ord("0"), ord("9")+1):
        alloweds.append(chr(r))
    alloweds.append("-")

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
                        height: 97.25%;
                        width: 100%;
                    }
                    textarea.righttext {
                        position:absolute;
                        right:1px;
                        bottom:15px;
                        resize:none;
                    }
                    button.rightbutton {
                        position:absolute;
                        right:1px;
                        bottom:15px;
                        resize:none;
                    }
                </style>
                
            </head>
            <body>
                <div id="mapid"></div>
                <div id="curpos">Current Position</div>
		        <div id="clickedpos">Clicked Position</div>
                <textarea class="righttext" name="llzoom" id="go" cols="32" rows="1"></textarea>
		        <button type="button" class="rightbutton" onclick="gozoom()">Go</button>
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

                    esriattr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' + 'Imagery © <a href="https://www.esri.com/">ESRI</a>'
                    
                    osmattr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'

                    normal = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    mdefault = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'mapbox/streets-v11',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    mgray = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'mapbox/light-v9',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    esrinormal = L.tileLayer('https://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
                        maxZoom: 21,
                        attribution: esriattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    esriterrain = L.tileLayer('https://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
                        maxZoom: 21,
                        attribution: esriattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        maxZoom: 21,
                        attribution: osmattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    satellite = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'user12435235124125235824592457/ckanekpxi1o3y1ipkm8tl6v3i',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    satellitenotext = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 21,
                        attribution: mapboxattr,
                        id: 'user12435235124125235824592457/ckb7ik2nf4rel1ip61enm2h23',
                        tileSize: 512,
                        zoomOffset: -1
                    })

                    gmapsnormal = L.tileLayer('https://www.google.com/maps/vt/pb=!1m4!1m3!1i{z}!2i{x}!3i{y}!2m1!1i0!3m2!2sen-US!5i1106!5m1!5f4.0!23i1358902', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    gmapsvue = L.tileLayer('https://maps.googleapis.com/maps/vt?pb=!1m5!1m4!1i{z}!2i{x}!3i{y}!4i256!2m3!1e0!2sm!3i520236120!3m17!2sen-US!3sUS!5e18!12m4!1e68!2m2!1sset!2sRoadmap!12m3!1e37!2m1!1ssmartmaps!12m4!1e26!2m2!1sstyles!2zcy50OjF8cy5lOmwudC5mfHAuYzojZmY0NDQ0NDQscy50OjV8cC5jOiNmZmYyZjJmMixzLnQ6MnxwLnY6b2ZmLHMudDozfHAuczotMTAwfHAubDo0NSxzLnQ6NDl8cC52OnNpbXBsaWZpZWQscy50OjUwfHMuZTpsLml8cC52Om9mZixzLnQ6NHxwLnY6b2ZmLHMudDo2fHAuYzojZmYyNjJlNDV8cC52Om9uLHMudDo2fHMuZTpsfHAudjpvZmY!4e0!5m1!5f4.0', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    gmapsfb = L.tileLayer('https://maps.googleapis.com/maps/vt?pb=!1m5!1m4!1i{z}!2i{x}!3i{y}!4i256!2m3!1e0!2sm!3i520236108!3m17!2sen-US!3sUS!5e18!12m4!1e68!2m2!1sset!2sRoadmap!12m3!1e37!2m1!1ssmartmaps!12m4!1e26!2m2!1sstyles!2zcy5lOmwuaXxwLnY6b2ZmLHMudDoxfHAudjpvbixzLnQ6NXxwLmM6I2ZmZThlOWU5LHMudDoyfHMuZTpnfHAuYzojZmZlOGU5ZTkscy50OjQwfHAuYzojZmZiYWQyOTQscy50OjQwfHMuZTpsfHAudjpvZmYscy50OjQ5fHMuZTpnLmZ8cC5jOiNmZmZmZmZmZixzLnQ6NDl8cy5lOmcuc3xwLnY6b2ZmLHMudDo1MHxzLmU6Zy5mfHAuYzojZmZmZmZmZmYscy50OjUwfHMuZTpnLnN8cC52Om9mZixzLnQ6NTF8cy5lOmcuZnxwLmM6I2ZmZmJmYmZiLHMudDo0fHAudjpvZmYscy50OjZ8cy5lOmd8cC5jOiNmZjQxYWVjOSxzLnQ6NnxzLmU6bC50LmZ8cC5jOiNmZjA2NTk3MSxzLnQ6NnxzLmU6bC50LnN8cC52OnNpbXBsaWZpZWQ!4e0!5m1!5f4.0', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    gmapsgray = L.tileLayer('https://maps.googleapis.com/maps/vt?pb=!1m5!1m4!1i{z}!2i{x}!3i{y}!4i256!2m3!1e0!2sm!3i520233372!3m17!2sen-US!3sUS!5e18!12m4!1e68!2m2!1sset!2sRoadmap!12m3!1e37!2m1!1ssmartmaps!12m4!1e26!2m2!1sstyles!2zcy50OjZ8cy5lOmd8cC5jOiNmZmU5ZTllOXxwLmw6MTcscy50OjV8cy5lOmd8cC5jOiNmZmY1ZjVmNXxwLmw6MjAscy50OjQ5fHMuZTpnLmZ8cC5jOiNmZmZmZmZmZnxwLmw6MTcscy50OjQ5fHMuZTpnLnN8cC5jOiNmZmZmZmZmZnxwLmw6Mjl8cC53OjAuMixzLnQ6NTB8cy5lOmd8cC5jOiNmZmZmZmZmZnxwLmw6MTgscy50OjUxfHMuZTpnfHAuYzojZmZmZmZmZmZ8cC5sOjE2LHMudDoyfHMuZTpnfHAuYzojZmZmNWY1ZjV8cC5sOjIxLHMudDo0MHxzLmU6Z3xwLmM6I2ZmZGVkZWRlfHAubDoyMSxzLmU6bC50LnN8cC52Om9ufHAuYzojZmZmZmZmZmZ8cC5sOjE2LHMuZTpsLnQuZnxwLnM6MzZ8cC5jOiNmZjMzMzMzM3xwLmw6NDAscy5lOmwuaXxwLnY6b2ZmLHMudDo0fHMuZTpnfHAuYzojZmZmMmYyZjJ8cC5sOjE5LHMudDoxfHMuZTpnLmZ8cC5jOiNmZmZlZmVmZXxwLmw6MjAscy50OjF8cy5lOmcuc3xwLmM6I2ZmZmVmZWZlfHAubDoxN3xwLnc6MS4y!4e0!5m1!5f4.0', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    gmapsbold = L.tileLayer('https://www.google.com/maps/vt?pb=!1m4!1m3!1i{z}!2i{x}!3i{y}!2m2!2sm!3i504221335!3m7!2sen-US!5i1105!12m4!1i68!2m2!1sset!2sTerrain!5m1!5f4.0!23i1358902', {
                        maxZoom: 21,
                        attribution: gmapsattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })

                    esrisatellite = L.tileLayer('https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                        maxZoom: 21,
                        attribution: esriattr,
                        id: 'user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc',
                        tileSize: 256,
                        zoomOffset: 0
                    })                    

                    esrisatellitealt = L.tileLayer('https://clarity.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                        maxZoom: 21,
                        attribution: esriattr,
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

                    gmapssatellitenotext = L.tileLayer('https://mt{s}.googleapis.com/vt?lyrs=s&hl=en-US&x={x}&y={y}&z={z}', {
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
                        "Mapbox Streets": mdefault,
                        "Mapbox Grayscale": mgray,
                        "Google Maps Normal": gmapsnormal,
                        "Google Maps Normal (Better)": gmapsfb,
                        "Google Maps Bold": gmapsbold,
                        "Google Maps Vue": gmapsvue,
                        "Google Maps Grayscale": gmapsgray,
                        "OSM": osm,
                        "ESRI Normal": esrinormal,
                        "ESRI Terrain": esriterrain,
                        "Mapbox Satellite": satellite,
                        "Mapbox Satellite (no label)": satellitenotext,
                        "Google Maps Satellite": gmapssatellite,
                        "Google Maps Satellite (no label)": gmapssatellitenotext,
                        "ESRI Satellite": esrisatellite,
                        "ESRI Satellite (alt)": esrisatellitealt,
                    }
                    
                    var dataset = {
                        "Smarty Pins data": data
                    }
                
                    layers = L.control.layers(layernames, dataset)
                    layers.addTo(mymap)	

                    mymap.on('click', function(e) {
                        document.getElementById("clickedpos").innerText = "ClickedPos: " + e.latlng.lat + ", " + e.latlng.lng + " ClickedZoom: " + mymap.getZoom()
                    });	

                    mymap.addEventListener('mousemove', function(e) {
                        document.getElementById("curpos").innerText = "Pos: " + e.latlng.lat + ", " + e.latlng.lng + " Zoom: " + mymap.getZoom()
                    });

                    function gozoom() {
			            msv = document.getElementById("go").value.split(", ")
			            if (msv[0] == document.getElementById("go").value) {
				            msv = document.getElementById("go").value.split(",")
				            if (msv[0] == document.getElementById("go").value) {
					            return
				            }
			            }
                        if (msv[2].slice(-1) !== "z") {
                            return
                        }
			            mymap.setView([parseFloat(msv[0]), parseFloat(msv[1])], parseInt(msv[2].slice(0,-1)))
		            }

                </script>
            </body>
        </html>
    '''

    #pinicon = binascii.a2b_base64('''
    #
    #''')
    
    root = tk.Tk()
    root.wm_title("Smarty Pins Editor")
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
        nonlocal lst2, lbl, last, lst, question, hint, bbox, minrange, focus, enabledfor, difficulty, standard, answer, answerpos, categories, itemid, zoom, zoomlastpos, rnd, shortname
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
                #rnd = staticmap.StaticMap(400, 400, tile_size=512, url_template="https://api.mapbox.com/styles/v1/user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw")
                '''
                ha = io.BytesIO(pinicon)
                hsk = io.BytesIO()
                himg = Image.open(ha)
                himg.thumbnail((himg.width/50,himg.height/50))
                himg.save(hsk, "png")
                hsk.seek(0)

                pina = staticmap.IconMarker((lst[nof]["answer"]["location"]["lng"], lst[nof]["answer"]["location"]["lat"]), hsk, 200, 200)

                rnd.add_marker(pina)
                '''
            lat, lng = (lst[nof]["answer"]["location"]["lat"], lst[nof]["answer"]["location"]["lng"])
                
            locaturl = f"https://api.mapbox.com/styles/v1/user12435235124125235824592457/ckao1rqf85kh01imwyf5b0pvc/static/url-https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fd%2Fd1%2FGoogle_Maps_pin.svg%2F64px-Google_Maps_pin.svg.png({lng},{lat})/{lng},{lat},{zoom.get()}/400x400@2x?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw&logo=true"

            s = hsession.get(locaturl)
            s.raise_for_status()

            outp = Image.open(io.BytesIO(s.content))
            outp.thumbnail((400,400))
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
            chtxt = "-".join(question.get().split()[:6]).lower().replace("'", "-")
            chout = ""
            for cht in chtxt:
                if cht in alloweds:
                    chout += cht
            lst[frm1.index(tk.ACTIVE)]["slug"] = chout
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
            "id":random.randint(1,1000000000000000-1),
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
        root.wm_title(f"Smarty Pins Editor - Untitled")
        root.after(300, opendelay)
        #print(lastsave)

    def newquestion():
        nonlocal lst, frm1
        if lst == []: return
        lst.append({
            "id":random.randint(1,1000000000000000-1),
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
        nonlocal lst, frm1, root, stopped, last, lastname, alloweds
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
        lsti = []
        for lstc in lst:
            chtxt = "-".join(lstc["title"].split()[:6]).lower().replace("'", "-")
            chout = ""
            for cht in chtxt:
                if cht in alloweds:
                    chout += cht
            lstc["slug"] = chout
            #print(chout)
            lsti.append(lstc)
            #print(chout)
        lst = lsti
        #print(lst)
            
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

        root.wm_title(f"Smarty Pins Editor - {lastname}")
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
        open(fnd, "w", encoding="utf-8").write(output)

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


                open(fnd+"/"+"questionmaps.txt", "a+", encoding="utf-8").write(str(isd)+"\n\n"+"".join(iout) + " -> " + json.dumps(item) + "\n\n")
                open(fnd+"/"+"".join(iout)+".html", "w", encoding="utf-8").write(output)
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

    def findanswercaseback():
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
            if searchto in item["answer"]["title"]:
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

    def findanswerback():
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
            if searchto.lower() in item["answer"]["title"].lower():
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

    def findanswercase():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find (case-sensitive)", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff+1
        found = False
        for item in lst[soff+1:]:
            if searchto in item["answer"]["title"]:
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

    def findanswer():
        nonlocal frm1, lst, last, stopped, root
        if lst == []: return
        stopped = True
        searchto = simpledialog.askstring("Find", "Find text from:")
        if not searchto: root.after(300, doupdate); return
        soff = frm1.index(tk.ACTIVE)
        idx = soff+1
        found = False
        for item in lst[soff+1:]:
            if searchto.lower() in item["answer"]["title"].lower():
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

    def reopen():
        nonlocal lastname, lst
        if lst == []: return
        openfile(lastname)

    def dodelete():
        nonlocal lst, frm1, last, stopped
        if lst == []: return
        stopped = True
        idx = frm1.index(tk.ACTIVE)
        rs = messagebox.askyesno("Warning", f"Question NO {idx+1} WILL BE DELETED!", icon="warning")
        if rs:
            tot = idx-1
            if idx == 0: tot = 0
            lst.pop(idx)
            frm1.see(tot)
            frm1.delete(idx)
            frm1.selection_clear(0, tk.END)
            frm1.selection_set(tot)
            frm1.event_generate("<<ListboxSelect>>")
            frm1.activate(tot)
            last = -1
            updatelst(tot)
            last = tot
            
        root.after(300, doupdate)

        

    root.bind("<Control-S>", lambda event: savefile())
    root.bind("<Control-O>", lambda event: openfile())
    root.bind("<Control-N>", lambda event: newfile())
    root.bind("<Control-R>", lambda event: reopen())
    root.bind("<Control-Alt-X>", lambda event: exportitem())
    root.bind("<Control-Shift-X>", lambda event: exportitems())
    root.bind("<Control-Shift-C>", lambda event: exportcsv())

    root.bind("<Control-s>", lambda event: savefile())
    root.bind("<Control-o>", lambda event: openfile())
    root.bind("<Control-n>", lambda event: newfile())
    root.bind("<Alt-n>", lambda event: newquestion())
    root.bind("<Control-r>", lambda event: reopen())
    root.bind("<Control-Alt-x>", lambda event: exportitem())
    root.bind("<Control-Shift-x>", lambda event: exportitems())
    root.bind("<Control-Shift-c>", lambda event: exportcsv())

    filemenu.add_command(label="New", command=newfile)
    filemenu.add_command(label="New Question", command=newquestion)
    filemenu.add_command(label="Open", command=openfile)
    filemenu.add_command(label="Reopen", command=reopen)
    filemenu.add_command(label="Save", command=savefile)
    filemenu.add_command(label="Save As", command=savefileas)
    filemenu.add_command(label="Export as CSV", command=exportcsv)
    filemenu.add_command(label="Export item", command=exportitem)
    filemenu.add_command(label="Export all", command=exportitems)
    filemenu.add_command(label="Exit", command=doquit)
    root.protocol("WM_DELETE_WINDOW", doquit)

    datamenu = tk.Menu(menu, tearoff=0)

    datamenu.add_command(label="Delete", command=dodelete)
    datamenu.add_command(label="Find", command=findquestion)
    datamenu.add_command(label="Find (case-sensitive)", command=findquestioncase)
    datamenu.add_command(label="Find Backwards", command=findquestionback)
    datamenu.add_command(label="Find Backwards (case-sensitive)", command=findquestioncaseback)
    datamenu.add_command(label="Find by Hints", command=findhints)
    datamenu.add_command(label="Find by Hints (case-sensitive)", command=findhintscase)
    datamenu.add_command(label="Find by Hints Backwards", command=findhintsback)
    datamenu.add_command(label="Find by Hints Backwards (case-sensitive)", command=findhintscaseback)
    datamenu.add_command(label="Find by Answer", command=findanswer)
    datamenu.add_command(label="Find by Answer (case-sensitive)", command=findanswercase)
    datamenu.add_command(label="Find by Answer Backwards", command=findanswerback)
    datamenu.add_command(label="Find by Answer Backwards (case-sensitive)", command=findanswercaseback)
    datamenu.add_command(label="Goto", command=gotoquestion)

    helpmenu = tk.Menu(menu, tearoff=0)

    def aboutMenu():
        simpledialog.SimpleDialog(root, text="Smarty Pins Editor\nVersion 0.1, 2020 WS01.", title="Smarty Pins Editor", buttons=["OK"]).go()

    helpmenu.add_command(label="About", command=aboutMenu)

    root.bind("<Control-Delete>", lambda event: dodelete())

    root.bind("<Control-G>", lambda event: gotoquestion())
    root.bind("<Control-g>", lambda event: gotoquestion())
    
    root.bind("<Control-f>", lambda event: findquestion())
    root.bind("<Control-Shift-F>", lambda event: findquestionback())

    root.bind("<Alt-a>", lambda event: findanswer())
    root.bind("<Shift-Alt-A>", lambda event: findanswerback())

    root.bind("<Control-h>", lambda event: findhints())
    root.bind("<Control-Shift-H>", lambda event: findhintsback())

    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Data", menu=datamenu)
    menu.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menu)
    if len(sys.argv) >= 2:
        openfile(sys.argv[1])
    root.after(1, tick)
    root.mainloop()

if __name__ == "__main__":
    main()
