#!/usr/local/bin/perl

require "../../../LIB/Reference.pm";

print("Content-type:text/html\n\n");
print("<CENTER><H1>學生直接進讀, 將舊密碼轉為新學號密碼</H1></CENTER>");

print qq(
  <CENTER>
  <FORM method="POST" action="Change_ID_Password2.cgi">
    請輸入舊學號:<INPUT name="old_id"><br>
    請輸入新學號:<INPUT name="new_id"><br>
    <INPUT type=submit value="轉檔">
  </FORM>
  </CENTER>
);
