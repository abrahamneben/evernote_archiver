# evernote_archiver

Evernote is a conventient way to keep track of code, plots, thoughts, half-results, etc. I've been
using it as a digital lab notebook for data analyses for years. Unfortunately there are occasionally
bugs and outages on Evernote's servers, and I don't like the idea of having to rely on the Evernote 
client continuing to exist for years to come.

I wrote evernote_archiver to produce a wrapper webpage to view the HTML notes produced by an Evernote
export in an Evernote-like two-column interface. Navigation is on the left and the note is shown
on the right. This allows the completed notebook to be preserved in pure HTML/CSS/Javascript without risk
of accidental deletion or of Evernote going out of business. You can quickly flip through the notes
with the arrow keys, or scroll and click the one you want to see. You can use the browser's page search
to search note titles.

![screenshot](screenshot.gif?raw=true "screenshot")

