#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";

print("Content-type:text/html\n\n");
print("<CENTER><H1>�ǥͪ����iŪ, �N�±K�X�ର�s�Ǹ��K�X</H1></CENTER>");

print qq(
  <CENTER>
  <FORM method="POST" action="Change_ID_Password2.cgi">
    �п�J�¾Ǹ�:<INPUT name="old_id"><br>
    �п�J�s�Ǹ�:<INPUT name="new_id"><br>
    <INPUT type=submit value="����">
  </FORM>
  </CENTER>
);
