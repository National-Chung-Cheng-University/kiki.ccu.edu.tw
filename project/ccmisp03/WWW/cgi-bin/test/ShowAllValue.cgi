#!/usr/local/bin/perl -w

require "../library/Reference.pm";

require $LIBRARY_PATH."GetInput.pm";

%InputForm=User_Input();

## Begin of HTML ##
print "Content-type: text/html","\n\n";

print "
<html>
<head>
</head>

<body>";

foreach $key(keys %InputForm){
    print $key,"=",$InputForm{$key},"<br>";
}


print "</body></html>";





