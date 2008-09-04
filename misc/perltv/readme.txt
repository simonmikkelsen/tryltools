This is a Perl script I wrote for personal use. It downloades and scrapes the danish
TV programs from dr.dk.

It stores the programs as a html file for each day and uses a Java script to present
different views. You can specify keywords to generate a view that tells what you
want to see.

This has not been tested for some years and the code is spagetti and crap.
Currently it does not seem to work. See below for example:

But hey! If it works for you!

License: GPLv3
Simon Mikkelsen, mikkelsen.tv/simon/

Example of the Java script in the html file:
sord is 1 if one of your keywords matched that program.
utid is the seconds from midnight the program started. Text should be HTML encoded.
Put this javascript after the arry definitions.

tider[1]="07.00";
titel[1]="TV Avisen Morgen&nbsp;";
kanal[1]="DR1";
besk[1]="";
utid[1] = 25200;
sord[1]=0;

tider[2]="09.05";
titel[2]="&nbsp;Derhjemme&nbsp; (3)&nbsp;&nbsp;&nbsp; (G)";
kanal[2]="DR1";
besk[2]="F<E5> hj<E6>lp med de praktiske problemer derhjemme.";
utid[2] = 32700;
sord[2]=0;

