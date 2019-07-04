#!/usr/local/bin/perl

#############
#####  Test_Password.cgi

require "../library/Reference.pm";
require "../library/Password.pm";
require "../library/GetInput.pm";
require "../library/Error_Message.pm";

print("Content-type:text/html\n\n");

%input = User_Input();
$id		= $input{id};
$password	= $input{password};

Test_Dept_Password($id,$password)  if( $input{select} eq "dept" );
Test_Teacher_Password($id,$password)  if( $input{select} eq "teacher" );
Test_Student_Password($id,$password)  if( $input{select} eq "student" );

###################################################################
sub Test_Dept_Password()
{
  ($id, $password) = @_;

  $salt = Read_Crypt_Salt($id, "dept");
  $password = Crypt($password, $salt);

  print("salt = $salt<br>");
  print("$id ===> $password<br>");
  
  $result = Check_Dept_Password($id, $password);
  print("result = $result");
}
###################################################################
sub Test_Teacher_Password()
{
  ($id, $password) = @_;

  $salt = Read_Crypt_Salt($id, "teacher");
  $password = Crypt($password, $salt);

  print("salt = $salt<br>");
  print("$id ===> $password<br>");

  $result = Check_Teacher_Password($id, $password);
  print("result = $result");
}
###################################################################

sub Test_Student_Password()
{
  ($id, $password) = @_;

  $salt = Read_Crypt_Salt($id, "student");
  $password = Crypt($password, $salt);

  print("salt = $salt<br>");
  print("$id ===> $password<br>");

  $result = Check_Student_Password($id, $password);
  print("result = $result");
}
