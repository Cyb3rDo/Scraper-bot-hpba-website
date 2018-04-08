from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import requests
import time

# This is the start url with all searches on one page. Remember to change the maxnr for future scrapes. In this instance the maxnr is 2266
start_url = urlopen("http://secure.hpba.org/cvweb/cgi-bin/utilities.dll/CustomList?ORGNAME_field=&ORGTYPE=&CITY_field=&STATECD=&ZIP_field=&DISTANCE=5000&COUNTRY_field=&_MULTIPLE_PRODUCT_TYPELIST=&_MULTIPLE_PRODUCT_CLASSLIST=&EMAIL=&ORGNAME=&CITY=&ZIPSEARCH=&ZIPDISTSEARCH=&COUNTRYSEARCH=&RANGE=1%2F2266&NOWEBFLG=%3C%3EY&ISMEMBERFLG=Y&SHOWSQL=N&SORT=ORGNAME&SQLNAME=ORGSEARCH&WHP=organization.htm&WBP=organizationList.htm")
# Create a Beautiful Object to read the page into a variable
bsObj = BeautifulSoup(start_url.read(), "lxml")
# Empty list to collect Organization link tags
orgid_tags = []
# Empty list to collect extracted Organization ids from tags
url_ids = []
# Empty list for collecting all collected organization details as list
org_collection = []
# Loop over all links and collect Organization ids
for x in bsObj.find_all('a'):    # will give you all a tag
     try:
         if re.match('getCVPageLink',x['onclick']):    # if onclick attribute exist, it will match for getCVPageLink, if success will be added to orgid_tags list
            orgid_tags.append(x['onclick'])        
     except:pass
# Extract digits from the tags and add to url_ids list
for tags in orgid_tags:
	url_ids.append((re.findall(r'\d+', tags)))

counter = 0
# Create a csv file and save looped data into a csv file in current working directory
with open('hpba_pitts_and_spitts.csv', 'w', newline='', encoding='utf-8') as outfile:
	mywriter = csv.writer(outfile)
	mywriter.writerow(['Name', 'Address', 'City', 'State/Province', 'ZIP/Postal', 'Country', 'Phone', 'Email', 'Web Site', 'NFI', 'Type'])
	# Loop over all organization ids in url_ids 
	for id in url_ids:
		# Build unique url for each organization 
		org_url = urlopen("https://secure.hpba.org/cvweb/cgi-bin/organizationdll.dll/Info?orgcd="+id[0])
		# Create a Beautiful Object to read the organization page into a variable
		bsObj2 = BeautifulSoup(org_url.read(), "lxml")
		# Empty list for collecting organization details from bsObj2 variable
		org_det = []
		# Find organization name 
		org_name = bsObj2.find('dt', text="Organization Name").find_next_sibling("dd").text
		org_det.append(org_name)
		# Find address
		org_addr = bsObj2.find('dt', text="Address").find_next_sibling("dd").text
		# If there is a line 2 for address concatenate the addresses
		if bsObj2.find('dt', text="Address Cont."):
				org_addr2 = bsObj2.find('dt', text="Address Cont.").find_next_sibling("dd").text
				org_det.append(org_addr+"/"+org_addr2)
		else:
			org_det.append(org_addr)
		# Find org city
		org_city = bsObj2.find('dt', text="City").find_next_sibling("dd").text
		org_det.append(org_city)
		# Find org State/Province
		org_prov = bsObj2.find('dt', text="State/Province").find_next_sibling("dd").text
		org_det.append(org_prov)
		# Find org ZIP/Postal Code
		org_zip = bsObj2.find('dt', text="Zip/Postal Code").find_next_sibling("dd").text
		org_det.append(org_zip)
		# If there is a country tag extract country or default is US
		if bsObj2.find('dt', text="Country"):
			org_country = bsObj2.find('dt', text="Country").find_next_sibling("dd").text
		else:
			org_country = "US"
		org_det.append(org_country)
		# Find org phonenumber
		if bsObj2.find('dt', text="Phone Number"):
    			org_tel = bsObj2.find('dt', text="Phone Number").find_next_sibling("dd").text
		else:
			org_tel = "N/A"
		org_det.append(org_tel)
		# Find org email
		org_email = bsObj2.find('dt', text="Email Address").find_next_sibling("dd").text
		org_det.append(org_email)
		# Find org web site address
		org_web = bsObj2.find('dt', text="Company Web Site").find_next_sibling("dd").text
		org_det.append(org_web)
		
		# Get NFI status for staff and add to org_det list
		nfi_status = requests.get("https://secure.hpba.org/cvweb/cgi-bin/utilities.dll/customlist?SQLNAME=NFISTAFF&ORGCD="+id[0]+"&WMT=none&WBP=staff.htm")
		if nfi_status.text[0] == 'Y':
			nfi_s = nfi_status.text[0]
		elif nfi_status.text[0] == 'N':
			nfi_s = nfi_status.text[0]
		else:
			nfi_s = ''
		
		org_det.append(nfi_s)

		#Find Organization type and add to org_det list
		org_find = bsObj2.find('dt', text="Organization Type").find_next_sibling("dd").text
		if "RETL" in org_find[0:30]:
			org_type = "Retailer"
			org_det.append(org_type)
		if "M00" in org_find[0:30]:
			org_type = "Manufacturer"
			org_det.append(org_type)
		if "DIST" in org_find[0:30]:
			org_type = "Distributor"
			org_det.append(org_type)
		if "NONP" in org_find[0:30]:
			org_type = "Non-Profit"
			org_det.append(org_type)
		if "SERV" in org_find[0:30]:
			org_type = "Service"
			org_det.append(org_type)
		if "ASOC" in org_find[0:30]:
			org_type = "Associate"
			org_det.append(org_type)
		if "FCMR" in org_find[0:30]:
			org_type = "Manufacturer Representative"
			org_det.append(org_type)
		if "COSB" in org_find[0:30]:
			org_type = "Company Subsidiary"
			org_det.append(org_type)
		if "IDST" in org_find[0:30]:
			org_type = "Installing Distributor"
			org_det.append(org_type)
		if "UNSP" in org_find[0:30]:
			org_type = "Unspecified"
			org_det.append(org_type)
		if "PFA" in org_find[0:30]:
			org_type = "Pellet Fuels Associate"
			org_det.append(org_type)
		if "B00" in org_find[0:30]:
			org_type = "Manufacturer"
			org_det.append(org_type)
		if "ASCR" in org_find[0:30]:
			org_type = "Associate Retailer"
			org_det.append(org_type)
		if "HPBA" in org_find[0:30]:
			org_type = "HPBA Related"
			org_det.append(org_type)
		if "ADDR" in org_find[0:30]:
			org_type = "Additional Retail Locations"
			org_det.append(org_type)
		if "ADDD" in org_find[0:30]:
			org_type = "Additional Distributor Locations"
			org_det.append(org_type)
		
		# Fix leading zero for ZIP Code
		try:
			org_det[4] = '='+'"'+org_det[4]+'"'
		except TypeError:
			pass
	
		# Increase counter for logging purposes
		counter += 1
		# Write row to csv file
		mywriter.writerow(org_det)
		# Sleep for one second to avoid overloading the servers
		time.sleep(1)

		#Logging info 
		print(counter)
		print(id)










