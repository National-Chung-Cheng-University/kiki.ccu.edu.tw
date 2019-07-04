#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">');
print("<CENTER><H1>新生通識英語課程批次載入</H1></CENTER><HR>\n");

#################################################################################
#####  已經解決的問題：
#####    * 支援系所的必修課     5/17(?)
#####  尚未解決的問題：
#####    * 必修時段只判斷到系，尚未到班  <- 看似沒必要了
#####    * 50/75分鐘課程衝堂判斷  <- done
#####    * 基礎/強化名單讀入功能尚未實做  <- done

require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%Input=User_Input();

 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag ne "TRUE" ) {
   print("Password check error! system logged!!\n");
   exit();
 }


#%Input=User_Input();
$cdept		= "I001";
$property	= "3";
$count = $count_succeed = $count_fail = 0;

#print("yiyooyo");
Print_Hash(%Input);


foreach $k (keys %Input) {
  ($cid, $group, $sid) = split("_", $k);
  $count++;
  $succeed = Add_Student_Course($sid, $cdept, $cid, $group, $property);
  if( $succeed == 1 ) {
    $count_succeed++;
  }else{
    print("<FONT color=RED>Add Fail:  $sid, $cdept, $cid, $group, $property<BR></FONT>\n");
    $count_fail++;
  }
}

print ("$count Records add, $count_succeed succeed.");
if( $count_fail > 0 ) {
  print(", $count_fail failed<BR>\n");
}else{
  print(".<BR>\n");
}
