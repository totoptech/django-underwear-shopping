import os
import sys
import re
import math
import numpy as np
import pandas as pd
from array import *
import time
from bs4 import BeautifulSoup as soup
import urllib.request

year_pattern = r"19\d\d|20\d\d"

brand_list = ["ABCTech", "Ability Systems","Acramatic","ACS","Acu-Rite","Adtech","AeroTech","Aggie Charmilles"
 ,"AH-HA","Alberti","Allen Bradley","Amada","AMC4","Anilam","Anorad","Axyz","B and R","Bandit","Biesse America","Bosch","BostoMatic"
 ,"Brother","Bridgeport","Burny","Camsoft","Centroid","Centurion","CharleyBot","Chmer","Cincinnati","CNC Masters"
 ,"CMS","C-Tek","Daewoo", "Datron","Deckel Maho","DeskCNC","DMG","DynaPath","Dooson","EasiCNC","Edge","Enroute","EMC","Emco"
 ,"EZ","Fadal","Fanuc","FlashCut","Esab","Fagor","GE","Gemini","General Automation","Giddings and Lewis","GSK","Haas"
 ,"Hansvedt","Hardinge","Heinz","Hitachi-Seiki","HPGL","Homag WoodWop","HoneyBee","Hurco","Hust","Hycut","Hypertherm","Hyundai"
 ,"Ingersoll","Koike","Komo","Laguna","Laserdyne","Leading","LightMachines"
 ,"Locshun","Mach 2,3&4 Controllers","Masterwood","Matsura","Maho","Mazak","Milltronics","Mitsubishi","Mori-Seki"
 ,"NC Studio","Nee","Nice","Northwood","Num","OKK","Okuma","OmniTech","OmniTurn","Onsrund","OpenCNC","OSAI","Pacer","Precision"
 ,"Precix","ProLight","RoboTool","Roland","Romero","Sabre","Seib-Meyer","Selexx","Sharanoa","Sherline","Shinx"
 ,"Shoda","ShopBot","ShopSabre","ShopTask","Siemens","SNK","Sodick","Sony","SouthBend","Southwest Industries ProtoTack","Style"
 ,"Taurus","Tecno","Testra","Thermwood","Torchmate","Tormach","Toshiba","Touch","Trumph","Turbo","Turner","Turmaster","Vernon","Vicon"
 ,"Vision","Weihong","WinCNC","WoodPecker","Xilog","Yasnac","Yeager","Zeus"]

model_list = [
        "DM-1",
        "DM-2",
        "DT-1",
        "DT-2",
        "EC-1600",
        "EC-1600ZT",
        "EC-400",
        "EC-500",
        "GR-510",
        "GR-712",
        "MINI MILL",
        "Mini Mill 2",
        "OM-2A",
        "Super Mini Mill",
        "Super Mini Mill 2",
        "TM-1",
        "TM-1P",
        "TM-2",
        "TM-2P",
        "TM-3",
        "TM-3P",
        "UMC-750",
        "UMC-750SS",
        "VF-1",
        "VF-10",
        "VF-10/50",
        "VF-11",
        "VF-11/50",
        "VF-1YT",
        "VF-2",
        "VF-2SS",
        "VF-2SS YT",
        "VF-2TR",
        "VF-2YT",
        "VF-3",
        "VF-3S",
        "VF-3SSYT",
        "VF-3YT",
        "VF-3YT/50",
        "VF-4",
        "VF-4SS",
        "VF-5 50XT",
        "VF-5/40",
        "VF-5/40TR",
        "VF-5/40XT",
        "VF-5/50",
        "VF-5/50TR",
        "VF-5SS",
        "VF-6",
        "VF-6/40TR",
        "VF-6/50",
        "VF-6/50TR",
        "VF-6SS",
        "VF-7",
        "VF-7/50",
        "VF-8",
        "VF-8/50",
        "VF-9",
        "VF-9/50",
        "VM-2",
        "VM-3",
        "VM-6",
        "DS-30",
        "DS-30SS",
        "DS-30SSY",
        "DS-30Y",
        "OL-1",
        "ST-10",
        "ST-10Y",
        "ST-15",
        "ST-15Y",
        "ST-20",
        "ST-20SS",
        "ST-20SSY",
        "ST-20Y",
        "ST-25",
        "ST-25Y",
        "ST-30",
        "ST-30SS",
        "ST-30SSY",
        "ST-30Y",
        "ST-35",
        "ST-35Y",
        "ST-40",
        "ST-40L",
        "ST-45",
        "ST-45L",
        "ST-50",
        "ST-55",
        "TL-1",
        "TL-2",
        "TL-3",
        "TL-3B",
        "PUMA 8S"

    ]
model_list_available = [
        "DM1",
        "DM2",
        "DT1",
        "DT2",
        "EC1600",
        "EC1600ZT",
        "EC400",
        "EC500",
        "GR510",
        "GR712",
        "MINIMILL",
        "MiniMill2",
        "OM2A",
        "SuperMiniMill",
        "SuperMiniMill2",
        "TM1",
        "TM1P",
        "TM2",
        "TM2P",
        "TM3",
        "TM3P",
        "UMC750",
        "UMC750SS",
        "VF1",
        "VF10",
        "VF10/50",
        "VF11",
        "VF11/50",
        "VF1YT",
        "VF2",
        "VF2SS",
        "VF2SSYT",
        "VF2TR",
        "VF2YT",
        "VF3",
        "VF3SS",
        "VF3SSYT",
        "VF3YT",
        "VF3YT/50",
        "VF4",
        "VF4SS",
        "VF550XT",
        "VF5/40",
        "VF5/40TR",
        "VF5/40XT",
        "VF5/50",
        "VF5/50TR",
        "VF5SS",
        "VF6",
        "VF6/40TR",
        "VF6/50",
        "VF6/50TR",
        "VF6SS",
        "VF7",
        "VF7/50",
        "VF8",
        "VF8/50",
        "VF9",
        "VF9/50",
        "VM2",
        "VM3",
        "VM6",
        "DS30",
        "DS30SS",
        "DS30SSY",
        "DS30Y",
        "OL1",
        "ST10",
        "ST10Y",
        "ST15",
        "ST15Y",
        "ST20",
        "ST20SS",
        "ST20SSY",
        "ST20Y",
        "ST25",
        "ST25Y",
        "ST30",
        "ST30SS",
        "ST30SSY",
        "ST30Y",
        "ST35",
        "ST35Y",
        "ST40",
        "ST40L",
        "ST45",
        "ST45L",
        "ST50",
        "ST55",
        "TL1",
        "TL2",
        "TL3",
        "TL3B",
        "Puma 8S"
    ]

def clean(text):
    """
    Remove any extra whitespace and line breaks as needed.
    """
    # Replace linebreaks with spaces
    text = '''
        {s}
    '''.format(s=text)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = text.split('\n')
    text = " ".join(text)
    # Remove any leeding or trailing whitespace
    text = text.strip()

    # Remove consecutive spaces
    text = re.sub(" +", " ", text)
    
    text = re.sub('[^\x00-\x7F]+',' ', text)

    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def remove_newline(text):
    string = ""
    for blines in text.splitlines():
        blines = blines.replace("\n", " ")
        string = string + blines
    return string
def parse_description(description):
    try:
        description_soup = soup(description, "html.parser")
        # print(description_soup.prettify())
        description = description_soup.text
    except:
        pass
    description = clean(description)
    description = remove_newline(description)
    return description

def get_year(title, description):
	
	year = ""
	match_year = re.search(year_pattern, title)
	if match_year:
		year = match_year.group()
	else:
		match_year = re.search(year_pattern, description)
		if match_year:
			year = match_year.group()
	return year

def get_brand(brand, title, description):
	make = ""
	try:
		if not math.isnan(brand):
			make = brand
		else:
			for brand_item in brand_list:
				match_brand = re.search(brand_item, title)
				if match_brand:
					make = match_brand.group()
			if make == "":
				for brand_item in brand_list:
					match_brand = re.search(brand_item, description)
					if match_brand:
						make = match_brand.group()
	except:
		make = brand
	return make, make

def get_model(brand, title, description, brand_list_temp):
	make = ""
	try:
		if not math.isnan(brand):
			make = brand
		else:
			for brand_item in brand_list_temp:
				match_brand = re.search(brand_item, title)
				if match_brand:
					make = match_brand.group()
			if make == "":
				for brand_item in brand_list_temp:
					match_brand = re.search(brand_item, description)
					if match_brand:
						make = match_brand.group()
	except:
		make = brand
	return make

# def get_model(model, title, description):
# 	make = ""
# 	if model:
# 		return model
# 	else:
# 		for model_item in model_list:
# 			match_model = re.search(model_item, title)
# 			if match_model:
# 				make = match_model.group()
# 			else:
# 				match_model = re.search(model_item, description)
# 				if match_model:
# 					make = match_model.group()
# 	for model_item in model_list_available:
# 		match_model = re.search(model_item, title)
# 		if match_model:
# 			make = match_model.group()
# 		else:
# 			match_model = re.search(model_item, description)
# 			if match_model:
# 				make = match_model.group()

# 	return make

def get_description(view_item_url):
    with urllib.request.urlopen(view_item_url) as response:
        html = response.read()
    soup_html = soup(html, "html.parser")
    description = soup_html.find('div', {'class' :'itemAttr'})
    return description

def analysis_product(item_title, Description, Make, Brand, Model, Year, view_item_url):
    Description = parse_description(Description)
    Year = get_year(item_title, Description)
    Make, Brand = get_brand(Brand, item_title, Description)
    Model = get_model(Model, item_title, Description, model_list)
    if Model == "":
    	Model = get_model(Model, item_title, Description, model_list_available)
    Description = get_description(view_item_url)
    return Make, Brand, Model, Year, Description

text = '''
\n\n\n\n\n\n\n\n\n\n\n\n\n Thousands of Used Metalworking and Plastic Machines & New Machine Tools Photos,Full Descriptions and Prices - Fast & Easy \n \n\n About Us Shipping Payments & Checkout FAQs \n\n\n\n\n\n\nOur Inventory\n\n \n\n\n\nHome \nCNC Machines \nManual Lathes, Mills, Drills, Saws \nGrinders, Hones, Finishing \nFabricating Equipment \nPresses & Feeds \nBoring Mills \nAutomatic Screw Machines \nEDMs \nInspection Equipment \nAir Compressors \nPlastic Machinery \nPlaners & Planer Mills \nBroaches & Keyseaters \nShapers & Slotters \nTooling & Accessories \nWelding Equipment \nWire & Fastener \nOvens, Furnaces & Environmental \nMisc Metalworking \nGear Machinery \nMaterial Handling \nMisc Non-Metalworking \n\n64" X 32" Y Haas VF-6/50 VERTICAL MACHINING CENTER, Haas 4-Axis Cntrl,CT50,30 AT\n\n64" X Axis 32" Y Axis Haas VF-6/50 VERTICAL MACHINING CENTER, Haas 4-Axis Cntrl,CT50,30 ATC,Probe,40Ref #: 158426 iammdna XVMCTRHAAS VERTICAL MACHINING CENTER MODEL: VF6/50, S/N: 1086204, NEW: 2011 X-AXIS TRAVEL........................... 64" Y-AXIS TRAVEL........................... 32"Z-AXIS TRAVEL........................... 30"SPINDLE NOSE TO TABLE................... 5" TO 35"TABLE SIZE.............................. 64" X 28"MAXIMUM WEIGHT ON TABLE................. 4,000 LBS SPINDLE SPEEDS (2 SPEED GEARED HEAD).... 7,500 RPM SPINDLE MOTOR........................... 40 HP SIDE MOUNT TOOL CHANGER................. 30 POSITIONS SPINDLE TAPER........................... CAT 50 APPROXIMATE MACHINE SIZE: .............. 195" X 102" X 130"APPROXIMATE MACHINE WEIGHT: ............ 23,000 LBS EQUIPPED WITH: * HAAS CNC CONTROL * DRIVE & WIRED 4TH AXIS READY * WIRELESS INTUITIVE PROBING SYSTEM * USB PORT AND ETHERNET * CHIP AUGER * COOLANT SYSTEM * PROGRAMMABLE COOLANT * REMOTE JOG HANGLE WITH COLOR LCD * JIB CRANE MACHINE IS IN SUPERB CONDITION Machine Location: HARRISON, NJClick Here For More Haas MachinesClick Here For More CNC Machines - VERTICAL MACHINING CENTERS. VMC's(s)UPDATE Descriptions SET Description = '19" Width Timesaver 50-19MW Wet Type, New 1997/Refurbished 2019 BELT GRINDER, V/S Conveyor, Air-KnifRef #: 158501 iammdna XBELTG 19" TIMESAVER "WET" BELT GRINDER MODEL: 5019-MW S/N: 25674S NEW: 1996 ABRASIVE BELT SIZE ..................... 19" X 48"LINFINITELY VARIABLE CONVEYOR SPEED ..... 10'' T0 30'' FPMGRINDING BELT MOTOR .................... 7.5 H.P.HEIGHT OPENING ......................... 0 TO 2- 1/2" APPROX. DIMS. .......................... 43"L-R x 55"F-B x 78"HAPPROX. MACHINE WEIGHT ................. 1,950 LBS. EQUIPPED WITH:WET OPERATION, WITH SELF-CONTAINED COOLANT SYSTEM AT THE BASE, WITH BAFFLED RESERVOIR, PAPER BED FILTERELECTRONIC VARIABLE SPEED CONVEYOR, TURN A DIAL ON THE ELECTRICAL CABINET FOR THE V/S"POSI-TRAK" SOLID STATE ELECTRONIC BELT SENSINGAIR-TENSIONING OF THE ABRASIVE BELTAIR-KNIFE DRYERDOUBLE HOLDDOWN ROLLS (INFEED & OUTFEED)5" DIAMETER MAIN CONTACT DRUM ROLL7.5 H.P. MAIN MOTOR, MOUNTED OVERHEAD, LOAD METER ON ELECTRICAL CABINETSEPARATE ELECTRICAL ENCLOSURE MOUNTED ON MACHINEMACHINE IS PRESENTLY WIRED FOR 3/60/208 VOLTS SPECIAL NOTE:THIS MACHINE HAS BEEN TAKEN APART, THOROUGHLY SERVICED, REPAINTED, AND IS NOW AVAILABLE FOR IMMEDIATE DELIVERY. ** INSPECT UNDER POWER IN OUR HARRISON, NJ WAREHOUSE **** EXCELLENT CONDITION & APPEARANCE ** Machine Location: HARRISON, NJClick Here For More Timesaver MachinesClick Here For More Fabricating Machine - BELT GRINDERS(s)Click Here For More Finishing - BELT GRINDERS(s)Click Here For More Grinders, Lappers & Hones - BELT GRINDERS(s)\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' WHERE DescriptionID = 98627;Play YouTube Video of this Item\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n\n \n\n\n\nShipping Policy \nWill ship to Worldwide. \nTOP\n\nPayments & Checkout \nWe accept PayPal, Visa & MasterCard and American Express, or contact us regarding other payment options. Please contact us soon after the auction ends (or Buy-It-Now ends listing) to tell us how you wish to pay and get any shipping quotes or pickup information you may require. \nTOP\n \n\nFrequently Asked Questions \nWe offer a 30 day return privilege on all used machines sold from our stock (machines sold for clients and shipped from their plant locations are generally not covered - so ask if you re in doubt). This return privilege is the industry standard MDNA return privilege which states the machine must be returned freight prepaid in the same condition it was shipped in (you can t break it then return it) for a full refund of your purchase price, excluding shipping costs.\nTOP\n
'''
# print(remove_newline(text))

description = """
<font size="4" style="font-family: Arial;" rwr="1"><font size="4" style="font-family: Arial;" rwr="1"><meta name="viewport" content="width=device-width, initial-scale=1"><title>bestdelas</title><link href="https://xdioms.com/store2016/machineusa/listing/css/bootstrap.css" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Terminal+Dosis" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Kaushan+Script|Questrial|Righteous" rel="stylesheet"><link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet"><link href="https://xdioms.com/store2016/machineusa/listing/css/style.css" rel="stylesheet" type="text/css"><link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet"><div class="container-fluid hbg"><div class="container"><div class="col-lg-3 col-md-3 col-sm-3 col-xs-12"> <img class="img-responsive logor" src="https://xdioms.com/store2016/machineusa/listing/images/logo.png"></div><div class="col-lg-9 col-md-9 col-sm-9 col-xs-12"><div class="col-sm-12 box1 nopad"><div class="col-lg-6 col-md-6 col-sm-6 col-xs-12 nopad"><p class="welcome">Welcome to Our Ebay Store!</p></div><div class="col-lg-6 col-md-6 col-sm-6 col-xs-12 nopad"><div class="upnav"><ul><li><a href="https://my.ebay.com/ws/eBayISAPI.dll?AcceptSavedSeller&amp;sellerid=machinestationusa&amp;ssPageName=STRK:MEFS:ADDSTR&amp;rt=nc" target="blank">Favorite Seller</a></li><li><a href="https://my.ebay.com/ws/eBayISAPI.dll?AcceptSavedSeller&amp;sellerid=machinestationusa&amp;ssPageName=STRK:MEFS:ADDSTR&amp;rt=nc" target="blank">Newsletter</a></li></ul></div></div></div><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 box2 nopad"> <header> <label class="hamburger" for="nav-toggle"></label> <input class="hidden" id="nav-toggle" type="checkbox"> <nav><ul><li><a href="https://www.ebaystores.com/machinestationusa" target="_blank">Home</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/About-Us.html" target="_blank">About Us</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/Shipping.html" target="_blank">Shipping</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/_i.html?rt=nc&amp;_sid=1285458394&amp;_sticky=1&amp;_trksid=p4634.c0.m14&amp;_sop=10&amp;_sc=1" target="_blank">New Arrivals</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/Payments.html" target="_blank">Payments</a></li><li><a href="https://contact.ebay.com/ws/eBayISAPI.dll?FindAnswers&amp;requested=machinestationusa&amp;_trksid=p2050430.m2531.l4583&amp;rt=nc" target="_blank">Contact Us</a></li></ul> </nav> </header></div></div></div></div><div class="container-fluid nopad"><img class="img-responsive img-bann" src="https://xdioms.com/store2016/machineusa/listing/images/bann.png"></div><div class="container nopad" style="margin-top: 15px;"><div class="whitesec-main"><div class="fbox"><div class="col-sm-8 col-xs-12 nopad"><div style="background: rgb(255, 255, 255); padding-top: 15px; padding-bottom: 10px; margin-top: 8px; position: relative;"><div class="slider"> <input name="slide_switch" id="id1" type="radio" checked="checked"> <label class="thumbnail" for="id1" width="450">&nbsp; </label><div class="large"></div> <input name="slide_switch" id="id2" type="radio"> <label class="thumbnail" for="id2">&nbsp; </label><div class="large"></div> <input name="slide_switch" id="id3" type="radio"> <label class="thumbnail" for="id3">&nbsp; </label><div class="large"></div> <input name="slide_switch" id="id4" type="radio"> <label class="thumbnail" for="id4">&nbsp; </label><div class="large"></div> <input name="slide_switch" id="id5" type="radio"> <label class="thumbnail" for="id5">&nbsp; </label><div class="large"></div> <input name="slide_switch" id="id6" type="radio"> <label class="thumbnail" for="id6">&nbsp; </label><div class="large"></div></div><div class="mainlightbox"> <span id="gallery"></span><input name="do_loop" id="do_loop" type="checkbox" value=""> <span class="picture" id="picture_1"> <img alt="Full picture" src="https://i.ebayimg.com/images/g/uyYAAOSwK8BbNE0U/s-l1600.jpg"> <a class="prev loop" href="#picture_7"></a> <a class="next" href="#picture_2"></a> </span><span class="picture" id="picture_2"> <img alt="Full picture" src="https://i.ebayimg.com/images/g/WYQAAOSwUxhbNE14/s-l1600.jpg"> <a class="prev" href="#picture_1"></a> <a class="next" href="#picture_3"></a> </span><span class="picture" id="picture_3"> <img alt="Full picture" src="https://i.ebayimg.com/images/g/Su4AAOSwRTtbNE0j/s-l1600.jpg"> <a class="prev" href="#picture_2"></a> <a class="next" href="#picture_4"></a> </span> <span class="picture" id="picture_4"> <img alt="Full picture" src="https://i.ebayimg.com/images/g/52QAAOSwXqZbNE0v/s-l1600.jpg"> <a class="prev" href="#picture_3"></a> <a class="next" href="#picture_5"></a> </span> <span class="picture" id="picture_5"> <img alt="Full picture" src="https://i.ebayimg.com/images/g/wxsAAOSwqWNbNE1q/s-l1600.jpg"> <a class="prev" href="#picture_4"></a> <a class="next" href="#picture_6"></a> </span> <span class="picture" id="picture_6"> <img alt="Full picture" src="https://i.ebayimg.com/images/g/WQQAAOSwUxhbNE1B/s-l1600.jpg"> <a class="prev" href="#picture_5"></a> <a class="next" href="#picture_7"></a> </span> <span id="chrome"> <label class="loop" for="do_loop">Loop</label> <a class="close" href="#gallery">Close</a> </span><div class="container2"><span class="thumb"> <a href="#picture_1"><img alt="Thumbnail" src="https://i.ebayimg.com/images/g/uyYAAOSwK8BbNE0U/s-l1600.jpg"></a> </span> <span class="thumb"> <a href="#picture_2"><img alt="Thumbnail" src="https://i.ebayimg.com/images/g/WYQAAOSwUxhbNE14/s-l1600.jpg"></a> </span> <span class="thumb"> <a href="#picture_3"><img alt="Thumbnail" src="https://i.ebayimg.com/images/g/Su4AAOSwRTtbNE0j/s-l1600.jpg"></a> </span> <span class="thumb"> <a href="#picture_4"><img alt="Thumbnail" src="https://i.ebayimg.com/images/g/52QAAOSwXqZbNE0v/s-l1600.jpg"></a> </span> <span class="thumb"> <a href="#picture_5"><img alt="Thumbnail" src="https://i.ebayimg.com/images/g/wxsAAOSwqWNbNE1q/s-l1600.jpg"></a> </span> <span class="thumb"> <a href="#picture_6"><img alt="Thumbnail" src="https://i.ebayimg.com/images/g/WQQAAOSwUxhbNE1B/s-l1600.jpg"></a> </span></div></div></div></div><div class="col-sm-4"><h3 class="titlemian">DAEWOO PUMA 8S CNC TURNING</h3><p class="rodesctitle">Product Features</p><div class="desclist"><ul><li></li><li></li><li></li><li></li><li></li></ul></div><div class="desc-sap"></div><p class="rodesctitle">Product Video</p><video class="pvideo" src="https://xdioms.com/store2016/machineusa/listing/images/visa.png" controls="controls"></video></div><div class="col-sm-12 pull-right nopad"><div class="bgh"><p class="bgtitle">Product Description</p></div><div class="desc-mian"><table width="100%" border="0" cellspacing="0" cellpadding="0"><tbody><tr><td class="price_txt"><font color="#000000">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <font size="5"><strong>DAEWOO PUMA&nbsp;8S&nbsp;CNC TURNING CENTER</strong></font></font></td></tr><tr><td><img width="10" height="10" alt="" src="https://a2zdesignstore.com/showcase/ebay_store/362/images/spacer.gif"></td></tr><tr><td align="center"><a></a><br><a></a></td></tr><tr><td><br></td></tr><tr><td><table width="100%" border="0" cellspacing="0" cellpadding="0"><tbody><tr><td class="price_bg_black"><br></td></tr><tr><td><img width="10" height="15" alt="" src="https://a2zdesignstore.com/showcase/ebay_store/362/images/spacer.gif"></td></tr><tr><td class="txt_desc2"><font color="#000000">&nbsp;<p class="p1"><span class="s1"><strong>We are a stocking dealer of New &amp; Used Machine Tools located in Southern California &amp; are members of the MDNA. We have thousands of different Manual, CNC Machines and Tooling in stock for both fabrication &amp; metal cutting.</strong></span></p><strong></strong><p class="p2"><span class="s1"></span><strong></strong></p><strong></strong><p class="p1"><span class="s1"><strong>If you have any questions regarding this machine, please contact us at </strong><a href="https://bulksell.ebay.com/ws/909-919-9600"><span class="s2"><strong>(909) 919-9600</strong></span></a><strong>&nbsp;or&nbsp;</strong><a href="mailto:orsales@machinestation.us"><span class="s2"><strong>sales@machinestation.us</strong></span></a></span></p><strong></strong><p class="p2"><span class="s1"></span><strong></strong></p><strong></strong><p class="p3"><strong><span class="s3">Machine</span><span class="s1">Station| 4590 Danito Court, Chino, CA 91710</span></strong></p><p class="p3"><span class="s1"><strong>-----------------------------------<br></strong></span></p><strong></strong><p class="p4"><span class="s4"></span><strong></strong></p><strong></strong><p class="p5"><span class="s4"></span><strong></strong></p><strong></strong><p class="p6"><span class="s1"><font face="Times New Roman" size="4"><strong>Make: Daewoo</strong></font></span></p><font face="Times New Roman" size="4"><strong></strong></font><p class="p4"><span class="s4"></span><font face="Times New Roman" size="4"><strong></strong></font></p><font face="Times New Roman" size="4"><strong></strong></font><p class="p7"><span class="s1"><font face="Times New Roman" size="4"><strong>Model No.: Puma 8S</strong></font></span></p><p class="p7"><span class="s1"><strong><font face="Times New Roman" size="4">Serial # PM8S 0226</font></strong></span></p><font face="Times New Roman" size="4"><strong></strong></font><font face="Times New Roman" size="4"><strong></strong></font><p class="p4"><span class="s4"></span><font face="Times New Roman" size="4"><strong></strong></font></p><strong><font face="Times New Roman" size="4"></font><font face="Times New Roman" size="4"></font></strong><p class="p4"><span class="s4"></span><font face="Times New Roman" size="4"><strong></strong></font></p><font face="Times New Roman" size="4"></font><p class="p6" style="font-weight: bold;"><span class="s1"><font face="Times New Roman" size="4">Condition: Very Good</font></span></p><font face="Times New Roman" size="4"></font><p class="p4" style="font-weight: bold;"><span class="s4"></span><font face="Times New Roman" size="4"></font></p><font face="Times New Roman" size="4"></font><p class="p8" style="font-weight: bold;"><span class="s1"><font color="#00429a" face="Times New Roman" size="4">All specifications are approximations, and are subject to verification.</font></span></p><p class="p8" style="font-weight: bold;"><span class="s1">-------------------------------------------------------<br></span></p><p class="p4" style="font-weight: bold;"><span class="s4"></span></p><p class="p5" style="font-weight: bold;"><span class="s4"></span></p><p class="p9"><span class="s1"><u><b><font color="#00429a" size="4">Equipped With:</font></b></u></span></p><p class="p9"><span class="s1"><font face="Times New Roman"><strong><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Fanuc OT-C&nbsp;CNC Control</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">8″ 3 Jaw&nbsp;Hydraulic Chuck</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">A2-6 Spindle</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Hydraulic Programmable Tailstock</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Coolant System</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Barfeed Interface</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">RS-232&nbsp;ports</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">12 Station Automatic&nbsp;Turret</span><br style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;"><span style="color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-style: normal; font-weight: 400; word-spacing: 0px; float: none; display: inline !important; white-space: normal; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Foot Switch</span></strong></font><span class="s1"><p><strong><font face="Times New Roman">Comes with Tool Holders, Chip Conveyor and Live Center.</font></strong></p><p><strong><br><font face="Times New Roman"></font></strong></p><p class="p9"><font face="Times New Roman"></font></p><p class="p9"><span class="s1"><u><font color="#00429a" face="Times New Roman" size="5"><strong>Specifications:</strong></font></u></span></p><p><font face="Times New Roman"></font></p><p><font face="Times New Roman"></font></p></span></span></p><p class="p9"><strong><font color="#00429a" face="Times New Roman"></font></strong></p><p class="p4"><font face="Times New Roman"><span class="s4"></span><strong><font color="#00429a"></font></strong></font></p><strong><font color="#00429a"></font></strong><p class="p6"><font face="Times New Roman"></font></p><span class="s6"><p class="p6"><strong><font color="#00429a"></font></strong></p><p style="margin: 0in 0in 0pt;"><font color="#00429a" face="Times New Roman"><strong><u>Capacity:</u></strong></font></p><p style="margin: 0in 0in 0pt;"><br></p><font face="Times New Roman"><p style="margin: 0px 0px 1.61em; color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Max Turning Diameter: 14.6″<br style="box-sizing: border-box;">Max Turning Length: 20.7″<br style="box-sizing: border-box;">Max Bar Capacity: 2.05″<br style="box-sizing: border-box;">Swing Over Bed: 19.7″<br style="box-sizing: border-box;">Distance Between Centers: 21.9″</p><p style="margin: 0px 0px 1.61em; color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">X Axis Travel: 8.3″<br style="box-sizing: border-box;">Z Axis Travel:&nbsp;21.7″<br style="box-sizing: border-box;">Rapid Traverse&nbsp;X Axis:&nbsp;630 IPM<br style="box-sizing: border-box;">Rapid Traverse Z Axis:&nbsp;787 IPM</p><p style="margin: 0px 0px 1.61em; color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Spindle Nose:&nbsp;A2-6<br style="box-sizing: border-box;">Spindle Bore:&nbsp;2.4″<br style="box-sizing: border-box;">Spindle Speed:&nbsp;0 – 4000 RPM<br style="box-sizing: border-box;">Spindle Motor:&nbsp;25 HP</p><p style="margin: 0px 0px 1.61em; color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Turret Capacity:&nbsp;12 Stations<br style="box-sizing: border-box;">Turret Index Time:&nbsp;1 Second</p><p style="margin: 0px 0px 1.61em; color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">Tailstock Taper: MT-4<br style="box-sizing: border-box;">Tailstock&nbsp; Quill Dia.: 3.1″<br style="box-sizing: border-box;">Tailstock Quill Travel: 4.0″</p><p style="margin: 0px 0px 1.61em; color: rgb(96, 100, 108); text-transform: none; text-indent: 0px; letter-spacing: normal; font-family: Roboto, sans-serif; font-size: 13px; font-style: normal; font-weight: 400; word-spacing: 0px; white-space: normal; box-sizing: border-box; orphans: 2; widows: 2; background-color: rgb(255, 255, 255); font-variant-ligatures: normal; font-variant-caps: normal; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">General:<br style="box-sizing: border-box;">Power: 21 kva, 220v / 3-Phase<br style="box-sizing: border-box;">Overall Dimensions: 114″ x 76″ x 77″&nbsp;High<br style="box-sizing: border-box;">Weight: 11000 lbs</p><p style="margin: 0in 0in 0pt;"><span class="s4"><br></span></p></font><p style="margin: 0in 0in 0pt;"><br></p></span><p class="p6"><font face="Times New Roman"><strong></strong></font></p><p class="p4"><span class="s4"></span><font face="Times New Roman"><strong></strong></font></p><font face="Times New Roman"><strong></strong></font><span class="s4"><font face="Times New Roman"><strong>Comes as shown in pictures.. For *VIDEO* and more Pictures visit "<a href="https://www.machinestation.us/">www.MachineStation.us</a></strong></font></span></font></td></tr></tbody></table></td></tr></tbody></table></div></div></div></div></div> <br><div class="container-fluid up-footer"><div class="container" style="background: none;"><div class="col-sm-8 nopad"><p class="subt"> Add our store to your favourites &amp; receive our Newsletters<br> with new items &amp; special offers</p> <a href="https://my.ebay.com/ws/eBayISAPI.dll?AcceptSavedSeller&amp;sellerid=machinestationusa&amp;ssPageName=STRK:MEFS:ADDSTR&amp;rt=nc" target="_blank"><div class="sub-btn">Subscribe</div></a></div></div></div><div class="container"><div class="col-sm-3 col-xs-12"><div class="flogo-c"> <img class="flogo2 img-responsive" src="https://xdioms.com/store2016/machineusa/listing/images/logo.png"></div></div><div class="col-sm-4 col-xs-12"><h4 class="fhead">Why Choose US?</h4><ul class="list"><li>&nbsp;&nbsp;&nbsp;Safe tracked shipment Worldwide (Parcels)</li><li>&nbsp;&nbsp;&nbsp;Secure Payments By PayPal</li></ul> <img class="fpay img-responsive" src="https://xdioms.com/store2016/machineusa/listing/images/visa.png"></div><div class="col-sm-2 col-xs-12"><h4 class="fhead">Information</h4><ul class="list"><li><a href="https://www.ebaystores.com/machinestationusa" target="_blank">Home</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/About-Us.html" target="_blank">About Us</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/Shipping.html" target="_blank">Shipping</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/Returns.html" target="_blank">Returns</a></li><li><a href="https://www.ebaystores.com/MACHINESTATIONUSA/Payments.html" target="_blank">Payments</a></li><li><a href="https://contact.ebay.com/ws/eBayISAPI.dll?FindAnswers&amp;requested=machinestationusa&amp;_trksid=p2050430.m2531.l4583&amp;rt=nc" target="_blank">Contact Us</a></li></ul></div><div class="col-sm-3 col-xs-12"> <a href="https://www.ebaystores.com/machinestationusa" target="_blank"><div class="fbutton1"><p>View All Items</p></div></a> <a href="https://www.ebaystores.com/MACHINESTATIONUSA/_i.html?rt=nc&amp;_sid=1285458394&amp;_sticky=1&amp;_trksid=p4634.c0.m14&amp;_sop=10&amp;_sc=1" target="_blank"><div class="fbutton1"><p>New Arrivals</p></div></a> <a href="https://www.ebaystores.com/MACHINESTATIONUSA/_i.html?rt=nc&amp;_sacat=MACHINESTATIONUSA&amp;_sc=1&amp;_sid=1285458394&amp;_sticky=1&amp;_trksid=p4634.c0.m14&amp;_sop=1&amp;_sc=1" target="_blank"><div class="fbutton1"><p>Ending Soon</p></div></a></div></div><div class="container lowf"><p class="fcopy3">© Copyright 2018 - Machine Station USA | All Rights Reserved</p></div></font></font>
"""
item_title = """
	1997 Haas VF-OE 
"""
brand = ""
model = ""
view_item_url = "https://www.ebay.com/itm/1999-Haas-SL-20-w-Rigid-Tap-Spindle-Orientation-Barfeed-Interface-Chip-Auger-/163701903981"
# print(parse_description(description))
# print(get_year(item_title, description))

# print(get_brand(brand, item_title, description))
# print(get_model(model, item_title, description))

# print(analysis_product(item_title, description, "", brand, model, ""))
# print(get_description(view_item_url))

