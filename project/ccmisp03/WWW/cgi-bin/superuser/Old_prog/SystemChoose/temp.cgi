#!/usr/local/bin/perl 

require "../../library/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."GetInput.pm";

%Change_School = Find_Change_School_Student();  ## 讀入轉學生名單

my($dept,$count,$i,$flag);

if(-e $BIN_PATH."SystemChoose/Filter.Full")
{
 open(LOG,"< $BIN_PATH"."SystemChoose/Filter.Full");
  @Courses = <LOG>;
  chop(@Courses);
 close(LOG);

 $i=0;
 foreach $course(@Courses)
 {
  $i++;
  ($course{dept},$course{id},$course{group},$temp) = split(/\s+/,$course);
  print "\n------處理第$i門科目中------\n";
  print "系所:$course{dept},科目代碼:$course{id},班別:$course{group}\n";
  Handle();
 }
}
else
{
 print "Error openning file:$BIN_PATH"."SystemChoose/Filter.Full\n";
}
sub Handle
{
 my(@Lines,$i,$count,$temp,$id,$grade,$flag,%s);
 if(-e $LOG_PATH."/$course{id}"."_$course{group}")
 {
  open(LOG,$LOG_PATH."/$course{id}"."_$course{group}");
   @Lines = <LOG>;
   chop(@Lines);
  close(LOG);
  $count = @Lines;
  for($i=1;$i<$count;$i++)
  {
   ($id,$temp,$grade,$temp,$flag,$temp)=split(/\s+/,$Lines[$i]);
   if($Change_School{$id} eq "1" && $grade ne "1")
   {
    print "轉學生:$id,$grade,$flag\n";
    $s{id}=$id;
   }
  }
 }
 else
 {
  print "Error opening file:$LOG_PATH"."/$course{id}"."_$course{group}\n";
 }
}

sub HTML_Head
{
 my($title);
 ($title)=@_;
 print << "HTML_HEAD"
Content-type: text/html


<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=big5">
 <title>$title</title>
</head>
HTML_HEAD 
}