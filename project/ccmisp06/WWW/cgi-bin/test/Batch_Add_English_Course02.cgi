#!/usr/local/bin/perl

print("Content-type:text/html\n\n");
print('<meta http-equiv="Content-Type" content="text/html; charset=big5">');
print("<CENTER><H1>�s�ͳq�ѭ^�y�ҵ{�妸���J</H1></CENTER><HR>\n");

#################################################################################
#####  �w�g�ѨM�����D�G
#####    * �䴩�t�Ҫ����׽�     5/17(?)
#####  �|���ѨM�����D�G
#####    * ���׮ɬq�u�P�_��t�A�|����Z  <- �ݦ��S���n�F
#####    * 50/75�����ҵ{�İ�P�_  <- done
#####    * ��¦/�j�ƦW��Ū�J�\��|���갵  <- done

require "../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";
require $LIBRARY_PATH . "Student.pm";
require $LIBRARY_PATH . "Student_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";
require $LIBRARY_PATH . "Error_Message.pm";

%Input=User_Input();
$cdept		= "I001";
$property	= "3";
$count = $count_succeed = $count_fail = 0;


foreach $k (keys %Input) {
  ($cid, $group, $sid) = split("_", $k);
  $count++;
  $succeed = Add_Student_Course($sid, $cdept, $cid, $group, $property);
  if( $succeed == 1 ) {
    $count_succeed++;
  }else{
    print("<FONT color=RED>�[�異�ѡG $sid, $cdept, $cid, $group, $property<BR></FONT>\n");
    $count_fail++;
  }
}

print ("�w�i�� $count ���[��A $count_succeed �����\\");
if( $count_fail > 0 ) {
  print("�A$count_fail �����ѡI<BR>\n");
}else{
  print("�C<BR>\n");
}
