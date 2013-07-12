#!/usr/bin/perl

use strict;

MAIN: {
  my ($cmd, $ip);
  $cmd = "/usr/bin/host";

  open (INFILE, "./ip_list.txt");

  while ($ip = <INFILE>) {
	$ip =~ s/^\s+|\s$+//g;
  	my @rst = split (/\s/, `$cmd $ip`);
	chop ($rst[4]);
  	print "$ip, $rst[4]\n";
  }
  close INFILE;
} # End Main
