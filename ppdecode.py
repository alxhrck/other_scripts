# -*- coding: utf-8 -
#
#   Original ppdecode Code: https://github.com/warquel/ppdecode
#       Scripttified by Alex Herrick
#       Added: Remove zero width space chars from URLs in Proofpoint alerts.
#

import urlparse
import re
import argparse

class PPDecode(object):
    def __init__(self, pplink):
        self.pplink = pplink
        self.pplink = self._remove_unicode()
        self.arguments = urlparse.parse_qs(urlparse.urlparse(self.pplink).query)

        if 'urldefense' in self.pplink:
            self.url = self._decodeurl()
            self._parse()
        else:
            self.url = self.pplink

    def _decodeurl(self):
        tmp = self.arguments['u'][0].replace("_","/")
        for x in list(set(re.findall('-[0-9A-F]{2,2}', tmp))):
            tmp = tmp.replace(x, chr(int(x[1:3],16)))
        return tmp

    def _parse(self):
        self.recipient = self.arguments['r'][0]
        self.site = self.arguments['c'][0]

    def _remove_unicode(self):
        # Remove zero width space unicode character from URL
        udata = self.pplink.decode("utf-8")
        tmp = udata.replace(u'\u200b', '')
        return tmp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='proofpoint encoded URL to decode')
    parser.add_argument('-r', '--recipient', help='display recipient id', action='store_true')
    parser.add_argument('-s', '--site', help='display site id', action='store_true')
    args = parser.parse_args()

    url = args.url
    p = PPDecode(url)
    print '[+] Dencoded URL: {url}'.format(url=p.url.replace('http', 'hxxp'))

    if args.recipient:
        print '\tRecipient: {0}'.format(p.recipient)

    if args.site:
        print '\tSite: {0}'.format(p.site)

