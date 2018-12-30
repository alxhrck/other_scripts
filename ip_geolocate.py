'''
	
	ip_geolocate.py
	Alex Herrick - Dec 2012

'''
import urllib, json, simplekml

# unique API key from IPInfoDB.com
ip_info_api_key = "1234"
api_url = "http://api.ipinfodb.com/v3/ip-city/?format=json&callback=&key=" + ip_info_api_key + "&ip="

url = urllib.FancyURLopener()
kml = simplekml.Kml()

# open file containing list of IPs
file = open('ip.txt', 'r')

# dict of every ip and login attempt count
bad_ip = {}

tmp2 = None

# counts every occurnace of IP in ip.txt to determine login attemps
for line in file:
	tmp1 = line.rstrip()
	if tmp1 == tmp2:
		# increase login attempt counter
		bad_ip[tmp1] = bad_ip[tmp1] + 1
	else:
		# create a new login attempt counter
		bad_ip[tmp1] = 1
	tmp2 = tmp1

# data parsing
for ip, count in bad_ip.iteritems():
	data = url.open(api_url + ip)
	geo_data = json.load(data)
	location = [geo_data['cityName'], geo_data['regionName'], geo_data['countryName']]
	long_lat = [geo_data['longitude'], geo_data['latitude']]
	
	info = " <![CDATA[ " + ", ".join(location) + "<br />" + "Login Attempts: " + str(count) + " ]]>"
	
	kml.newpoint(name = ip, description = info, coords=[(long_lat[0], long_lat[1])])
	
	#print ", ".join(location) + '\n', ip_addr + ":" , ", ".join(long_lat) + '\n'
	
kml.save("location_data.kml")
print "KML file has been created."
