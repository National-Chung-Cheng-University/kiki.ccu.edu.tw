#!/usr/local/bin/perl

#################################################################
#####  Show_all_support_course.cgi
#####  �䴩�q�Ѭ�ؤ@���� -- ��X�Ҧ����䴩�q�Ѫ����
#####  Coder: Nidalap
#####  Date : Nov17, 2000
#################################################################
print("Content-type: text/html\n\n");
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Error_Message.pm";

my(%Input,%Student,%Dept);
%Input=User_Input();
%cge = Read_Cge();

print qq(
  <HTML>
    <HEAD><TITLE>�䴩�q�Ѭ�ؤ@����</TITLE></HEAD>
      <BODY background="$GRAPH_URL/bk.jpg">
        <CENTER>
        <H1>�䴩�q�Ѭ�ؤ@����</H1><HR>
        <FORM method="POST" action="Show_all_support_course2.cgi">
          <TABLE border=1>
            <TR><TD>
              �]�A�q�Ѥ��ߩҶ}���
                <INPUT type="radio" name="include_cge" value=1>�O
                <INPUT type="radio" name="include_cge" value=2>�_
            </TD>
            <TR><TD>
            
          </TABLE>
        </FORM>  
              
);
 