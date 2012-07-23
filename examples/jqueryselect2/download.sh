#!/bin/sh

prompt_download( ) {
	if [ -z "$DOWNLOADS" ] ; then
		cat <<EOM
Use --downloads-yes to automatically answer the next prompt with 'yes' and
use --downloads-no to automatically answer the next prompt with 'no'
EOM
	fi
	while [ "$DOWNLOADS" != "no" -a "$DOWNLOADS" != "yes" ] ; do
		read -p "Download Processing.js? (yes/no) " DOWNLOADS
	done
	if [ "$DOWNLOADS" = "yes" ] ; then
		return 0;
	fi
	return 1
}
get_jquery ( ) {
    URL="http://code.jquery.com"
    URL="$URL/jquery-1.7.2.min.js"
	if which wget >/dev/null ; then
		wget -O output/jquery.min.js "$URL"
	elif which curl >/dev/null ; then
		curl -L "$URL" -o output/jquery.min.js
	else
		echo "No wget/curl found" >&2
		exit 1
	fi
}
get_select2 ( ) {
    URL="https://github.com/downloads/ivaynberg/select2"
    URL="$URL/select2-2.1.zip"
	if which wget >/dev/null ; then
		wget -O xxx.zip "$URL"
        unzip xxx.zip
        mv select2-2.1 output/select2
        rm xxx.zip
	elif which curl >/dev/null ; then
		curl -L "$URL" -o xxx.zip
        unzip xxx.zip
        mv select2-2.1 output/select2
        rm xxx.zip
	else
		echo "No wget/curl found" >&2
		exit 1
	fi
}
if [ ! -f processing.js ] ; then
	if prompt_download ; then
		get_jquery
        get_select2
	else
		echo "Will not download processing.js" >&2
		exit 1
	fi
fi
exit 0
