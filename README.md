getbooru
========

Crawls getbooru for images corresponding tags and options and downloads them.

# Requirements:
- Python 3.4 (Should work on all versions of Python 3, but didn't test that)

# Usage:

		getbooru 1.0
		A simple API-based Gelbooru crawler.
		Author: Jan 'jarainf' Rathner
		
		http://github.com/jarainf/getbooru
		
		Usage: getbooru [options] [tags]
		
		Options:
		-h		--help					Displays this help page and exits
		-a		--artist				Specify an artist to search for his works
		-d		--destination			Specify a destination (default: .)
				--delete-latest			Delete the latest changed file on SIGINT/SIGTERM
										This is meant to prevent malicous files, because
										of incomplete downloads.
										WARNING: Only use if downloading to a dedicated folder
										THIS MAY DELETE FILES YOU OR YOUR PC CREATED!
		-f		--file-format			Specify a file format by its extension
											(gif, jpg, jpeg, png)
										Add a "-" in front to exclude this type
		-n		--number-of-files		The number of files to look through
		-q		--quiet					Quiet mode
		-r		--rating				Specify the rating to retrieve files from (e.g. "safe", "questionable", "explicit")
		-s		--size					Specify the resolution of files to download (e.g. "1920x1080")
				--score					Specify a score limit (e.g. "<20", "20", ">20", ">=20", "<=20")
		-t		--total					If added, downloads a total of "-n"-files, if possible
