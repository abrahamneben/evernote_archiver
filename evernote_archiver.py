import commands
import os
import xml.etree.ElementTree as ET
from dateutil.parser import parse
import datetime
import urllib
import cgi
import sys
from shutil import copyfile

# date utilities
def html_name_to_date(h):
	r = ET.parse(h).getroot()
	return parse(r[0].find("meta[@name='created']").attrib['content'])
def html_name_to_tags(h):
	r = ET.parse(h).getroot()
	if r[0].find("meta[@name='keywords']") is not None:
		return r[0].find("meta[@name='keywords']").attrib['content']
	return ''


if len(sys.argv) == 1:
	print('Usage: python evernote_archiver.py [name of file listing paths to all evernote HTML exports]')
	sys.exit(1)

# load paths to evernote html exports
archive_paths = [l.strip() for l in open(sys.argv[1]).readlines()]

# generate the "table of contents" of all the archives
archive_index_file = open('index.html','w')
archive_index_file.write('<html><body><ul>\n')
for a in archive_paths: 
	archive_index_file.write('<li><a href="'+a+'/frameview.html">'+a+'</a></li>\n')
archive_index_file.write('</ul></body></html>')
archive_index_file.close()

for archive_path in archive_paths:
	print(archive_path)
	archive_name = archive_path.split('/')[-1]

	copyfile('nav.css',archive_path+'/nav.css')
	copyfile('nav.js',archive_path+'/nav.js')
	os.chdir(archive_path)

	# find all the .html files (i.e, all the notes)
	html_names = commands.getoutput('ls *.html').split('\n')
	html_names.remove('index.html')
	if 'frameview.html' in html_names: html_names.remove('frameview.html')
	if 'nav.html' in html_names: html_names.remove('nav.html') 
	html_names_sorted = sorted(html_names,key=html_name_to_date,reverse=True)

	# create the nav frame HTML file with links to all the note HTML files
	nav_file = open(archive_path+'/nav.html','w')
	nav_file.write('<!DOCTYPE html><html>\n')
	nav_file.write('<head><title>nav</title></head>')
	nav_file.write('<link rel="stylesheet" type="text/css" href="nav.css"/>')
	nav_file.write('<body>\n')

	for i in range(len(html_names_sorted)):
		h = html_names_sorted[i]
		p_class = ''
		if i==0: p_class = 'selected'
		nav_file.write('<a href="'+urllib.quote(h)+'" target="note_frame" onclick="change_focus(this);" class="'+p_class+'"><p>\n')
		nav_file.write('<b>'+cgi.escape(h.split('.html')[0])+'</b><br/>\n')
		nav_file.write(html_name_to_date(h).strftime('%b %d, %Y @ %I:%M %p')+'\n')
		nav_file.write('<span class="tags">'+html_name_to_tags(h)+'</span>')
		nav_file.write('</p></a>')

	nav_file.write('<script type="text/javascript" src="nav.js"></script>\n')
	nav_file.write('</body>\n</html>')
	nav_file.close()


	# create the evernote-style view with iframes with the nav frame on the left, and the note on the right
	frameview_file = open(archive_path+'/frameview.html','w')

	frameview_file.write('<!DOCTYPE html>\n<html>\n<head>\n<title>'+archive_name+'</title>\n')

	frameview_file.write('<iframe id="nav_frame" src="nav.html" style="position: absolute; left:0; width:30%; height:100%"></iframe>\n')
	frameview_file.write('<iframe id="note_frame" src="'+urllib.quote(html_names_sorted[0])+'" style="position: absolute; right:0; width:70%; height:100%"></iframe>\n')

	# set the default focus to the nav frame so that the up and down key commands work right
	# when the page loads
	frameview_file.write('<script>document.getElementById("nav_frame").focus();</script>')
	frameview_file.write('</body></html>')
	frameview_file.close()

