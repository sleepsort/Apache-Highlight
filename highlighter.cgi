#!/usr/bin/env python2
# highlight.cgi: Syntax Highlight Code and Send it as HTML
# Copyright 2009-2010 Jonas Buckner
# Distributed under the GNU General Public License
# http://www.gnu.org/licenses/gpl.html
#
# 2009-05-13: Initial Release
# 2010-05-12: Added Documentation to README
#             Changed one of the styles to make the numbers a fixed-width font
# 2010-11-26: Added Link to download the highlighted file as plain text
# 2013-08-18: Remove color scheme and simplify codes for better performance
#             Add support for unrecognized files (use TexLexer by default)
#
# To install, see README File
#
# WARNING: Be very sure that the directory to which you apply this contains the correct
#           files you want to highlight. This can be a major security flaw if you share
#           scripts and other files you don't intend to.

import cgi
import pygments
from os import path
from pygments import lexers
from pygments import formatters

filename = cgi.os.environ["PATH_TRANSLATED"]
title = path.basename(filename)
file = open(filename, 'r')
lines = file.readlines()
file.close()
content = "".join(lines)

# check whether we need to download it
form = cgi.FieldStorage()
if form.has_key("action") and form["action"].value == "download":
    print """Content-disposition: attachment; filename=%s
             Content-type: text/plain\
             %s""" % (title, content)
    exit()

style = formatters.HtmlFormatter().get_style_defs('.highlight') 

print """Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>%s</title>
<style type="text/css">
body {
    margin: 0;
    padding: 0;
}
#header {
    width: 100%%;
    background-color: #aab3a3;
    margin: 0;
    padding: 0;
}
#header h3 {
    font-family: "Courier", "Courier New", monospace;
    color: #ffffff;
    margin: 0;
    padding: 0;
    padding-left: 0.5em;
}
#header h3 span {
    font-size: 60%%;
}
.highlighttable {
    padding: 0;
    margin: 0;
    font-family: "Courier", "Courier New", monospace;
    line-height: auto;
}
.highlighttable .linenos {
    background-color: #dddddd;
    padding-left: 0.2em;
    padding-right: 0.2em;
    margin: 0.0em;
}
.hightlighttable .linenos pre {
    font-family: "Courier", "Courier New", monospace;
    line-height: auto;
}
%s
</style>
</head>
<body class="highlight">
""" % (title, style)

print """
<div id="header">
  <h3>%s
  <span> (<a href="%s?action=download">download</a>)</span>
  <span> (<a href="%s/../">back</a>)</span>
  </h3>
</div>
""" % (title, title, title)

formatter = formatters.HtmlFormatter(linenos='table')
try:
  lexer = lexers.guess_lexer_for_filename(filename, content)
  print pygments.highlight(content, lexer, formatter)
except:
  print pygments.highlight(content, lexers.TextLexer(), formatter)


print "</body>"
print "</html>"
