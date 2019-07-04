#!/usr/local/bin/perl 

print "Content-type: text/html","\n\n";

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."System_Settings.pm";

%Input = User_Input();
%Dept = Read_Dept($Input{dept_id});
$dept = $Input{dept_id};
($course_id,$group) = split(/_/,$Input{course_id});

if( ($course_id eq "") or ($group eq "") ) {
  print("錯誤！找不到科目！！");
  exit();
}

%Course = Read_Course($dept,$course_id,$group,"", "");

#foreach $k (keys %Input) {
#  print("$k -> $Input{$k}<br>");
#}

@student = Student_in_Course($dept, $course_id, $group, "");
$student_number = @student;

print qq(
  <html>
    <head>
      $EXPIRE_META_TAG	
      <title>科目批次選課作業 - $Dept{cname}</title>
    </head> 
    <body background="$GRAPH_URL/ccu-sbg.jpg">
      <center>
      <img src="$GRAPH_URL/open.jpg"><p>
  <center><h1>科目選課作業</h1></center>
  科目代碼: $course_id<br>
  科目班別: $group<br>
  科目名稱: $Course{cname}<br>
  科目限修: $Course{number_limit}<br>
  修課人數: $student_number<br>
  <hr>
  <FORM method=POST action="Course_Batch_Add03.cgi">
    <INPUT type=hidden name=dept value=$dept>
    <INPUT type=hidden name=course_id value=$course_id>
    <INPUT type=hidden name=group value=$group>
);

if($Input{add_or_delete} eq "add")  {
  Show_Add_Table();
}elsif($Input{add_or_delete} eq "delete") {
  Show_Delete_Table();
}
print("</FORM>");
################################################################################
sub Show_Delete_Table() 
{
  print qq(
    <INPUT type=hidden name="add_or_delete" value="delete">
    <TABLE border=1>
      <TR><TD>退選</TD><TD>學號</TD><TD>姓名</TD><TD>系所班級</TD><TD>學分歸屬</TD></TR>
  );

  foreach $student (@student) {
    %student = Read_Student($student);
    print qq(
      <TR><TD align=center><INPUT type=checkbox name="$student"></TD>
      <TD>$student</TD><TD>$student{name}</TD><TD>$student{dept}</TD><TD></TD></TR>
    );
  }
  print qq(
      </TABLE>
      <INPUT type=submit value="進入退選確認畫面">
  );

}
########################################################################################
sub Show_Add_Table()
{
  print qq(
    <TABLE border=1>
      <TR align=CENTER valign=TOP>
        <TD>
  );
  Show_Add_Table1();
  print("</TD><TD>");
  Show_Add_Table2();
  print qq(
        </TD>
      </TR>
    </TABLE>
  );
  

}
########################################################################################
sub Show_Add_Table1()
{
  print qq(
    <TABLE border=1>
      <TR>
        <TD colspan=2 bgcolor=YELLOW>
          <INPUT type=radio name="add_or_delete" value="add1">替以下學生加選
        </TD>
      </TR>
      <TR><TD>學號</TD><TD>學分歸屬</TD></TR>
  );
  @Credit_table = CREDIT_TABLE();
  $ctable_size  = @Credit_table;
  for($count=0; $count<50; $count++) {
    $id       = $count . "_id";
    $property = $count . "_property";
    print qq(
      <TR><TD><INPUT name=$id></TD>
      <TD><SELECT name=$property>
    );
    for($i=0; $i<$ctable_size; $i++) {
      if( $i == $Input{property} ) {
        print("<OPTION value=$i SELECTED>$Credit_table[$i]");
      }else{
        print("<OPTION value=$i>$Credit_table[$i]");
      }
    }
    print qq(  
      </SELECT></TD></TR>
    );
  }
  
  print qq(
    </TABLE>
    <INPUT type=submit value="進入加選確認畫面">
  );
}
#########################################################################################
sub Show_Add_Table2()
{
  print qq(
    <TABLE border=1>
      <TR>
        <TD colspan=2 bgcolor=YELLOW>
          <INPUT type=radio name="add_or_delete" value="add2">或是, 替以下學生加選
        </TD>
      </TR>
      <TR><TD>
        學分歸屬: $PROPERTY_TABLE2{$Input{property}}<BR>
        學號清單:<BR>
          <TEXTAREA name=id_list cols=30 rows=50></TEXTAREA>
      </TD></TR>
      <INPUT type=hidden name=property value=$Input{property}>
  );


}

