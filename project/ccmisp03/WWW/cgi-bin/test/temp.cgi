#!/usr/local/bin/perl

print("Content-type:text/html\n\n");

use CGI qw(:standard);
$query = new CGI;

$File_Handle = $query->param(file);
print("file handle = $File_Handle<br>\n");
open(FILE, ">test.txt");

while ($Bytes = read($File_Handle,$Buffer,1024)) {
 $BytesRead += $Bytes;
 print FILE $Buffer;
 print $Buffer;
}

close FILE;
print("The text you gave to me are written into file \"test.txt\"");
