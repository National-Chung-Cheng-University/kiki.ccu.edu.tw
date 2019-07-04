#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";

print("Content-type:text/html\n\n");
%input = User_Input();
%dept  = Read_Dept($input{dept_id});
@teacher = Read_Teacher_File();

$input{page} = 1  if( not defined $input{page} );

#foreach $k (keys %input) {
#  print("$k ---> $input{$k}<br>");
#}
Check_Dept_Password($input{dept_id}, $input{password});

print qq(
 <html><head><title>開排課系統--修改當學期已開科目</title></head>
 <body background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <br>
    <table border=0 width=40%>
     <tr>
      <td>系別:</td><td> $dept{cname} </td>
      <td>年級:</td><td> $input{grade} </td></tr><tr>
      <th colspan=4><H1>修改當學期已開科目</H1></th>
     </tr>
    </table>
    <hr width=80%>
    顯示此年級科目
    <TABLE border=0>
     <tr><td>
      <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="1">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 一 ">
      </FORM>
     </td><td>
      <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="2">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 二 ">
      </FORM>
     </td><td>
      <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="3">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 三 ">
      </FORM>
     </td><td>
        <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="4">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" 四 ">
      </FORM>
     </td></tr>
    </TABLE>

);

#foreach $k (keys %input) {
#  print("$k --> $input{$k}<br>");
#}

print qq(
  八十八年度第一學擬開科目列表
  <FORM action="Modify_Course2.cgi" method="POST">
    <input type=hidden name="dept_id" value=$input{dept_id}>
    <input type=hidden name="grade" value=$input{grade}>
    <input type=hidden name="password" value=$input{password}>
  <table border=1>
    <tr bgcolor=yellow>
      <th>刪除</th><th>修改</th><th>科目編號</th><th>班別</th>
      <th>科目屬性</th><th>開課教師</th><th>科目中文名稱</th>
    </tr>
);

@course = Find_All_Course($input{dept_id}, $input{grade}, "");

my %cname = ( "1" => "必修",
              "2" => "選修",
              "3" => "通識",
              "4" => "學程"  );
$record_count = 0;
foreach $course (@course) {
  if( ($record_count>=($input{page}*10-10)) and ($record_count<=($input{page}*10-1)) ) {
    $course_id_and_group = $$course{id} . ":::" . $$course{group};
    %course = Read_Course($input{dept_id}, $$course{id}, $$course{group}, "");
    print qq(
      <tr>
        <td align=center>
          <INPUT name="choice" type="radio" value="DELETE:::$course_id_and_group">
        </td>
        <td align=center>
          <INPUT name="choice" type="radio" value="MODIFY:::$course_id_and_group">
        </td>
        <td align=center> $$course{id} </td>
        <td align=center> $$course{group} </td>
        <td align=center> $cname{$course{property}} </td>
        <td align=center> 
    );
    foreach $teacher( @{ $course{teacher} } ) {
       print $Teacher_Name{ $teacher },"<br>\n";
    }
    print qq(
        </td>
        <td align=left> $course{cname} </td>
       
      </tr>
    );
  }
#  print("<tr><td>$$course{id}</td></tr>");
  $record_count++;
}

$num_of_course = @course;
$next_page = $input{page}+1;
$prev_page = $input{page}-1;
print qq(
   </table>
   <input type=submit value="確認">
  </FORM>  
);

print("<table border=0><tr>");
if( $input{page} > 1 ) {
  print qq(
    <td> 
    <FORM action=Modify_Course1.cgi method=post>
      <input type=hidden name=dept_id value=$input{dept_id}>
      <input type=hidden name=grade   value=$input{grade}>
      <input type=hidden name=password value=$input{password}>
      <input type=hidden name=page value=$prev_page>
      <input type=submit value="顯示上十筆科目資料">
    </FORM>
    </td>
  );
}

if( $num_of_course>$input{page}*10 ) {
  print qq( 
    <td>
    <FORM action=Modify_Course1.cgi method=post>
      <input type=hidden name=dept_id value=$input{dept_id}>
      <input type=hidden name=grade   value=$input{grade}>
      <input type=hidden name=password value=$input{password}>
      <input type=hidden name=page value=$next_page>
      <input type=submit value="顯示下十筆科目資料">
    </FORM>
    </td>
  );
}
print("</tr></table>");


Links3($input{dept_id} ,$input{grade}, $input{password});
