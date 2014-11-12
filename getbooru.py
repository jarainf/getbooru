#!/usr/bin/env python3
# Author: Jan 'jarainf' Rathner <jan@rathner.net>

from xml.dom import minidom
from urllib.request import urlopen, urlretrieve, URLError
from urllib.parse import quote_plus
import os
import sys, getopt
import signal

GELBOORU = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index'
USAGE = '''\tgetbooru 1.0
	A simple API-based Gelbooru crawler.
	Author: Jan 'jarainf' Rathner

	http://github.com/jarainf/getbooru
	
	Usage: getbooru [options] [tags]
	
	Options:
	-h	--help					Display this help page and exit.
	-a	--artist				Filter by given artist.
	-d	--destination				Specify a destination (default: cwd).
		--delete-latest				Delete the newest file on SIGINT/SIGTERM.
							This is meant to prevent broken files caused
							by incomplete downloads.
							WARNING: Only use if downloading to a dedicated folder.
							THIS MAY DELETE FILES YOU OR YOUR PC CREATED!
	-f	--file-format				Specify a file format by its extension
								(gif, jpg, jpeg, png)
							Add a "-" in front to exclude this type.
	-n	--number-of-files			Process n posts.
	-q	--quiet					Suppress output.
	-r	--rating				Filter by rating (e.g. "safe", "questionable", "explicit").
	-s	--size					Filter by resolution (e.g. "1920x1080").
		--score					Filter by score (e.g. "<20", "20", ">20", ">=20", "<=20").
	-t	--total					Guarantee that n pictures (see -n) will be downloaded.
	'''

def _parseURL(url, total = False, n = 0):
	global duplicates
	global xmlerrors

	images = {}

	xml = _getContent(url)
	if xml is None:
		print('XML data could not be retrieved.\nExiting...')
		return False

	try:
		parsedXml = minidom.parseString(xml)
	except:
		xmlerrors += 1
		print('XML was malformed, couldn\'t continue.\nExiting...')
		return False

	posts = parsedXml.getElementsByTagName('post')

	if posts == []:
		return False

	for i in posts:
		images[i.attributes['id'].value] = i.attributes['file_url'].value

	for id, location in images.items():
		filetype = location.rsplit('.', 1)[1]
		if filetype not in fformat:
			continue
		filename = os.path.join(destination, id + '.' + filetype)
		if os.path.isfile(filename):
			duplicates += 1
			continue
		image = _getImage(location, filename)
		if not downloads < n and total:
			print('return')
			return False

	return True

def _getContent(url):
	global xmlerrors
	data = None
	try:
		data = urlopen(url).readall()
	except URLError as e:
		xmlerrors += 1
		if not quiet:
			print('URL: ' + url + ' could not be opened.')
	return data

def _getImage(url, file):
	global downloads
	global urlerrors
	try:
		urlretrieve(url, file)
		downloads += 1
	except URLError as e:
		urlerrors += 1
		try:
			os.remove(file)
		except:
			pass
		if not quiet:
			print('Image: ' + url + ' could not be retrieved.')

def _usage():
	print(USAGE)

def _signals(signum = None, frame = None):
	global destination
	global delete_latest
	if(delete_lastest):
		latest = _latest_changed_file(destination)
		try:
			os.remove(latest)
		except:
			print('Could not delete latest changed file. You should probably stop using Windows.')
	print('Interrupted, terminating...')
	sys.exit(0)

def _latest_changed_file(dir):
	def list_files(dir):
		for dirpath, dirnames, filenames in os.walk(dir):
			for filename in filenames:
				yield os.path.join(dirpath, filename)
	return max(list_files(dir), key=os.path.getmtime)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'a:d:f:hn:qr:s:t', ['rating=', 'help', 'quiet', 'size=' ,'score=', 'artist=', 'file-format=', 'total', 'number-of-files=', 'destination=', 'delete-latest'])
	except getopt.GetoptError as e:
		print(e)
		_usage()
		sys.exit(1)

	global quiet
	global delete_latest
	global downloads
	global duplicates
	global xmlerrors
	global urlerrors
	global fformat
	global destination

	delete_latest = False
	quiet = False
	downloads = 0
	duplicates = 0
	xmlerrors = 0
	urlerrors = 0
	fformat = ('jpg', 'jpeg', 'gif', 'png')
	destination = os.curdir

	total = False
	tags = ' '.join(args) + ' '
	pages = 1
	last = 0
	inf = False

	for opt, arg in opts:
		if opt in ('-a', '--artist'):
			tags += arg + ' '
		elif opt in ('-d', '--destination'):
			if arg != '':
				if not os.path.exists(arg):
					try:
						os.makedirs(arg)
					except:
						print('Failed to create directory \"' + destination + '\", exiting.')
						sys.exit(1)
				destination = arg
		elif opt == '--delete-latest':
			delete_latest = True
		elif opt in ('-f', '--file-format'):
			if arg in ('jpeg', 'jpg'):
				fformat = ('jpeg', 'jpg')
			elif arg == 'png':
				fformat = 'png'
			elif arg == 'gif':
				fformat = 'gif'
			elif arg in ('-jpg', '-jpeg'):
				fformat = ('gif', 'png')
			elif arg == '-png':
				fformat = ('jpg', 'jpeg', 'gif')
			elif arg == '-gif':
				fformat = ('jpg', 'jpeg', 'png')
			else:
				print('Argument: \"' + arg + '\" not recognized, possible arguments:')
				print('jpg, jpeg, gif, png, -jpg, -jpeg, -gif, -png')
				print('Note that \"jpg\" and \"jpeg\" are the same format and specifying one of them will also download the other.')
		elif opt in ('-h', '--help'):
			_usage()
			sys.exit(0)
		elif opt in ('-n', '--number-of-files'):
			if arg != '' and arg.isdigit():
				pages = int(arg) // 100
				last = int(arg) % 100
			elif arg == 'inf':
				inf = True
			else:
				print('You have to specify a number for \"-n\", using default (100).')
				pages = 1
				last = 0
		elif opt in ('-q', '--quiet'):
			quiet = True
		elif opt in ('-r', '--rating'):
			tags += 'rating:' + arg + ' '
		elif opt in ('-s', '--size'):
			sarg = arg.split('x')
			if len(sarg) == 2 and arg.replace('x', '').isdigit():
				tags += 'width:' + sarg[0] + ' height:' + sarg[1] + ' '
			else:
				print('Invalid size formatting - should be \"$WIDTHx$HEIGHT\" but got: ' + arg + '\nExiting...')
		elif opt in ('-t', '--total'):
			total = True
		elif opt == '--score':
			tags += 'score:' + arg + ' '
		else:
			sys.exit(1)

	for sig in [signal.SIGTERM, signal.SIGINT]:
		signal.signal(sig, _signals)

	url = GELBOORU + '&tags=' + quote_plus(tags)
	
	if not inf and (not total or fformat == ('jpg', 'jpeg', 'gif', 'png')):
		done = False
		for i in (j for j in range(pages) if not done):
			done = not _parseURL('%s&limit=100&pid=%d' % (url, i))
		if last != 0 and not done:
			_parseURL('%s&limit=%d&pid=%d' % (url, last, pages))
	elif not inf:
		done = False
		i = 0
		while not done:
			done = not _parseURL('%s&limit=100&pid=%d' % (url, i), True, pages * 100 + last)
			i += 1
		if (xmlerrors + urlerrors) == 0:
			print('Done, total downloads: %03d.' % downloads)
		else:
			print('Done, total downloads: %03d. XML-Errors: %03d, URL-Errors: %03d' % (downloads, xmlerrors, urlerrors))
		sys.exit(0)

	else:
		i = 0
		while _parseURL(url + '&limit=100&pid=' + str(i)):
			i +=1
	if (xmlerrors + urlerrors) == 0:
		print('Done, total downloads: %03d. Duplicates: %03d. Total: %03d.' % (downloads, duplicates, duplicates + downloads))
	else:
		print('Done, total downloads: %03d. Duplicates: %03d. Total: %03d. XML-Errors: %03d, URL-Errors: %03d.' % (downloads, duplicates, duplicates + downloads, xmlerrors, urlerrors))

if __name__ == "__main__":
	main()
