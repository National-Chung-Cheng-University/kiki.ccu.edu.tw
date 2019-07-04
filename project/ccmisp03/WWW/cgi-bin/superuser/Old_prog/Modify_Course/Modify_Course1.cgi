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
 <html><head><title>�}�ƽҨt��--�ק��Ǵ��w�}���</title></head>
 <body background=$GRAPH_URL/ccu-sbg.jpg>
   <center>
    <br>
    <table border=0 width=40%>
     <tr>
      <td>�t�O:</td><td> $dept{cname} </td>
      <td>�~��:</td><td> $input{grade} </td></tr><tr>
      <th colspan=4><H1>�ק��Ǵ��w�}���</H1></th>
     </tr>
    </table>
    <hr width=80%>
    ��ܦ��~�Ŭ��
    <TABLE border=0>
     <tr><td>
      <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="1">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" �@ ">
      </FORM>
     </td><td>
      <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="2">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" �G ">
      </FORM>
     </td><td>
      <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="3">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" �T ">
      </FORM>
     </td><td>
        <FORM action="Modify_Course1.cgi" method=POST>
        <input type=hidden name="dept_id" value=$input{dept_id}>
        <input type=hidden name="grade" value="4">
        <input type=hidden name="password" value=$input{password}>
        <input type=submit value=" �| ">
      </FORM>
     </td></tr>
    </TABLE>

);

#foreach $k (keys %input) {
#  print("$k --> $input{$k}<br>");
#}

print qq(
  �K�Q�K�~�ײĤ@�����}��ئC��
  <FORM action="Modify_Course2.cgi" method="POST">
    <input type=hidden name="dept_id" value=$input{dept_id}>
    <input type=hidden name="grade" value=$input{grade}>
    <input type=hidden name="password" value=$input{password}>
  <table border=1>
    <tr bgcolor=yellow>
      <th>�R��</th><th>�ק�</th><th>��ؽs��</th><th>�Z�O</th>
      <th>����ݩ�</th><th>�}�ұЮv</th><th>��ؤ���W��</th>
    </tr>
);

@course = Find_All_Course($input{dept_id}, $input{grade}, "");

my %cname = ( "1" => "����",
              "2" => "���",
              "3" => "�q��",
              "4" => "�ǵ{"  );
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
   <input type=submit value="�T�{">
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
      <input type=submit value="��ܤW�Q����ظ��">
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
      <input type=submit value="��ܤU�Q����ظ��">
    </FORM>
    </td>
  );
}
print("</tr></table>");


Links3($input{dept_id} ,$input{grade}, $input{password});
