#!/usr/local/bin/perl
###########################################################################
#####  Login.cgi
#####  �d�߿�ҾǥͦW��
#####  �C�X�t�Ҩѿ��.
#####  �t�������d�ߥ\���, �|�����\�d��
#####  Modified: 2001/09/11
#####  Coder: Nidalap :D~
###########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Select_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

$sys_state = Whats_Sys_State();
if( $sys_state == 0 ) {
  print qq(
    <html>
      <head><title>�ĤG���}�ƽҨt��</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>�d�߭׽ҾǥͦW��\\��</h4><HR>
         �ثe�t�μȤ��}��d��!
  );
}else{
  ($year, $term) = Last_Semester(1);
  %system_settings = Read_System_Settings();
#  foreach $key (keys %system_settings) {   
#    print("$key => $system_settings{$key}<BR>\n");
#  }
  if( $system_settings{redirect_to_query} == 1 ) {			###  �p�G�t�Υثe���b�}�s�Ǵ�����
    $selected1 = "";							###    ���N�w�]��ܤW�Ǵ����
    $selected2 = "selected=\"selected\"";
  }else{
    $selected1 = "selected=\"selected\"";
    $selected2 = "";
  }

  print qq(
    <html>
      <head><title>�ĤG���}�ƽҨt��</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>�d�߭׽ҾǥͦW��\\��</h4><p>
         <h4>�п�ܨt��</h4><p><br>
         <form method=post action=Query_1.cgi>
           <table border=0>
             <tr>
               <th><h3>�t�O:</h3></th>
               <td><select name=dept_cd>
  );
  my(@Dept,$dept,%Dept);
  @Dept=Find_All_Dept();
  foreach $dept(@Dept) {
    %Dept=Read_Dept($dept);
    print "<option value=$Dept{id}>$Dept{cname}\n";
  }
  print qq(
                  </select>
               </td>
             </tr>
           </table>
           <INPUT type=CHECKBOX name=query_count value=1>�d�ߦU��ؿ�ҤH��<P>
           <SELECT name=semester>
             <OPTION value="this" $selected1>$YEAR �Ǧ~�ײ� $TERM �Ǵ����</OPTION>
             <OPTION value="last" $selected2>$year �Ǧ~�ײ� $term �Ǵ����</OPTION>
           </SELECT>
           <P>
           <input type="submit" value="��ƶ�g����"> 
           <input type="reset" value="���s��g���">
         </form>
       </center>
     </body>
   </html>
  );
}
