#!/usr/local/bin/perl

###########################################################################
#####   Perl_Sybase.cgi
#####   將相關資料批次轉入sybase
#####   Coder: Victor
#####   Date : Jun,05,1999
#####   Moify : Paladin
#####   Content: 加入註解..本程式僅供程式撰寫休閒時笑笑用....
###########################################################################
require "/ultra2/project/ccmisp06/LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"

  <HEAD><TITLE>轉入計中sybase資料庫工作</TITLE></HEAD>
  <BODY background="$GRAPH_URL./manager.jpg">
  <CENTER><H1>轉入Sybase資料庫中...<hr></H1>
  <FORM action="Perl_Sybasetest.cgi" method="POST">  
      嚴重毀損資料庫!!!警告,後果自行負責.......
      清除中....毀損.

TABLE_1
;           
