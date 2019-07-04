#!/usr/local/bin/perl

print("Content-type:text/html\n\n");

use CGI qw(:standard);
$query = new CGI;

$File_Handle = $query->param(file);
print("file handle = $File_Handle<br>\n");
$outfile = $File_Handle;
$outfile =~ s/.*\\//g;
print("outfile = $outfile<br>\n");
open(FILE, ">$outfile");

while ($Buffer = <$File_Handle>) {
#while ($Bytes = read($File_Handle,$Buffer,1024)) {
 $BytesRead += $Bytes;
 $Buffer =~ s/\s+$//;
 print FILE ("$Buffer\n");
# print $Buffer;
}

close FILE;
print("The text you gave to me are written into file \"test.txt\"");
