#!/usr/local/bin/perl

open(F, "name_list.txt");
@lines = <F>;
open(OUT, ">junk.txt");

foreach $line (@lines) {
  $line =~ s/\t/\t\t/g;
  print OUT $line;
}