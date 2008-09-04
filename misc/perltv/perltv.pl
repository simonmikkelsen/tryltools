#!/usr/bin/perl

$debug = 0;

$dage_frem = 7; #Hent antal dag frem
$start_fra = 0; #Start fra denne dag (0 idag, 1 imorgen)

# + skrives %2B

# TV stations in the order you want. The text strings are the keys given
# in the urls of dr.dk to identify each station.
@prog = (
	"dk1", #DR1
	"td2", #TV2
	"tvd", #TV DK
	"dk2", #DR2
	 "dk3", #TV3
	 "d3+", #TV3+
#	 "dk4", #DK4
#	 "042", #The Voice TV
	 "999", #Kanal 5
	 "t2z", #TV2 Zulu
#	 "041", #TV2 Charlie
	 "dsc", #Discovery
#	 "hlk", #Hallmark
	 "mtv", #MTV
#	 "ngs", #NGC
#	 "tns", #TCM
#	 "vh1" #VH1
#	"dp1", #P1
#	"dp2", #P2
#	"dp3"  #P3
	
);

# Maps the station keys to readable names. &nbsp; is a HTML space that does not break.
@kanaler = ();
$kanaler{"dk1"} = "DR1";
$kanaler{"td2"} = "TV2";
$kanaler{"dk2"} = "DR2";
$kanaler{"tvd"} = "TV&nbsp;DK";
$kanaler{"dp1"} = "P1";
$kanaler{"dp2"} = "P2";
$kanaler{"dp3"} = "P3";
$kanaler{"dk3"} = "TV3";
$kanaler{"d3+"} = "TV3+";
$kanaler{"dk4"} = "DK4";
$kanaler{"042"} = "The Voice TV";
$kanaler{"999"} = "Kanal 5";
$kanaler{"t2z"} = "TV2 Zulu";
$kanaler{"041"} = "TV2 Charlie";
$kanaler{"dsc"} = "Discovery";
$kanaler{"hlk"} = "Hallmark";
$kanaler{"mtv"} = "MTV";
$kanaler{"ngs"} = "NGC";
$kanaler{"tns"} = "TCM";
$kanaler{"vh1"} = "VH1";


#  ! i starten af et søgeord, betyder at strengen (undtagen start!'et)
#skal matche eksakt i titlen, og beskrivelsen medtages ikke
@sord = (
#"Wrestling",
"\\ASimpsons",
"south park",
#"Monty Python",
"Strengt fortroligt",
"Muppet show",
"Troldspejlet",
"Airport",
"Gintberg",
"\\ANettet",
"stand-up.dk",
"Tæskeholdet",
"dilbert",
"hack",
"the osbourns",
"Dark Angel",
"Airline",
"Osbourne",
"crank yankers",
"awful truth",
"awfull truth",
"magic man",
"harddisken",
"Duksedrengen",
"Firefly",
"værste svindlere",
"Drew Carey"
);

#############################################################################

use LWP::Simple;

for ($d = $start_fra; $d < $dage_frem;$d++)
{
undef($ud);

$z = 0;
$ud .= "var tider=new Array;\n";
$ud .= "var sord =new Array;\n";
$ud .= "var titel=new Array;\n";
$ud .= "var utid =new Array;\n";
$ud .= "var kanal=new Array;\n";
$ud .= "var besk =new Array;\n";
$ud .= "\n\n";

#Henter dato og tid
#Sekund, minut, time, dag_i_måned, måned, år, ugedag, dag_i_år
($sec,  $min,  $hour,$mday,	$mon,  $year,$wday,$yday) = localtime(time + $d*24*3600);
$mon++;
#9-32-15-2-3-99-5-91

$year -= 100;
if ($year < 10)
	{ $year = "0$year"; }
if ($mon < 10)
	{ $mon = "0$mon"; }
if ($mday < 10)
	{ $mday = "0$mday"; }

$printud = "Henter for ". &ugedag($wday) ." d. $mday-$mon 20$year\n";
syswrite(STDOUT,$printud,length($printud));

$filnavn = "tv-oversigt-". &ugedag($wday) ."-$mday-$mon-20$year.html";

	#Henter dato og tid for i morgen
	#Sekund, minut, time, dag_i_måned, måned, år, ugedag, dag_i_år
	($secm,  $minm,  $hourm,$mdaym,	$monm,  $yearm,$wdaym,$ydaym) = localtime(time + ($d+1)*24*3600);
	$monm++;
	#9-32-15-2-3-99-5-91
	
	$yearm -= 100;
	if ($yearm < 10)
		{ $yearm = "0$yearm"; }
	if ($monm < 10)
		{ $monm = "0$monm"; }
	if ($mdaym < 10)
		{ $mdaym = "0$mdaym"; }
	
	$printudm = "Gå til ". &ugedag($wday+1) ." d. $mdaym-$monm 20$yearm\n";
	$filnavnm = "tv-oversigt-". &ugedag($wdaym) ."-$mdaym-$monm-20$yearm.html";

#&DaysFromNow=1&PeriodeID=0&GenreGruppeID%5B%5D=0&KanalID%5B%5D=9&Overskriftslinie=
$mainurl = "http://www.dr.dk/nav/programoversigt/n4/epg.asp";
#$mainurl = "http://www.dr.dk/nav/programoversigt/w3c/epg.asp";

for ($hentStation = 0; $hentStation < @prog; $hentStation++)
	{
	$dato = "$year$mon$mday";#ååmmdd
	$kanal = $prog[$hentStation]; #Kanal
	$sord = "";#Søgeord

	$qs = "?seldate=".$d."&seltime=0&media=TV&channel=".$kanal."&submit1=Sort%E9r";
	
	$url = $mainurl . $qs;
	
	$hentetAdOmgange = 1;
	$li = "";

	$liIn = get($url);
	if ($debug) {
		$pu = "	*Main url: ".$url."\n";
		syswrite(STDOUT,$pu,length($pu));
	}

	$li = $liIn;

	@linier = split(/\n/,$li);
	findel();

	$kan_al = $prog[$hentStation];
	$kan_al =~ s/\+/ /g;
	$kan_al =~ s/\%2B/\+/g;

	$printud = "	".$kanaler{$kan_al}." hentet ($hentetAdOmgange)...\n";
	syswrite(STDOUT,$printud,length($printud));
	}

open (FIL,">$filnavn");
print FIL "<html><body>\n\n";
print FIL "<h1>Programoversigt for ". &ugedag($wday) ." d. $mday-$mon 20$year</h1>\n";
print FIL "<a href=\"$filnavnm\">$printudm</a> | ";
print FIL "<style type=\"text/css\">\n<!--\nTD {\n        font-size: small;\n}\n-->\n</style></head>\n";
print FIL "<script language=\"JavaScript\">\n\n";

#Print resultat af søgeord
#@ktider;
#@ktitler;
#@kbesk;
#@kkanal
$day = int($mday);
print FIL $ud;

print FIL "var max=$z;\n";

print FIL "var time = new Date();\n";
print FIL "var hour = time.getHours();\n";
print FIL "var minute = time.getMinutes();\n";
print FIL "var tid = time.getDate();\n";
print FIL "var untid = hour*3600+minute*60;\n";
print FIL "if (tid != $mday)\n";
print FIL "	{\n";
print FIL "	untid += 24*3600;\n";
print FIL "	}\n\n";


print FIL "</script>\n";

print FIL "<script language=\"JavaScript\" src=\"jstv.js\"></script>\n\n";
print FIL "</body>\n</html>";
close FIL;
#Skriver resultatet

} #Slut på for...

sub findel
{

undef(@tider);
undef(@titler);
undef(@besk);
#Start på hvert nyt program
$filt0 = "<td valign=\"top\" width=\"1%\"  class=\"programmer\">";
#Matcher linien med tider
$filt1 = "<td valign=\"top\" width=\"1%\"  class=\"programmer\">";
#ubrugt nu $filt2 = "<font face=\"verdana\"";
#Beskrivelse
$filt3 = "<td valign=\"top\" width=\"98%\" class=\"p_text\">";

$kan_al = $kanaler{$kanal};

#For en anden type filtre - matcher nedenstående kommer der et sæt programmet i det format
#Start på program
$sec_filt0 = "<table border=\"0\" cellpadding=\"1\" cellspacing=\"1\" width=\"100%\"><tr>";
#Linien med tider OG titel
$sec_filt1 = "<td width=\"98%\" valign=\"top\"><a href=\"#\" onclick=\"EPG_PopUp\\('";
#Linien med beskrivelser
$sec_filt3 = "<td valign=\"top\" class=\"p_text\">";
$sec_filt3_2 = "<td class=p_text_border>";

$n = 0;
for ($i = 0; $i <= @linier; $i++)
	{
	if ($linier[$i] =~ /$filt0/)
		{
		$n++;
		}

	if (($linier[$i] =~ /$filt1/))
		{
		$tider[$n] = $linier[$i];
		$tider[$n] =~ s/<([^>]|\n)*>//g;
		$tider[$n] =~ s/  */ /g;
		$tider[$n] =~ s/\A //;
		$tider[$n] =~ s/	//g;
		$tider[$n] = substr($tider[$n],0,5);
		$tider[$n] =~ s/:/\./g;
		$i++;
		$titler[$n] = $linier[$i];
		$titler[$n] =~ s/<([^>]|\n)*>//g;
		$titler[$n] =~ s/  */ /g;
		$titler[$n] =~ s/\A //;
		$titler[$n] =~ s/	//g;
		}
	if ($linier[$i] =~ /$filt3/ or $linier[$i] =~ /$sec_filt3_2/)
		{
		$besk[$n] = $linier[$i];
		$besk[$n] =~ s/<([^>]|\n)*>//g;
		$besk[$n] =~ s/  */ /g;
		$besk[$n] =~ s/\A //;
		$besk[$n] =~ s/\[L\&aelig;s\&nbsp;mere\]//g;
		}

	if ($linier[$i] =~ /$sec_filt0/)
	{
		$n++;
	}
	
	if ($linier[$i] =~ /$sec_filt1/)
	{
		$beskTi = $linier[$i];
		$beskTi =~ s/<([^>]|\n)*>//g;
		$beskTi =~ s/  */ /g;
		$beskTi =~ s/\A //;
		$beskTi =~ s/	//g;
		$tider[$n] = substr($beskTi, 0, 5);
		$titler[$n] = substr($beskTi, 5);
		
		if ($linier[$i] =~ /genuds\.gif/)
		{
			$titler[$n] .= " (G)";
		}
	}

	if ($linier[$i] =~ /$sec_filt3/)
	{
		$besk[$n] = $linier[$i];
		$besk[$n] =~ s/<([^>]|\n)*>//g;
		$besk[$n] =~ s/  */ /g;
		$besk[$n] =~ s/\A //;
		$besk[$n] =~ s/\[L\&aelig;s\&nbsp;mere\]//g;
	}
	
	if ($titler[$n] eq $besk[$n]) { $besk[$n] = "&nbsp;"; }
	}

$timekor = 0;

for ($i = 0; $i <= @tider; $i++)
	{
	if ($tider[$i] and $titler[$i])
		{
		$tider[$i] =~ s/[\n\r]//g;
		$titler[$i] =~ s/[\n\r]//g;
		$kan_al =~ s/[\n\r]//g;
		$besk[$i] =~ s/[\n\r]//g;

		$tider[$i] =~ s/\"/\\\"/g;
		$titler[$i] =~ s/\"/\\\"/g;
		$kan_al =~ s/\"/\\\"/g;
		$besk[$i] =~ s/\"/\\\"/g;

		$besk[$i] =~ s/Amerikansk/Amr\./g;
		$besk[$i] =~ s/amerikansk/amr\./g;
		$kan_al =~ s/TVDanmark1/TVDK 1/;

		$ud .= "tider[$z]=\"$tider[$i]\";\n";
		$ud .= "titel[$z]=\"$titler[$i]\";\n";
		$ud .= "kanal[$z]=\"$kan_al\";\n";
		$ud .= "besk[$z]=\"$besk[$i]\";\n";

		($tim,$mi) = split(/\./,$tider[$i]);
		if ($z > 0)
			{
			($timf,$mif) = split(/\./,$tider[$i-1]);
			if ($tim < $timf)
				{ $timekor = 1; }
			}
			$udim = $tim*3600 + $mi*60 + $timekor*3600*24;
		$ud .= "utid[$z] = $udim;\n";
		$sz = 0;
		for ($c = 0; $c < @sord; $c++)
			{
			if ($sord[$c] =~ /\A\!/)
				{
				if ("!".$titler[$i] eq $sord[$c])
					{
					$sz = 1;
					} #Slut på if søgeord eq titel.
				}
			else
				{
				if (($titler[$i] =~ /$sord[$c]/i) or ($besk[$i] =~ /$sord[$c]/i))
					{
					$sz = 1;
					} #Slut på if søgeord i titel eller besk.
				}
			} #Slut på for $c = ... 
		$ud .= "sord[$z]=$sz;\n";
		$ud .= "\n";
		}
	$z++;
	}

}


####################################################

sub maal
{ #Returnere månedens længde. Tager højde for skudår hvert 4. år.

if ($_[0] == 0) { return 31;}
elsif (($_[0] == 1) and ($year/4 != int($year/4))) { return 28;}
	elsif (($_[0] == 1) and ($year/4 == int($year/4))) { return 29;}
elsif ($_[0] == 2) { return 31;}
elsif ($_[0] == 3) { return 30;}
elsif ($_[0] == 4) { return 31;}
elsif ($_[0] == 5) { return 30;}
elsif ($_[0] == 6) { return 31;}
elsif ($_[0] == 7) { return 31;}
elsif ($_[0] == 8) { return 30;}
elsif ($_[0] == 9) { return 31;}
elsif ($_[0] == 10) { return 30;}
else { return 31;}
}

##################################################
sub ugedag
{
if ($_[0] == 1) { return "man"; }
elsif ($_[0] == 2) { return "tir"; }
elsif ($_[0] == 3) { return "ons"; }
elsif ($_[0] == 4) { return "tors"; }
elsif ($_[0] == 5) { return "fre"; }
elsif ($_[0] == 6) { return "lør"; }
elsif ($_[0] == 0) { return "søn"; }
}
