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
    <title>國立中正大學$SUB_SYSTEM_NAME開排課系統--學期科目開課</title>
   </head>
   <body bgcolor=white background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <H1><FONT face="標楷體">國立中正大學<FONT color=RED>$SUB_SYSTEM_NAME</FONT>開排課系統--學期科目開課</FONT></H1>
    <table border=0 width=60%>
     <tr>
      <td align=left>系別: $Dept{cname} </td>
      <td align=center>年級: $Input{grade} </td>
      <td align=right>$YEAR年度第$TERM學期</td>
     </tr>
    </table>
   <hr width=40%>
   <table border=0 width=30%> 
   <tr><th colspan=4><font size=4 color=brown>顯示此年級歷年科目</font></th>
     </tr><tr>
       <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=1>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=一>
        </form>
      </th>
      <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=2>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=二>
        </form>
      </th>
      <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=3>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=三>
        </form>
      </th>
      <th>
        <form action=Open_Course_1.cgi method=post>
         <input type=hidden name=dept_cd value=$Dept{id}>
         <input type=hidden name=grade value=4>
         <input type=hidden name=password value=$Input{password}>
         <input type=submit value=四>
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
      <input type=submit value=新增科目> 
     </form>   
  <Form action=Open_Course_2.cgi method=post>
   <input type=hidden name=password value=$Input{password}>
   <table border=0>
   <tr>
   <th>歷年開課資料</th>
   <th>本學期開課科目</th>
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
     if($$course{group} eq "01")  # 只顯示 01 班別的資料
     {
      %Course=Read_Course($Dept{id},$$course{id},$$course{group},"history");
      print "<option value=$$course{id}>[$$course{id}]$Course{cname}\n";
     }
  }
  @course = Find_All_Course($Dept{id},$Input{grade},"");

  foreach $course (@course) {
     if($$course{group} eq "01")  # 只顯示 01 班別的資料
     {
         %Course=Read_Course($Dept{id},$$course{id},$$course{group},"");
         print "<option value=\"$$course{id} new\">(本學期)[$$course{id}]$Course{cname}\n";
     }
  }
print "
     </select>
     </td>
     <td>";
         
print "
     <textarea cols=40 rows=10>\n<<本欄位僅供參考,不必於本欄填選資料>>\n";

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
     <input type=submit name=submit value=以此科目開課> 
    </Form>
   <hr>";
Links1($Dept{id},$Input{grade},$Input{password});
print "
   </center>
   </body>
  </html>
";