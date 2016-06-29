import urllib2
import re
#
#
#       ieee-oui-parse.py
#
#       convert ieee oui.txt to CSV for use with Splunk TA isc-dhcp
#
#
#       Alex Herrick - March 2014 - @alxhrck
#
url = 'http://standards.ieee.org/develop/regauth/oui/oui.txt'
print '[*] Downloading {url}'.format(url=url)
output = urllib2.urlopen(url)
oui_txt = output.read()
output.close()

print '[*] Parsing oui.txt...'

with open('dhcpd-mac_vendor_names.csv', 'wb') as output:

    output.write('src_mac_prefix,src_mac_vendor\n')
    for line in oui_txt.splitlines():
            try:
                if 'hex' in line:
                    line = re.sub('[.,]','',line)   # remove extra commas to prevent csv from breaking and periods (i dont like them.)
                    mac = line.split()[0].replace('-', ':')
                    org = line.split('\t\t')[1]
                    text = '{mac}*,"{org}"\n'.format(mac=mac, org=org)
                    #print text
                    output.write(text.lower())
            except IndexError:
                 print "[-]ERROR: Index Error"

print '[*] Add to transforms.conf:', 'match_type = WILDCARD(src_mac_prefix)'  # OUI is first half of the MAC.