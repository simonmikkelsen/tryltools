
if (document.location.search == "?visalle")
	{ document.write("<a href=\"javascript:document.location.search='viskunspecielle';\">Vis kun specielle lister</a><br>"); }
else
	{ document.write("<a href=\"javascript:document.location.search='visalle';\">Vis almindelige programmer</a><br>"); }

//////////HER OG NU////////////////////////////////////////////////////////////////////////////////
document.write("<table border=0 width=100%><tr><td>");
document.write("<table border=1 align=left width=50%><tr><td colspan=4><h2>Lige nu</h2></td></tr>\n<tr><td bgcolor=silver>Tid</td><td bgcolor=silver>Titel</td><td bgcolor=silver>Kanal</td><td bgcolor=silver>Beskrivelse</td></tr>");

var ud = "";

for (i = 1;i <= max;i++)
	{
	if (sord[i] == 1)
		{ var mark = "<blink><font color=red>*</font></blink>"; }
	else
		{ var mark = ""; }
	if (untid >= utid[i] && untid < utid[i+1] && kanal[i] == kanal[i+1])
		{
		ud += "<tr><td nowrap>" + tider[i] + " - "+ tider[i+1] +"</td><td>"+ mark + titel[i] +"</td><td><a href=\"#"+ kanal[i] +"\">"+ kanal[i] +"</a></td><td><input type=\"text\" style=\"width: 18em; border: 0px solid black;\" value=\""+ besk[i] +"\"></td></tr>\n";
		}
	}

document.write(ud+"</table>\n\n");

//////////SØGEORD////////////////////////////////////////////////////////////////////////////////

var sord_tekst = new Array;
var sord_utid  = new Array;


document.write("<table border=1 width=50%><tr><td colspan=4><h2>Søgeordbasserede programmer</h2></td></tr>\n<tr><td bgcolor=silver>Tid</td><td bgcolor=silver>Titel</td><td bgcolor=silver>Kanal</td><td bgcolor=silver>Beskrivelse</td></tr>");
var antal = 0;
for (i = 1;i <= max;i++)
	{
	if (sord[i] == 1)
		{
		var farv = "black";
		if (untid >= utid[i] && kanal[i] == kanal[i+1])
			{ var farv = "silver"; }
		if (untid >= utid[i] && untid < utid[i+1] && kanal[i] == kanal[i+1])
			{ var farv = "blue"; }
		sord_tekst[antal] = "<tr><td nowrap>" + tider[i] + " - "+ tider[i+1] +"</td><td><font color=" + farv + ">"+ titel[i] +"</font></td><td><a href=\"#"+ kanal[i] +"\">"+ kanal[i] +"</a></td><td><input type=\"text\" style=\"width: 18em; border: 0px solid black;\" value=\""+ besk[i] +"\"></td></tr>\n";
		sord_utid[antal] = utid[i];
		antal++;
		}
	}
tael_til = sord_tekst.length;
for (i = 0;i < tael_til;i++)
	{
	var minindex = tael_til-1;
	//Finder det største tal
	for (var n = i;n < tael_til;n++)
		{
		if (sord_utid[n] < sord_utid[minindex])
			{ minindex = n; }
		}
	//Bytter pladser
	var temp = sord_utid[i];
	sord_utid[i] = sord_utid[minindex];
	sord_utid[minindex] = temp;
	
	temp = sord_tekst[i];
	sord_tekst[i] = sord_tekst[minindex];
	sord_tekst[minindex] = temp;

	}

var ud = "";
for (i = 0;i < tael_til;i++)
	{
	ud += sord_tekst[i];
	}
document.write(ud+"</table>\n\n");

document.write("</td></tr></table>\n<hr>\n");

//////////Næste////////////////////////////////////////////////////////////////////////////////
document.write("<table border=0 width=100%><tr><td>");
document.write("<table border=1 align=left width=50%><tr><td colspan=4><h2>Næste</h2></td></tr>\n<tr><td bgcolor=silver>Tid</td><td bgcolor=silver>Titel</td><td bgcolor=silver>Kanal</td><td bgcolor=silver>Beskrivelse</td></tr>");

var ud = "";

for (i = 1;i <= max;i++)
	{
	if (sord[i] == 1)
		{ var mark = "<blink><font color=red>*</font></blink>"; }
	else
		{ var mark = ""; }
	if (untid >= utid[i] && untid < utid[i+1] && kanal[i] == kanal[i+1])
		{
		i++;
		ud += "<tr><td nowrap>" + tider[i] + " - "+ tider[i+1] +"</td><td>"+ mark + titel[i] +"</td><td><a href=\"#"+ kanal[i] +"\">"+ kanal[i] +"</a></td><td><input type=\"text\" style=\"width: 18em; border: 0px solid black;\" value=\""+ besk[i] +"\"></td></tr>\n";
		i--;
		}
	}

document.write(ud+"</table>\n\n");

//////////FILM///////////////////////////////////////////////////////////////////////////////////

document.write("<table border=1><caption><h2>Film</h2></caption>\n<tr><td bgcolor=silver>Tid</td><td bgcolor=silver>Titel</td><td bgcolor=silver>Kanal</td><td bgcolor=silver>Beskrivelse</td></tr>");

var antal = 0;
for (i = 1;i <= max;i++)
	{
	if (utid[i+1] - utid[i] > 75*60)
		{
		var farv = "black";
		if (untid >= utid[i] && kanal[i] == kanal[i+1])
			{ var farv = "silver"; }
		if (untid >= utid[i] && untid < utid[i+1] && kanal[i] == kanal[i+1])
			{ var farv = "blue"; }
		sord_tekst[antal] = "<tr><td nowrap>" + tider[i] + " - "+ tider[i+1] +"</td><td><font color=" + farv + ">"+ titel[i] +"</font></td><td><a href=\"#"+ kanal[i] +"\">"+ kanal[i] +"</a></td><td>"+ besk[i] +"</td></tr>\n";
		sord_utid[antal] = utid[i];
		antal++;
		}
	}
tael_til = sord_tekst.length;
for (i = 0;i < tael_til;i++)
	{
	var minindex = tael_til-1;
	//Finder det største tal
	for (var n = i;n < tael_til;n++)
		{
		if (sord_utid[n] < sord_utid[minindex])
			{ minindex = n; }
		}
	//Bytter pladser
	var temp = sord_utid[i];
	sord_utid[i] = sord_utid[minindex];
	sord_utid[minindex] = temp;
	
	temp = sord_tekst[i];
	sord_tekst[i] = sord_tekst[minindex];
	sord_tekst[minindex] = temp;

	}
var ud = "";
for (i = 0;i < tael_til;i++)
	{
	ud += sord_tekst[i];
	}

document.write(ud);
document.write("</table>\n\n<hr>\n\n");


//////////ALLE///////////////////////////////////////////////////////////////////////////////////
if (document.location.search == "?visalle")
	{
	document.write("<a name=visalle></a><h2>Alle programmer</h2>\n");
	document.write("<h3>"+kanal[1]+ "<font size=-1> - <a href=\"#\">Top</a></font></h3>\n");
	document.write("<table border=1>\n<tr><td bgcolor=silver>Tid</td><td bgcolor=silver>Titel</td><td bgcolor=silver>Beskrivelse</td></tr>");

	var ud = "";

	for (i = 1;i <= max;i++)
		{
		if (tider[i])
			{
			var farv = "black";
			if (untid >= utid[i] && kanal[i] == kanal[i+1])
				{ var farv = "silver"; }
			if (untid >= utid[i] && untid < utid[i+1] && kanal[i] == kanal[i+1])
				{ var farv = "blue"; }

			ud += "<tr><td>" + tider[i] + "</td><td><font color=" + farv + ">" + titel[i] +"</font></td><td>"+ besk[i] +"</td></tr>\n";

			if (i > 1 && kanal[i] != kanal[i-1] && i < max)
				{
				document.write(ud+"</table>\n\n");

				ud = "<a name=\""+ kanal[i] +"\"></a><h3>"+kanal[i]+ "<font size=-1> - <a href=\"#\">Top</a></font></h3>\n";
				ud += "<table border=1>\n<tr><td bgcolor=silver>Tid</td><td bgcolor=silver>Titel</td><td bgcolor=silver>Beskrivelse</td></tr>";
				}
			}
		}

	document.write(ud+"</table>\n\n");
	} //Slut på if false
