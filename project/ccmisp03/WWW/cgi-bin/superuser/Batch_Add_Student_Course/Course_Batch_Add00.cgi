#!/usr/local/bin/perl
print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."GetInput.pm";

%Input = User_Input();

print qq(
  <html>
   <head><title>�ĤG���}�ƽҨt�� �޲z�t��</title></head>
   <body background="$GRAPH_URL/ccu-sbg.jpg">
     <center>
     <img src="$GRAPH_URL/open.jpg"><P>
     <h4>��ا妸�[��</h4><P>
     <h4>�п�ܨt��</h4><p><br>
     <form method=post action=Course_Batch_Add01.cgi>
       <table border=0>
         <tr>
         <th><h3>�t�O:</h3></th><td><select name=dept_id>
);

my(@Dept,$dept,%Dept);
@Dept=Find_All_Dept();
foreach $dept(@Dept) {
  %Dept=Read_Dept($dept);
  print "<option value=$Dept{id}>$Dept{cname}\n";
}

print qq(
      </select>
      </td>
      </tr>
      <INPUT type=hidden name=password value=$Input{password}>
      <INPUT type=hidden name=grade value=1>
    </table>
      <input type=\"submit\" value=\"��ƶ�g����\">
      <input type=\"reset\" value=\"���s��g���\">
    </form><p>
    </center>
    </body>
  </html>
);
