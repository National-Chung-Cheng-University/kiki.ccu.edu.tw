#!/usr/local/bin/perl 

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Dept);

%Input=User_Input();
%Dept=Read_Dept($Input{dept_cd});

## Begin of HTML ##
print "Content-type: text/html","\n\n";

print
" <html>
   <head>
    <title>$SUB_SYSTEM_NAME開排課系統--查詢當學期已開科目</title>
   </head>
   <body bgcolor=white background=$GRAPH_URL"."ccu-sbg.jpg>
   <center>
    <br>
    <table border=0 width=50%>
     <tr>
      <td>系別:</td><td> $Dept{cname} </td>
      <td>年級:</td><td> $Input{grade} </td>
      <td>$YEAR年度第$TERM學期</td>
     </tr>
    </table>
   <br>
   <hr width=40%>
   <table border=0 width=30%> 
   <tr><th colspan=4><font size=4 color=brown>顯示此年級科目</font></th>
     </tr><tr>
       <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=1>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=一>
        </form>
      </th>
      <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=2>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=二>
        </form>
      </th>
      <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=3>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=三>
        </form>
      </th>
      <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=4>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=四>
        </form>
      </th>
    </tr>
   </table>
   <hr width=40%><br>
    <Form action=Show_Course_2.cgi method=post>
    <input type=hidden name=password value=$Input{password}>\n";
  
 my(@course,%Course);

  @course = Find_All_Course($Dept{id},$Input{grade},"");
  $temp=@course;
if($temp ne 0)
{
 print "<font size=4>";
 print "共有 $temp 筆開課資料<br><br>\n";
 print "請選擇欲查詢之科目</font><br><br><br>\n";
 print "<select name=id_group>";
  foreach $course (@course) {
 %Course=Read_Course($Dept{id},$$course{id},$$course{group},"");
 print "<option value=$$course{id}_$$course{group}>
        [$$course{id}-$$course{group}]$Course{cname}\n";
 
 
 }
 print "</select>"; 
 print "<br><br>
     <input type=hidden name=dept_cd value=$Dept{id}>
     <input type=hidden name=grade   value=$Input{grade}>
     <input type=submit name=submit value=顯示此科目資料> 
    </Form>";

}
else
{ print "沒有任何開課資料<br>"; }

print "<hr width=40%><br><br>";

Links1($Dept{id},$Input{grade},$Input{password});
print "
   </center>
   </body>
  </html>
";