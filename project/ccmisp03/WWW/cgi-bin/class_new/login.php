<HTML>
<!script type="text/javascript" src="acpwd.js"></script>
<script language="JavaScript">
//  �o�@�q�O�q���y�t�Ϊ��n�J�����ۨӪ� Added 2005/09/13 Nidalap :D~

  function f_action(field) {
	popup_ask_passwd=window.open("http://mis.cc.ccu.edu.tw/academic/lost_passwd.htm", "�򥢱K�X", "width =600, height =600, scrollbars=yes");
	popup_ask_passwd.name = "lost_passwd";
	return true;
  }

  function f_action_gra(field) {
        popup_ask_passwd=window.open("http://mis.cc.ccu.edu.tw/academic/gra/lost_passwd.htm", "�򥢱K�X", "width =600, height =600, scrollbars=yes");
        popup_ask_passwd.name = "lost_passwd";
        return true;
  }


</SCRIPT>

<?PHP
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $system_settings = Get_System_State();
?>

 <HEAD>
   <meta http-equiv="Content-Type" content="text/html; charset=big5">
   <TITLE>LOGIN</TITLE>
 </HEAD>
  <BODY>

  <FONT size=2>
  <CENTER>
  <?PHP
    if( $system_settings['redirect_to_query'] == 1 ) {   // �p�G��Ƥw�g�M��
      echo("<CENTER>$YEAR �Ǧ~�ײ� $TERM �Ǵ��}�Ҥ�, ���d�ߥ��Ǵ���Ҹ��, �Цb�n�J���I�� <FONT color=RED>��Ƭd�� -> �W�Ǵ��\\�Ҫ�</FONT></CENTER>");
    }
  ?>
  <FORM name="form1" action="bookmark.php" method=POST>
  <TABLE border=0 width=100%>
    <TR>
      <TD><FONT size=2>�Ǹ�:</TD>
      <TD>
        <!input class="MyInput" onmouseover="this.className='MyInput2';" onmouseout="this.className='MyInput';"  type="text" name="temp_count" size="12" onkeyup="star();" onBlur="key_end();">
        <!input type="hidden" name="id">
        <INPUT name="id" size=12 maxlength=9>
      </TD>
    </TR>
    <TR>
      <TD><FONT size=2>�K�X:</TD>
      <TD>
        <INPUT size=10 type=password name=password>
      </TD>
    </TR>
    <TR>
      <TD colspan=2>
        <FONT size=2>
        <INPUT type=RADIO name=term checked ><? echo $YEAR ?> �Ǧ~��
        <?PHP 
          if( $TERM == 3 ) {
            echo("����<BR>");
          }else{
            echo("�� $TERM �Ǵ�<BR>");
          }
        ?>
        <!INPUT type=RADIO name=term><! 95 �Ǧ~�״���>
      </TD>
    </TR>
    <TR><TD colspan=2><HR></TD></TR>
    <TR>
      <TD><INPUT type=submit value="�n�J�t��"></TD>
      <?php 
        if( is_GRA() == 1 ) {
          echo("<TD><input type=\"button\" value=\"�򥢱K�X\" name=\"bt_lost_passwd\" onClick=\"return f_action_gra(this)\"></TD>");
        }else{
          echo("<TD><input type=\"button\" value=\"�򥢱K�X\" name=\"bt_lost_passwd\" onClick=\"return f_action(this)\"></TD>");
        }
      ?>
    </TR>
  </TABLE>
  </FORM>
 </BODY>
</HTML>