#!/usr/local/bin/perl

require("../library/Reference.pm");
require("../library/Course.pm");
require("../library/GetInput.pm");
require("../library/Error_Message.pm");
print "Content-type: text/html","\n\n";

%input = User_Input();

print("<H1>This is a test of accessing course data</H1>\n");

Show_All_Course()      if( $input{request} eq "Find_All_Course");
Read_One_Course()      if( $input{request} eq "Read_One_Course");
Read_All_Course_Data() if( $input{request} eq "Read_All_Course_Data");
Add_Course_Data()      if( $input{request} eq "Add_Course");
Delete_Course_Data()   if( $input{request} eq "Delete_Course");

###########################################################################
sub Show_All_Course()
{
  print("$input{dept}系所$input{grade}年級開課所有科目代碼班別:");
  @course = Find_All_Course($input{dept}, $input{grade});
  print("<table border=3>");
  foreach $course (@course) {
    print("<tr>");
    print("<td>$$course{id}</td> <td>$$course{group}</td>");
    print("</tr>");
  }
  print("</table>");
}
###########################################################################
sub Read_One_Course()
{
   print("<HR>\n");
   %course = Read_Course($input{dept},$input{id},$input{group});
   print("<table border=3>");
   print("<tr><td>id</td><td>$course{id}</td></tr>");
   print("<tr><td>group</td><td>$course{group}</td></tr>");
   print("<tr><td>dept </td><td>$course{dept} </td></tr>");
   print("<tr><td>cname</td><td>$course{cname}</td></tr>");
   print("<tr><td>ename</td><td>$course{ename}</td></tr>");
   print("<tr><td>grade</td><td>$course{grade}</td></tr>");
   print("<tr><td>credit</td><td>$course{credit}</td></tr>");
   print("<tr><td>classroom</td><td>$course{classroom}</td></tr>");
   print("<tr><td>teacher</td>");
   foreach $teacher (@{$course{teacher}}) {
     print("<td>$teacher</td>");
   } print(" </tr>");
   print("<tr><td>property</td><td>$course{property}</td></tr>");
   print("<tr><td>number_limit</td><td>$course{number_limit}</td></tr>");  

   print("<tr><td>support_dept</td>");
   foreach $ele (@{$course{support_dept}}) {    
     print("<td>$ele</td></tr>");
   } print(" </tr>");

   print("<tr><td>support_grade</td>");
   foreach $ele (@{$course{support_grade}}) {
     print("<td>$ele</td></tr>");
   } print(" </tr>");

   print("<tr><td>support_class</td>");
   foreach $ele (@{$course{support_class}}) {
     print("<td>$ele</td></tr>");
   } print(" </tr>");

   print("<tr><td>ban_dept</td>");
#   print("<td>$course{ban_dept}</td></tr>");
   foreach $ele (@{$course{ban_dept}}) {
     print("<td>$ele</td></tr>");
   } print(" </tr>");

   print("<tr><td>ban_grade</td>");
   foreach $ele (@{$course{ban_grade}}) {
     print("<td>$ele</td></tr>");
   } print(" </tr>");

   print("<tr><td>ban_class</td>");
   foreach $ele (@{$course{ban_class}}) {
     print("<td>$ele</td></tr>");
   } print(" </tr>");

   print("<tr><td>total_time</td><td>$course{total_time}</td></tr>");

#   print("<tr><td>time</td><td>$course{time}</td></tr>");
   print("<tr><td>time</td><td>");
   foreach $ele (@{$course{time}}) {
     print("[$$ele{week},$$ele{time}] ;");
   } print("</td> </tr>");

   print("<tr><td>reserved_number</td><td>$course{reserved_number}</td></tr>");
   print("<tr><td>principle</td><td>$course{principle}</td></tr>");
   print("<tr><td>note</td><td>$course{note}</td></tr>");

   print("</table>");
}
##########################################################################
sub Read_All_Course_Data()
{
  @course = Find_All_Course($input{dept}, $input{grade});
  print("<table border=3>");
  foreach $course (@course) {
    %course = Read_Course($input{dept},$$course{id},$$course{group});
    print("<table border=3>");
    foreach $key (sort keys %course) {
      if( ($course{$key} !~ /ARRAY/) and ($course{$key} !~ /HASH/) ) {
         print("<tr><td>$key</td> <td>$course{$key}<td></tr>");
      }
      if( $key eq "teacher" ) {
        foreach $v (@{$course{$key}}){
          print("<tr><td>$key</td><td>$v</td></tr>\n");
        }
      }
      if( $key eq "time" ) {
        print("<tr><td>time</td><td>");
        foreach $aaa (@{$course{$key}} ) {
          print("[ $$aaa{week}, $$aaa{time}] ,");
        }
        print("</td>.");
      }
    }
    print("</table>");
  }
}
###########################################################################
sub Add_Course_Data()
{
  %course = %input;
  print("Hello!");
 
  $course{time}[0]{week} = $input{time_w1};
  $course{time}[0]{time} = $input{time_t1};
  $course{time}[1]{week} = $input{time_w2};
  $course{time}[1]{time} = $input{time_t2};
  $course{time}[2]{week} = $input{time_w3};
  $course{time}[2]{time} = $input{time_t3};
  $course{time}[3]{week} = $input{time_w4};
  $course{time}[3]{time} = $input{time_t4};
  
  $result = Modify_Course( $input{selection} , %course);
  print("<H1>Result = $result</H1>");
}
###########################################################################
sub Delete_Course_Data()
{
  %course = %input;
  
  $result = Delete_Course( $course{id}, $course{group}, $course{dept});
  print("<h1>The result of Delete_Course() is <font color=RED>$result</font>");

}
