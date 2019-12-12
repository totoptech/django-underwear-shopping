import os
import sys
import numpy as np
import pandas as pd
import time

#https://developer.ebay.com/DevZone/finding/Concepts/FindingAPIGuide.html
	#https://developer.ebay.com/DevZone/finding/CallRef/extra/fnditmsadvncd.rqst.srtordr.html
	#paginationInput.pageNumber=1. starts at 1.
	#outputSelector[1]=SellerInfo

import requests
	
myappid = "adamj-Barker-PRD-bea94fa4c-f21d10ee"

def makeFindingAPICall(myappid, mykeywords, page_num, min_search_price=None, max_search_price=None):
	"""
	Makes an eBay finding API call.
	https://developer.ebay.com/devzone/finding/CallRef/findItemsByKeywords.html
	
	myappid: your eBay API app id. Try inserting in a search URL like the following to verify you've got the right ID:
	http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-NAME=FindingService&SERVICE-VERSION=1.19.0&GLOBAL-ID=EBAY-US&SECURITY-APPNAME=your_app_id_here&RESPONSE-DATA-FORMAT=XML&sortOrder=StartTimeNewest&keywords=dmg%20mori&paginationInput.pageNumber=1&outputSelector[1]=SellerInfo&outputSelector[2]=PictureURLLarge&outputSelector[3]=PictureURLSuperSize
	
	mykeywords: your search keywords
	page_num: which page number the search will look at. For searches with more than 100 results.
	min_search_price: exclude items under this price.
	max_search_price: exclude items over this price.
	"""
	params = {
		'OPERATION-NAME':'findItemsByKeywords',
		'SERVICE-NAME':'FindingService',
		'SERVICE-VERSION':'1.1.13',
		'GLOBAL-ID':'EBAY-US',
		'SECURITY-APPNAME':myappid,
		'RESPONSE-DATA-FORMAT':'JSON',
		'sortOrder':'StartTimeNewest',
		'keywords':mykeywords,
		'paginationInput.pageNumber':page_num,
		'outputSelector[0]':'SellerInfo',
		'outputSelector[1]':'StoreInfo',
		'outputSelector[2]':'PictureURLLarge',
		'outputSelector[3]':'PictureURLSuperSize',
	}
	filt_i = 0
	if min_search_price is not None:
		params["itemFilter["+str(filt_i)+"].name"] = "MinPrice"
		params["itemFilter["+str(filt_i)+"].value"] = min_search_price
		filt_i += 1
	if max_search_price is not None:
		params["itemFilter["+str(filt_i)+"].name"] = "MaxPrice"
		params["itemFilter["+str(filt_i)+"].value"] = max_search_price
		filt_i += 1
	#http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-NAME=FindingService&SERVICE-VERSION=1.19.0&GLOBAL-ID=EBAY-US&SECURITY-APPNAME=your_app_id_here&RESPONSE-DATA-FORMAT=XML&sortOrder=StartTimeNewest&keywords=dmg%20mori&paginationInput.pageNumber=1&outputSelector[1]=SellerInfo&outputSelector[2]=PictureURLLarge&outputSelector[3]=PictureURLSuperSize
	#http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-NAME=FindingService&SERVICE-VERSION=1.19.0&GLOBAL-ID=EBAY-US&SECURITY-APPNAME=your_app_id_here&RESPONSE-DATA-FORMAT=XML&sortOrder=StartTimeNewest&keywords=dmg%20mori&paginationInput.pageNumber=1&outputSelector[1]=SellerInfo&outputSelector[2]=PictureURLLarge&outputSelector[3]=PictureURLSuperSize&itemFilter[0].name=MinPrice&itemFilter[0].value=250
	time.sleep(2) #don't spam requests
	URL = "http://svcs.ebay.com/services/search/FindingService/v1"
	r = requests.get(url=URL, params=params)
	result_json = r.json()
	return result_json

#######
##ordered column names for CSV
colnames = [
	'searched_keywords',
	'timestamp',
	'item_id',
	'item_title',
	'item_url_short',
	'primary_category_id',
	'primary_category_name',
	'secondary_category_id',
	'secondary_category_name',
	'listing_type',
	'category_id',
	'currency',
	'price',
	'shipping',
	'bestOfferEnabled',
	'num_watchers',
	'condition_name',
	'seller_username',
	'seller_feedback_number',
	'seller_feedback_percent',
	'thumbnail_url',
	'photo_url',
	'huge_photo_url',
	'paymentMethod',
	'postalCode',
	'location',
	'country',
	'view_item_url',
	#'item_specifics',
	#'description',
	###single item fields
]

def parse_item(myitem, timestamp='', keywords=''):
	"""
	Parses listing metadata from a single-item JSON returned in an eBay API call.
	myitem: item JSON data to parse.
	timestamp: (optional) timestamp to label item with.
	keywords: (optional) searched keywords to label item data with.
	"""
	for k in list(myitem.keys()):
		if len(myitem[k]) == 1:
			myitem[k] = myitem[k][0]
	item_id = myitem["itemId"]
	view_item_url = myitem["viewItemURL"]
	item_url_short = "https://ebay.com/itm/"+item_id
	item_title = myitem["title"]
	listing_type = myitem["listingInfo"]["listingType"][0]
	primary_category_id = myitem["primaryCategory"]["categoryId"][0]
	primary_category_name = myitem["primaryCategory"]["categoryName"][0]
	try:
		secondary_category_id = myitem["secondaryCategory"]["categoryId"][0]
		secondary_category_name = myitem["secondaryCategory"]["categoryName"][0]
	except:
		secondary_category_id = ''
		secondary_category_name = ''
	#price_USD = float(myitem["sellingStatus"]["convertedCurrentPrice"][0]["__value__"])
	currency = myitem["sellingStatus"]["currentPrice"][0]["@currencyId"]
	price = float(myitem["sellingStatus"]["currentPrice"][0]["__value__"])
	try:
		shipping = float(myitem["shippingInfo"]["shippingServiceCost"][0]["__value__"])
	except:
		shipping = 0.0
	bestOfferEnabled = myitem["listingInfo"]["bestOfferEnabled"][0]
	try:
		num_watchers = myitem[3]["listingInfo"][0]["watchCount"][0]
	except:
		num_watchers = 0
	try:
		condition_name = myitem["condition"]["conditionDisplayName"][0]
	except:
		condition_name = ""
	seller_username = myitem["sellerInfo"]["sellerUserName"][0]
	seller_feedback_number = int(myitem["sellerInfo"]["feedbackScore"][0])
	seller_feedback_percent = float(myitem["sellerInfo"]["positiveFeedbackPercent"][0])
	try:
		thumbnail_url = myitem["galleryURL"]
	except:
		thumbnail_url = ""
	try:
		photo_url = myitem["pictureURLLarge"]
	except:
		photo_url = ''
	try:
		huge_photo_url = myitem["pictureURLSuperSize"]
	except:
		huge_photo_url = ''
	try:
		paymentMethod = myitem['paymentMethod']
	except:
		paymentMethod = ''
	try:
		postalCode = myitem['postalCode']
	except:
		postalCode = ''
	try:
		location = myitem['location']
	except:
		location = ""
	try:
		country = myitem['country']
	except:
		country = ""
	#import pdb; pdb.set_trace()
	return {
		'searched_keywords':keywords,
		'timestamp':timestamp,
		'item_id':item_id,
		'item_title':item_title,
		'item_url_short':item_url_short,
		'primary_category_id':primary_category_id,
		'primary_category_name':primary_category_name,
		'secondary_category_id':secondary_category_id,
		'secondary_category_name':secondary_category_name,
		'listing_type':listing_type,
		'currency':currency,
		'price':price,
		'shipping':shipping,
		'bestOfferEnabled':bestOfferEnabled,
		'num_watchers':num_watchers,
		'condition_name':condition_name,
		'seller_username':seller_username,
		'seller_feedback_number':seller_feedback_number,
		'seller_feedback_percent':seller_feedback_percent,
		'thumbnail_url':thumbnail_url,
		'photo_url':photo_url,
		'huge_photo_url':huge_photo_url,
		'paymentMethod':paymentMethod,
		'postalCode':postalCode,
		'location':location,
		'country':country,
		'view_item_url':view_item_url,
	}

def makeSingleItemAPICall(myappid, myitemid):
	"""
	makes the eBay API call to get full listing details for a single item.
	https://developer.ebay.com/devzone/shopping/docs/callref/GetSingleItem.html
	
	myappid: your eBay API app id
	myitemid: the listing id of the item to be looked up.
	
	This call returns the item specifics and full listing description, both of which are not returned in the bulk search results.
	"""
	params = {
		'callname':'GetSingleItem',
		#'SERVICE-NAME':'FindingService',
		#'SERVICE-VERSION':'1.1.13',
		'version':'1089',
		#'GLOBAL-ID':'EBAY-US',
		'siteid':'0',
		'appid':myappid,
		#'RESPONSE-DATA-FORMAT':'JSON',
		'responseencoding':'JSON',
		'ItemID':myitemid,
		#'IncludeSelector':'Details,Description,TextDescription,ItemSpecifics,ShippingCosts',
			#TextDescription overrides description
		#'IncludeSelector':'Details,TextDescription,ItemSpecifics,ShippingCosts',
			#ShippingCosts usually errors.
			#Need to use GetShippingCosts call for that.
		'IncludeSelector':'Details,Description,ItemSpecifics',
		#'IncludeSelector':'Details,TextDescription,ItemSpecifics',
		#'IncludeSelector[3]':'ItemSpecifics',
			#*** This gets the category details like Brand, MPN. They are all given by custom NameValueList name in the response.
		#'IncludeSelector[4]':'ShippingCosts',
		#'IncludeSelector[0]':'Details',
			#What does this get?
			#BestOfferEnabled
			#StartTime
			#PaymentMethods
			#PostalCode
			#Seller/store info
			#*** Quantity
			#*** QuantitySold
			#BidCount
			#HitCount
			#*** ConditionDescription
			#Also possible to get multiple picture URLs through PictureURL
		#'IncludeSelector[1]':'Description',
		#'IncludeSelector[2]':'TextDescription',
		#'IncludeSelector[3]':'ItemSpecifics',
		#'IncludeSelector[4]':'ShippingCosts',
		#'IncludeSelector[5]':'Variation',
		#'IncludeSelector[6]':'Compatibility',
	}
	#http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=XML&appid=[your_app_id_here]&siteid=0&version=967&ItemID=180126682091&IncludeSelector=ShippingCosts
	time.sleep(2) #don't spam requests
	URL = "http://open.api.ebay.com/shopping"
	r = requests.get(url=URL, params=params)
	result_json = r.json()
	return result_json

#myitemid = "163593598809"
#result_json = makeSingleItemAPICall(myappid, myitemid)
#do Ack check as usual
#myitem = result_json["Item"]
def parseSingleItemResult(myitem):
	"""
	Parses the result of a single item API call, extracting details such as full item description, bid count, hit count, condition description, and item specifics.
	
	myitem: JSON result from GetSingleItem API call
	"""
	try:
		html_description = myitem["Description"]
	except:
		html_description = ''
	try:
		BidCount = myitem['BidCount']
	except:
		BidCount = ''
	try:
		HitCount = myitem['HitCount']
	except:
		HitCount = ''
	try:
		ConditionDescription = myitem["ConditionDescription"]
	except:
		ConditionDescription = ''
	try:
		ItemSpecifics = myitem["ItemSpecifics"]["NameValueList"]
		
	except:
		ItemSpecifics = []
	#import pdb; pdb.set_trace()
	return {
		'html_description':html_description,
		'ConditionDescription':ConditionDescription,
		'ItemSpecifics':ItemSpecifics,
		'BidCount':BidCount,
		'HitCount':HitCount,
		#can get multiple PictureURL's, too.
	}

def parse_pages(myappid, mykeywords = "dmg mori", max_pages = 5, order_colnames = colnames, agg_items = pd.DataFrame([], columns=colnames), add_single_items_limit = 10, min_search_price=None, max_search_price=None, filter_results_under_this_pricePlusShipping=5000):
	"""
	Main function to make an eBay API search and aggregate item data.
	
	myappid
	mykeywords: search keywords
	max_pages: max pages to search
	order_colnames: column order for output CSV
	agg_items: (empty list by default). Items from previous searches, if results from previous searches are to be used. They would be compared on item id to avoid inserting duplicates.
	
	add_single_items_limit: Maximum number of GetSingleItem requests to make. e.g. if a search returned 1000 results and you don't want to make 1000 calls to check descriptions for all 1000 items. Then set this to 10 and it will only check up to 10 items.
	
	min_search_price: Exclude items under this price from appearing in search results. Used in finding API call.
	max_search_price: Exclude items over this price from appearing in search results. Used in finding API call.
	
	filter_results_under_this_pricePlusShipping: Exclude found items from appearing in CSV if their price + shipping is under this value.
	"""
	result_pages_max = -1
	page_num = 1
	error_count = 0
	while 1:
		if error_count >= 10:
			print("Exceeded 10 errors in a row. Stopping for now.")
			break
		if result_pages_max != -1:
			print("searching page",page_num,"of",result_pages_max)
		else:
			print("searching page",page_num)
		result_json = makeFindingAPICall(myappid, mykeywords, page_num, min_search_price, max_search_price)
		try:
			result = result_json["findItemsByKeywordsResponse"][0]
		except:
			print("result has no findItemsByKeywordsResponse")
			error_count += 1
			continue
		if result["ack"][0] == "Failure":
			print("ack is failure.")
			error_count += 1
			continue
		error_count = 0
		try:
			result_pages_max = int(result["paginationOutput"][0]["totalPages"][0])
			n_items = int(result["paginationOutput"][0]["totalEntries"][0])
			if page_num == 1:
				print(n_items, "total items.")
			if n_items == 0:
				break
			allitems = result["searchResult"][0]["item"]
			#<>timestamp = result["timestamp"][0]
			timestamp = result["timestamp"][0].split("T")[0]
			parsed_items = pd.DataFrame([parse_item(x, timestamp, mykeywords) for x in allitems], columns=order_colnames)
			if len(agg_items) > 0:
				parsed_items = filterDupes(parsed_items, agg_items)
			###add single item results
			for i in range(len(parsed_items)):
				if add_single_items_limit <= 0:
					break
				#filter by price, too
				skip_detailed_search_because_item_is_too_inexpensive = filter_results_under_this_pricePlusShipping is not None and parsed_items.iloc[i]["price"] + parsed_items.iloc[i]["shipping"] < filter_results_under_this_pricePlusShipping
				if skip_detailed_search_because_item_is_too_inexpensive:
					continue
				myitemid = parsed_items.iloc[i]["item_id"] #always new ID since list was already filtered.
				result_json = makeSingleItemAPICall(myappid, myitemid)
				if result_json["Ack"] == "Failure":
					print("item ack is failure. skipping item.")
					print("all result json for failed search:", result_json)
					continue
				print("adding text description for item id", myitemid)
				myitem = parseSingleItemResult(result_json["Item"])
				add_single_items_limit -= 1
				parsed_items.loc[i, "Description"] = myitem["html_description"]
				parsed_items.loc[i, "ConditionDescription"] = myitem["ConditionDescription"]
				parsed_items.loc[i, "BidCount"] = myitem["BidCount"]
				parsed_items.loc[i, "HitCount"] = myitem["HitCount"]
				#then for the item specifics the values need to be done one by one, adding many columns
				for j in range(len(myitem["ItemSpecifics"])):
					keyname = myitem["ItemSpecifics"][j]["Name"]
					keyvalue = "\n".join(myitem["ItemSpecifics"][j]["Value"])
					parsed_items.loc[i, keyname] = keyvalue
			#append to list
			agg_items = agg_items.append(parsed_items, sort=False)
			agg_items.reset_index(inplace=True, drop=True)
			page_num += 1
			if page_num > result_pages_max or page_num > max_pages:
				print(page_num, "is greater than max pages. ending search")
				break
		except:
			print("Some kind of weird parsing error. Check it out.")
			import pdb; pdb.set_trace()
	agg_items.reset_index(drop=True, inplace=True)
	return agg_items

def filterDupes(all_items, old_items):
	"""
	Filter duplicate items already found in an old item list.
	"""
	newidlist = np.array([x for x in all_items["item_id"].astype(str).values if x not in old_items["item_id"].astype(str).values])
	parsed_items_filtered = all_items[[x in newidlist for x in all_items["item_id"]]]
	parsed_items_filtered.reset_index(drop=True, inplace=True)
	return parsed_items_filtered

def filterInexpensiveItems(parsed_items, filter_results_under_this_pricePlusShipping):
	return parsed_items.iloc[[i for i in range(len(parsed_items)) if parsed_items.iloc[i]["price"] + parsed_items.iloc[i]["shipping"] >= filter_results_under_this_pricePlusShipping]].reset_index(drop=True)

def sample_search(mykeyword, outfilename, max_pages=5, add_single_items_limit=10, min_search_price=None, max_search_price=None, filter_results_under_this_pricePlusShipping=5000):
	print("starting keyword search for:",mykeyword)
	all_items = parse_pages(myappid, mykeywords = mykeyword, max_pages = max_pages, order_colnames = colnames, agg_items = pd.DataFrame([], columns=colnames), add_single_items_limit = add_single_items_limit, min_search_price=min_search_price, max_search_price=max_search_price, filter_results_under_this_pricePlusShipping=filter_results_under_this_pricePlusShipping)
	#import pdb; pdb.set_trace()
	if filter_results_under_this_pricePlusShipping is not None:
		all_items = filterInexpensiveItems(all_items, filter_results_under_this_pricePlusShipping)
	#all_items.to_csv("sample_search.csv", index=False)
	#replace \n in description
	try:
		all_items.loc[:, "Description"] = all_items.loc[:, "Description"].apply(lambda x: x if pd.isna(x) else x.replace("\n", "\\n"))
	except: #no description keys.
		pass
	# import pdb; pdb.set_trace()
	try: #check if file already exists
		#filter item numbers that are already in old searches. Then, write new searches on top of old searches to csv.
		old_items = pd.read_csv(outfilename)
		#all_items = filterDupes(all_items, old_items)
		#<>all_items.append(old_items).to_csv(outfilename, index=False)
		old_items.append(all_items, sort=False).reset_index(drop=True).to_csv(outfilename, index=False) #write to bottom
	except:
		all_items.to_csv(outfilename, index=False)


	return all_items

def sample_search_old(mykeyword, outfilename, max_pages=5, add_single_items_limit=10, min_search_price=None, max_search_price=None, filter_results_under_this_pricePlusShipping=5000):
	print("starting keyword search for:",mykeyword)
	all_items = parse_pages(myappid, mykeywords = mykeyword, max_pages = max_pages, order_colnames = colnames, agg_items = pd.DataFrame([], columns=colnames), add_single_items_limit = add_single_items_limit, min_search_price=min_search_price, max_search_price=max_search_price, filter_results_under_this_pricePlusShipping=filter_results_under_this_pricePlusShipping)
	#import pdb; pdb.set_trace()
	if filter_results_under_this_pricePlusShipping is not None:
		all_items = filterInexpensiveItems(all_items, filter_results_under_this_pricePlusShipping)
	#all_items.to_csv("sample_search.csv", index=False)
	#replace \n in description
	try:
		all_items.loc[:, "Description"] = all_items.loc[:, "Description"].apply(lambda x: x if pd.isna(x) else x.replace("\n", "\\n"))
	except: #no description keys.
		pass
	#import pdb; pdb.set_trace()
	try: #check if file already exists
		#filter item numbers that are already in old searches. Then, write new searches on top of old searches to csv.
		old_items = pd.read_csv(outfilename)
		#all_items = filterDupes(all_items, old_items)
		#<>all_items.append(old_items).to_csv(outfilename, index=False)
		old_items.append(all_items, sort=False).reset_index(drop=True).to_csv(outfilename, index=False) #write to bottom
	except:
		all_items.to_csv(outfilename, index=False)
	print("\n")
	return

#Haas, Okuma, Doosan, Mazak, dmg mori

# #MinPrice
# os.makedirs("ebay_out", exist_ok=True)
# #max_pages=5
# add_single_items_limit=5
# max_pages=500
# # add_single_items_limit=1000
# keywords = ["Haas", "Okuma", "Doosan", "Mazak", "dmg mori"]
# for thiskeyword in keywords:
# 	sample_search(thiskeyword, "ebay_out/"+thiskeyword+".csv", max_pages=max_pages, add_single_items_limit=add_single_items_limit, min_search_price=4000, max_search_price=None, filter_results_under_this_pricePlusShipping=5000)
