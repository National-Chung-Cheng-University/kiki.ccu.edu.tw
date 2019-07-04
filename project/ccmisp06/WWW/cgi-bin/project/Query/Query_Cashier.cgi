#!/usr/local/bin/perl

require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
#require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."Error_Message.pm";
#require $LIBRARY_PATH."Checking_State_Map.pm";

print "Content-type: text/html"."\n\n";
%Input= User_Input();
Check_Cashier_Password($Input{dept_id},$Input{password});

print qq(
  <HTML>
    <FRAMESET rows="60,80%" border=1>
      <FRAME src="Query_Cashier2.cgi?dept=$Input{dept_id}&password=$Input{password}" name=INPUT>
      <FRAME src="" name=OUTPUT>
    </FRAMESET>
  </HTML>
);