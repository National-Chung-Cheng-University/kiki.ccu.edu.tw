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
@Course = Find_All_Course( $Dept{id},"","history" );
$filter = $Input{filter};

print qq(
  <html>
    <head>
      <title>同班學生批次加選 - $Dept{cname}</title>
    </head>
    <body background=$GRAPH_URL/ccu-sbg.jpg>
      <center>
      <img src=$GRAPH_URL/open.jpg>
      <p>
      <H1>
        同班學生批次加選
      </H1>
      <HR>
      <form method=post action=Batch_Add02.cgi>
      <TABLE border=1>
        <TR>
          <TH>請選擇上學期科目及班別</TH>
          <TH>請選擇要轉入的本學期科目及班別</TH>
        </TR>
        <TR>
          <TD>
            科目: <select name=course_id_last>
);

 my($course,%temp,$i,$count);
 $count = @Course;
 for($i=0;$i < $count;$i++) {
   %temp = Read_Course($Dept{id},$Course[$i]{id},$Course[$i]{group},"history","");
   next if( ($filter eq "on") and $temp{id} !~ /210100/ );
   print"<option value=$temp{id}>[$temp{id}]$temp{cname}\n";
 }
print qq(
    </SELECT><P>
    班別: <SELECT name=course_group_last>
);

 for($i=1; $i<=20; $i++) {
   if($i<10) {
     $j = "0" . $i;
   }else{
     $j = $i;
   }
   print("<OPTION value=$j>$j");
 }

print qq(
             </select>
             <input type=hidden name=dept_id value=$Input{dept_id}>
           </TD>
           <TD>
             科目: <select name=course_id_now>
);

 @Course = Find_All_Course( $Dept{id},"","" );
 my($course,%temp,$i,$count);
 $count = @Course;
 for($i=0;$i < $count;$i++) {
   %temp = Read_Course($Dept{id},$Course[$i]{id},$Course[$i]{group},"","");
   next if( ($filter eq "on") and $temp{id} !~ /210100/ );
   $key = $temp{id} . "_" . $temp{group};
   print"<option value=$key>[$temp{id} _ $temp{group}]$temp{cname}\n";
 }

print qq(
             </SELECT>
           </TD>
         </TR>
       </TABLE>
      <input type=submit value="資料填寫完畢">
      <input type=reset value="重新填寫資料">
    </form>
    <p>
    </center>
  </body>
  </html>
);
