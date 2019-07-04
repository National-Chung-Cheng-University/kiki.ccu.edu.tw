#!/usr/local/bin/perl
$|=1;
print "Content-type: text/html","\n\n";
$|=0;
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Dept.pm";
my(%Input,@Dept,@Course,%Dept);

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
@Course = Find_All_Course( $Dept{id},"","" );

print qq(
  <html>
    <head><title>��ا妸��ҧ@�~ - $Dept{cname}</title></head>
    <body background="$GRAPH_URL/ccu-sbg.jpg">
      <center>
      <img src="$GRAPH_URL/open.jpg"><p>
      <h4>�P�Z�ǥͧ妸�[��</h4><p>
      <h4>�п�ܤW�Ǵ���ؤίZ�O</h4><p><br>
      <form method=post action=Course_Batch_Add02.cgi>
        <table border=0>
          <tr>
          <th><h3>���:</h3></th><td><select name=course_id>
);

my($course,%temp,$i,$count);
$count = @Course;
for($i=0;$i < $count;$i++) {
  %temp = Read_Course($Dept{id},$Course[$i]{id},$Course[$i]{group},"","");
  print"<option value=$temp{id}_$temp{group}>[$temp{id}-$temp{group}]$temp{cname}\n";
}

print qq(
  </select>
  <input type=hidden name=dept_id value=$Dept{id}>
  </td>
  </tr>
  </table>
  <INPUT type=radio name=add_or_delete value="add">�[��    
  <INPUT type=radio name=add_or_delete value="delete" checked>�h��<br>
  <input type=\"submit\" value=\"��ƶ�g����\">
  <input type=\"reset\" value=\"���s��g���\">

  </form>
  <p>

  </center>
  </body>
  </html>
);
