#!/usr/local/bin/perl

use CGI qw(:standard);

#print("Content-type:text/html\n\n");
print header;
if( param() ) {
  print("name = ", param('name'), "<P>\n");
}


print("lalalaa....");
