#!/usr/local/bin/perl
print("Content-type:text/html\n\n");

require "../../library/Reference.pm";

print qq(
  <BODY background=$GRAPH_URL/bk.jpg>
    <CENTER><H1>��Ǵ��}�Ҭ�ئC��</H1><HR>
    �п�ܦC���ح���:
    
    <FORM action="List_Course2.cgi" method=POST>
      ���פH��: <INPUT type=checkbox name=number_limit><br>
      
      <INPUT type=submit value="��ܦC��">
    </FORM>


);