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
    <head>
      $EXPIRE_META_TAG
      <title>科目批次選課作業 - $Dept{cname}</title>
    </head>
    <body background="$GRAPH_URL/ccu-sbg.jpg">
      <center>
      <img src="$GRAPH_URL/open.jpg"><p>
      <h4>同班學生批次加選</h4><p>
      <h4>請選擇上學期科目及班別</h4><p><br>
      <form method=post action=Course_Batch_Add02.cgi>
        <table border=0>
          <tr>
          <th><h3>科目:</h3></th><td><select name=course_id>
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
  <INPUT type=radio name=add_or_delete value="add">加選    
  <INPUT type=radio name=add_or_delete value="delete" checked>退選<br>

  <INPUT type=radio name=property value="1">必修
  <INPUT type=radio name=property value="2">選修
  <INPUT type=radio name=property value="3">通識
  <br>

  <input type=\"submit\" value=\"資料填寫完畢\">
  <input type=\"reset\" value=\"重新填寫資料\">

  </form>
  <p>

  </center>
  </body>
  </html>
);
