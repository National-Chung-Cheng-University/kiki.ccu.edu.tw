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
    <title>$SUB_SYSTEM_NAME�}�ƽҨt��--�d�߷�Ǵ��w�}���</title>
   </head>
   <body bgcolor=white background=$GRAPH_URL"."ccu-sbg.jpg>
   <center>
    <br>
    <table border=0 width=50%>
     <tr>
      <td>�t�O:</td><td> $Dept{cname} </td>
      <td>�~��:</td><td> $Input{grade} </td>
      <td>$YEAR�~�ײ�$TERM�Ǵ�</td>
     </tr>
    </table>
   <br>
   <hr width=40%>
   <table border=0 width=30%> 
   <tr><th colspan=4><font size=4 color=brown>��ܦ��~�Ŭ��</font></th>
     </tr><tr>
       <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=1>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�@>
        </form>
      </th>
      <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=2>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�G>
        </form>
      </th>
      <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=3>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�T>
        </form>
      </th>
      <th>
        <form action=Show_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=4>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�|>
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
 print "�@�� $temp ���}�Ҹ��<br><br>\n";
 print "�п�ܱ��d�ߤ����</font><br><br><br>\n";
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
     <input type=submit name=submit value=��ܦ���ظ��> 
    </Form>";

}
else
{ print "�S������}�Ҹ��<br>"; }

print "<hr width=40%><br><br>";

Links1($Dept{id},$Input{grade},$Input{password});
print "
   </center>
   </body>
  </html>
";