<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_student01.php
  /////  更新學生學籍資料檔 01 - 選擇是否加入預計復學生
  /////  Coder: Nidalap :D~
  /////  2006/09/22
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";
  
  echo $EXPIRE_META_TAG;
?>


<BODY background="../../../Graph/manager.jpg">
  <CENTER>
  <H1>更新學生學籍資料檔</H1><HR>
  <FORM action = "Update_student02.php">
    <SELECT name=include_rest>
      <OPTION value=0>不包含預計復學生
      <OPTION value=1>包含預計復學生
    </SELECT>
    <P>
    <INPUT type=submit value="更新資料">
  </FORM>


<?PHP

 
?>
