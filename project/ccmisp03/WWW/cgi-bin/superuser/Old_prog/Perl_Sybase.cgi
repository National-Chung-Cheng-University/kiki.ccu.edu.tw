#!/usr/local/bin/perl

###########################################################################
#####   Perl_Sybase.cgi
#####   �N������Ƨ妸��Jsybase
#####   Coder: Victor
#####   Date : Jun,05,1999
#####   Moify : Paladin
#####   Content: �[�J����..���{���Ȩѵ{�����g�𶢮ɯ�����....
###########################################################################
require "/ultra2/project/ccmisp06/LIB/Reference.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student.pm";

print("Content-type:text/html\n\n");

@dept = Find_All_Dept();
print << "TABLE_1"

  <HEAD><TITLE>��J�p��sybase��Ʈw�u�@</TITLE></HEAD>
  <BODY background="$GRAPH_URL./manager.jpg">
  <CENTER><H1>��JSybase��Ʈw��...<hr></H1>
  <FORM action="Perl_Sybasetest.cgi" method="POST">  
      �Y�����l��Ʈw!!!ĵ�i,��G�ۦ�t�d.......
      �M����....���l.

TABLE_1
;           
