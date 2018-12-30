##  Logged IP to Country Code - lip2cc.py
##
##  Script will preform WHOIS quires on IP address from a file,
##  then display the country of orign
##
##  Alex Herrick - June 2011 - share with credits

import sys
import socket
import re
from optparse import OptionParser

def read_file(f):
        f = open(f,'r')
        i = []
        for line in f:
                i.append(line.rstrip())
        return i

def parse_opts():
        parser = OptionParser()
        parser.add_option("-f", "--file", dest="filename",
                          help="FILE containing list of IPs", metavar="FILE")
        (options, args) = parser.parse_args()
        
        return options.filename

def ip_connect(a,x):
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                address = a
                if address != '':
                        s.connect((address,43))
                        s.send(x + '\r\n')
                        return s
        except Exception, ei:
                s.close()
                print ei

def search(p,fstr,cstr):
        p = p.lower()
        refIndex = p.find(fstr)
        if refIndex != -1:
                pat = re.compile(cstr)
                line = p[refIndex:]
                found = pat.match(line)
                try:
                     return found.group(0)
                except Exception, er:
                        print er
        else:
                return '0'

def whois(u,x):
        s2 = ip_connect(u,x)
        while True:
                try:
                        p2 = s2.recv(4096)
                except Exception, er2:
                        print er2
                        s2.close()
        # Find Country Code
                fstr = 'country:'
                cstr = 'country.+'
                tmp = search(p2,fstr,cstr)
                if tmp != '0':
                        tmp = re.sub(r'\s+', '', tmp)
                        coAry = tmp.split(':')
                        country = coAry[0].title() + ': ' + coAry[1].upper()
                        return country
                        
                if p2 == '':
                        s2.close()
                        return '0'
                        break

def registry_lookup(x):  
                a = 'whois.iana.org'
                s = ip_connect(a,x)
                while True:
                    try:
                        p = s.recv(4096)
                    except Exception, er:
                        print er
                        s.close()
                        break
                
        # Find Regional Registry URL
                    fstr = 'whois.'
                    cstr = 'whois\.?[a-z]+?\.net'
                    url = search(p,fstr,cstr)
                    if url != '0':
                            return url
                            break
                    if p == '':
                        s.close()
                        break

def main(): 
        f = parse_opts() 
        ip = read_file(f)
        for x in ip:
                reg = registry_lookup(x)
                co = whois(reg,x)
                if co == '0':
                        co = 'Country not found!'

                print 'Logged IP: ' + x + '\n' + co + '\nRefer: ' + reg + '\n'


if __name__ == '__main__':
        main()
