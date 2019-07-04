#!/usr/local/bin/perl 

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
#require $LIBRARY_PATH."Password.pm";

my(%Input,%Dept);

%Input=User_Input();
%Dept=Read_Dept($Input{dept_cd});

## Begin of HTML ##
print "Content-type: text/html","\n\n";

#print("Hello!!!");
#Check_Dept_Password($Input{dept_cd}, $Input{password});

#foreach $key (keys %Input) {
#  print("$key ---> $Input{$key}<br>");
#}


print qq (
 <html>
   <head>
    <title>��ߤ����j��$SUB_SYSTEM_NAME�}�ƽҨt��--�Ǵ���ض}��</title>
   </head>
   <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <H1><FONT face="�з���">��ߤ����j��<FONT color=RED>$SUB_SYSTEM_NAME</FONT>�}�ƽҨt��--�Ǵ���ض}��</FONT></H1>
    <table border=0 width=60%>
     <tr>
      <td align=left>�t�O: $Dept{cname} </td>
      <td align=center>�~��: $Input{grade} </td>
      <td align=right>$YEAR�~�ײ�$TERM�Ǵ�</td>
     </tr>
    </table>
   <hr width=40%>
   <table border=0 width=30%> 
   <tr><th colspan=4><font size=4 color=brown>��ܦ��~�ž��~���</font></th>
     </tr><tr>
       <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=1>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�@>
        </form>
      </th>
      <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=2>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�G>
        </form>
      </th>
      <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=3>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�T>
        </form>
      </th>
      <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=4>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=�|>
        </form>
      </th>
    </tr>
   </table>
   <hr width=40%>
     <form action=Open_Course_2.cgi method=post>
      <input type=hidden name=dept_cd value=$Dept{id}>
      <input type=hidden name=grade value=$Input{grade}>
      <input type=hidden name=password value="$Input{password}">
      <input type=hidden name=course_cd value=new>
      <input type=submit value=�s�W���> 
     </form>   
  <Form action=Open_Course_2.cgi method=post>
   <input type=hidden name=password value=$Input{password}>
   <table border=0>
   <tr>
   <th>���~�}�Ҹ��</th>
   <th>���Ǵ��}�Ҭ��</th>
   </tr>
   <td>
     <select name=course_cd size=10>
);;
  my(@course,%Course);

  @course = Find_All_Course($Dept{id},$Input{grade},"history");

#  foreach $course (@course) {
#    print("<OPTION value=$$course{id}> [$$course{id} $$course{group} ]");
#  }

  
  foreach $course (@course) {
     if($$course{group} eq "01")  # �u��� 01 �Z�O�����
     {
      %Course=Read_Course($Dept{id},$$course{id},$$course{group},"history");
      print "<option value=$$course{id}>[$$course{id}]$Course{cname}\n";
     }
  }
  @course = Find_All_Course($Dept{id},$Input{grade},"");

  foreach $course (@course) {
     if($$course{group} eq "01")  # �u��� 01 �Z�O�����
     {
         %Course=Read_Course($Dept{id},$$course{id},$$course{group},"");
         print "<option value=\"$$course{id} new\">(���Ǵ�)[$$course{id}]$Course{cname}\n";
     }
  }
print "
     </select>
     </td>
     <td>";
         
print "
     <textarea cols=40 rows=10>\n<<�����ȨѰѦ�,������������>>\n";

 my(@course,%Course);

  @course = Find_All_Course($Dept{id},$Input{grade},"");

  foreach $course (@course) {
    %Course=Read_Course($Dept{id},$$course{id},$$course{group},"");
    print "[$$course{id}-$$course{group}]$Course{cname}\n";
  }
print "</textarea>
     </td>
     </tr></table>
     <input type=hidden name=dept_cd value=$Dept{id}>
     <input type=hidden name=grade   value=$Input{grade}>
     <input type=submit name=submit value=�H����ض}��> 
    </Form>
   <hr>";
Links1($Dept{id},$Input{grade},$Input{password});
print "
   </center>
   </body>
  </html>
";