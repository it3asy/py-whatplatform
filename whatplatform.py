# coding: utf-8

import os,sys,inspect
import re,urlparse
import time
import requests
import optparse
from linkparser import *

reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG_LEVEL = 1


ROOT_DIR=os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))

try:
	import requests.packages.urllib3
	requests.packages.urllib3.disable_warnings()
except:
    pass


def _debug(s,level):
	if level<=DEBUG_LEVEL:
		x = 32+level
		print '\033[0;%s;40m' % x + '  ' * (level-1) + '- %s' % s + '\033[0m'


platforms = {
		'exts':{
			'php':['php'],
			'asp':['asp'],
			'asp.net':['aspx','asmx','ashx','axd'],
			'java':['jspx','jsp','do','action'],
			},
		'exclude':['jpg','js','gif','bmp','png','ico','css'],
		}

header_finger = {
	'Server':{
		'java':['Apache-Coyote'],
		#'php':['PHP/']
		},
	'Set-Cookie':{
		'java':['JSESSIONID'],
		'asp.net':['ASP.NET_SessionId'],
		'asp':['ASPSESSIONID'],
		'php':['PHPSESSIONID'],
		},
	'X-Powered-By':{
		'java':['Jboss', 'JSP/', 'Servlet',],
		'php':['PHP/']

		}
	}


def http_get(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-GB,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'Connection': 'keep-alive'
	}
	session = requests.Session()
	try:
		resp = session.get(url, headers=headers, timeout=20)
		return resp
	except Exception as e:
		return

def get_status(url):
	try:
		resp = http_get(url)
		return resp.status_code
	except:
		return

def get_charset(html, headers=[]):
	if html[0:3] == '\xef\xbb\xbf':
		return 'UTF-8'
	if dict(headers).has_key('Content-Type'):
		match = re.search('charset[\s]*?=[\s]*?[\'"]?([a-z0-9\-]+)[\'"]?', headers['Content-Type'], re.IGNORECASE)
		if match:
			return match.group(1).upper()
	match = re.search('<meta\s[\s\S]*?charset[\s]*?=[\s]*?[\'"]?([a-z0-9\-]+)[\'"]?[\s\S]*?>', html, re.IGNORECASE)
	if match:
		return match.group(1).upper()
	try_list = ["UTF-8", "GB18030", "BIG5"]
	for codec in try_list:
		try:
			decoded = html.decode(codec)
			return codec
		except:
			continue
	return 'UTF-8'

def get_exts_by_links(links):
	exts = {}
	scripts = []
	for i in links:
		p = urlparse.urlparse(i).path
		q = p.split('/')
		n = len(q)
		if n>0:
			scripts.append(q[n-1])
	for i in set(scripts):
		if '.' in i:
			p = i.split('.')
			n = len(p)
			ext = p[n-1]
			try:
				exts[ext]
			except:
				exts[ext] = 0
			exts[ext] = exts[ext] + 1
	return exts
		
def get_platform_by_exts(exts):
	global platforms
	plats = []
	for ext in exts:
		if ext in platforms['exclude']:
			continue
		for key in platforms['exts'].keys():
			if ext in platforms['exts'][key]:
				if key not in plats:
					plats.append(key)
	return plats

def get_platform_by_links(links):
	exts = get_exts_by_links(links)
	platform = get_platform_by_exts(exts)
	return platform


def get_platform_by_headers(headers):
	global header_finger
	hd = dict(headers)
	for key in header_finger.keys():
		if hd.has_key(key):
			for platform in header_finger[key]:
				for keyword in header_finger[key][platform]:
					if keyword in hd[key]:
						_debug('found "%s" in %s' % (keyword,key), 2)
						return [platform]

	_debug('return  []',2)
	return []


def get_platform_by_index(url, headers, content):
	baseurl = url
	charset = get_charset(content, headers)
	content = content.decode(charset, 'ignore')
	links = LinksParser(baseurl,content).get_links_internal()
	platform = get_platform_by_links(links)

	_debug('return  %s'%platform,2)
	return platform


def get_platform_by_blind(website):

	weburl = website
	url_404 = '/adcbf8c6f66dcf'
	url_tries = ['/index','/default','/search']
	for platform in platforms['exts'].keys():
		exts = platforms['exts'][platform]
		for ext in exts:

			_debug('trying .%s' % ext, 2)

			url = weburl + url_404 + '.' + ext

			resp_404 = http_get(url)
			if resp_404 == None:
				_debug('bad request, break...', 3)
				break

			content_404 = resp_404.content.decode(get_charset(resp_404.content, resp_404.headers),'ignore')
			status_404 = resp_404.status_code
			content_404_length = len(content_404)

			_debug('404_status=%s, 404_length=%s'%(status_404,content_404_length), 3)

			for url_try in url_tries:
				url = weburl + url_try + '.' + ext

				_debug('requesting  %s'%url, 3)

				resp = http_get(url)
				if resp == None:
					_debug('bad request, continue next', 3)
					continue
				status = resp.status_code

	
				if status_404 == 404:
					if status in [200,500]:
						_debug('status=%s'%status, 3)
						_debug('return %s'%platform, 3)
						return [platform]
				else:
					content = resp.content.decode(get_charset(resp.content, resp.headers),'ignore')
					content_length = len(content)

					_debug('status=%s, length=%s' % (status,content_length), 3)

					p = (max(content_404_length,content_length) - min(content_404_length,content_length)) * 100 / min(content_404_length,content_length)
					_debug('ratio is %s%%'%p, 3)
					if p > 5:
						_debug('return %s'%platform, 3)
						return [platform]
			_debug('not matched', 2)
	_debug('return  []',2)
	return []


def whatplatform(target, debug_level=0):
	global DEBUG_LEVEL
	DEBUG_LEVEL = debug_level
	result = {'index':[], 'header':[], 'blind':[]}
	weburl = target['website']

	_debug('request %s'%weburl, 1)
	resp = http_get(weburl)
	if resp == None:
		_debug('error: bad request, exiting...', 2)
		return

	_debug('status %s'%resp.status_code, 2)

	headers = resp.headers
	baseurl = resp.url
	content = resp.content

	if target['header']:
		_debug('headering...', 1)
		platform = get_platform_by_headers(headers)
		result['header'] = platform

	if target['index']:
		_debug('indexing...', 1)
		platform = get_platform_by_index(baseurl, headers, content)
		result['index'] = platform

	if not len(result['header'])==1 and not len(result['index'])==1:
		if target['blind']:
			_debug('blinding...', 1)
			platform = get_platform_by_blind(weburl)
			result['blind'] = platform

	return result

if __name__=='__main__':
	import optparse
	parser = optparse.OptionParser('usage: %prog [options] target.com')
	parser.add_option("-?", action="help", help=optparse.SUPPRESS_HELP)
	parser.add_option("--blind", dest="blind", action="store_true", help="with blind mode")
	parser.add_option("-d", "--debug", dest="debug", action="append", type=int,help="show debug log level", metavar="level")
	(options, args) = parser.parse_args()

	if len(args) < 1:
		parser.print_help()
		sys.exit(0)

	target = {'website':args[0],'header':True, 'index': True, 'blind':False}

	if options.debug:
		DEBUG_LEVEL = options.debug[0]

	if options.blind:
		target['blind'] = True
	
	print whatplatform(target, DEBUG_LEVEL)


	