#!/usr/local/bin/perl
##########################################################################
#####   Create_Password1.cgi
#####   �妸���ͷs�ͱK�X
#####   Coder: Nidalap
#####   Date : 2001/08/09
#####   Note : ��F���O�����H���K�X, ���~�אּ�w�]�������Ҹ�
#####          �t��Ū���U�t�ҹw�w�Ǹ��d��, �M��̷Ӹӽd�򲣥ͷs�ͱK�X.
##########################################################################
print("Content-type:text/html\n\n");
require "../../../../LIB/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
$fs = "<FONT size=2>";

%Input = User_Input();

#$result = Check_SU_Password($Input{password}, "su", "su");
#if( $result ne "TRUE" ) {
#  print("Password Check Error!!");
#  exit(0);
#}

print qq (
  <HEAD><TITLE>���ͷs�ͱK�X</TITLE></HEAD>
  <BODY>
    <CENTER>
      <H1>���ͷs�ͱK�X -- �B�J1/3</H1>
      <HR>
      <FORM action="Create_Password2.cgi" method=POST>
      
      �Цb�H�U��줤��J�U�t�ҹw�p�_�W�Ǹ�:
      <TABLE border=0><TR><TD width=80%>
      
      <TABLE border=0>
        <TR>
          <TH width=50% bgcolor=YELLOW>�U�t�ҹw�p�_�W�Ǹ�</TH>
          <TH width=50% bgcolor=YELLOW>�榡�d��</TH>
        </TR>
        <TR>
          <TD><TEXTAREA name="input" rows=15 cols=50></TEXTAREA></TD>
          <TD valign=TOP>
          <FONT size=2 color=RED>
           * �@�欰�@�Ӱ_�W, �t�αN���Ͱ_���쨴�����Ҧ��K�X.<BR>
           * �t�һP�Ǹ������n�Τ@�өΦh�ӥb�Ϊťչj�}.<BR>
           * �Ǹ��_�W�H "~" ���j, ���i�t�ťզr��<BR>
          </FONT>
          <HR>
          $fs
          ����t  &nbsp&nbsp&nbsp488110055~488110063<BR>
          �~��t  &nbsp&nbsp&nbsp488115055~488115062<BR>
          ��u�t  &nbsp&nbsp&nbsp488410055~488410066<BR>
          ����t  &nbsp&nbsp&nbsp488420102~488420115<BR>
          �Ƥu�t  &nbsp&nbsp&nbsp488425054~488425062<BR>
          �g�٨t  &nbsp&nbsp&nbsp488510067~488510085<BR>
          ��ިt  &nbsp&nbsp&nbsp488530057~488530065<BR>
          �k�ߨt�k���    &nbsp&nbsp&nbsp488620047~488620055<BR>
          �k�ߨt�k�ǲ�    &nbsp&nbsp&nbsp488610048~488610058<BR>
          </TD>
        </TR>
      </TABLE>

      </TD></TR></TABLE>
      
      <INPUT type=SUBMIT value="�i�J�T�{�e��">
);
