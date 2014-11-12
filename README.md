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
		-h		--help					Display this help page and exit.
		-a		--artist				Filter by given artist.
		-d		--destination			Specify a destination (default: cwd).
				--delete-latest			Delete the newest file on SIGINT/SIGTERM.
										This is meant to prevent broken files caused
										by incomplete downloads.
										WARNING: Only use if downloading to a dedicated folder.
										THIS MAY DELETE FILES YOU OR YOUR PC CREATED!
		-f		--file-format			Specify a file format by its extension.
											(gif, jpg, jpeg, png)
										Add a "-" in front to exclude this type.
		-n		--number-of-files		Process n posts.
		-q		--quiet					Suppress output.
		-r		--rating				Filter by rating (e.g. "safe", "questionable", "explicit").
		-s		--size					Filter by resolution (e.g. "1920x1080").
				--score					Filter by score (e.g. "<20", "20", ">20", ">=20", "<=20").
		-t		--total					Guarantee that n pictures (see -n) will be downloaded.
