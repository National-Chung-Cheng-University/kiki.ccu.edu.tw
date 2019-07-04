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
      <title>�P�Z�ǥͧ妸�[�� - $Dept{cname}</title>
    </head>
    <body background=$GRAPH_URL/ccu-sbg.jpg>
      <center>
      <img src=$GRAPH_URL/open.jpg>
      <p>
      <H1>
        �P�Z�ǥͧ妸�[��
      </H1>
      <HR>
      <form method=post action=Batch_Add02.cgi>
      <TABLE border=1>
        <TR>
          <TH>�п�ܤW�Ǵ���ؤίZ�O</TH>
          <TH>�п�ܭn��J�����Ǵ���ؤίZ�O</TH>
        </TR>
        <TR>
          <TD>
            ���: <select name=course_id_last>
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
    �Z�O: <SELECT name=course_group_last>
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
             ���: <select name=course_id_now>
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
      <input type=submit value="��ƶ�g����">
      <input type=reset value="���s��g���">
    </form>
    <p>
    </center>
  </body>
  </html>
);
