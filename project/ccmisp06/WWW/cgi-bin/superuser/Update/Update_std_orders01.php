<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_std_orders01.php
  /////  更新學生排名檔 01 - 顯示警訊, 避免不小心更新.
  /////  Updates:
  /////    2006/09/22  Created.
  /////    2009/03/03  增加顯示警訊功能, 避免不小心更新到.
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  echo $EXPIRE_META_TAG;
?>

<BODY background="../../../Graph/manager.jpg">
  <CENTER>
  <H1>更新學生排名檔</H1><HR>
  <FORM action = "Update_std_orders02.php">
    <FONT color=RED size=+2><B>
      請注意:<BR>
      此功能會更新包含當學期的排名資料,
      請確定當學期排名資料已經可以公佈, 才可繼續.
    </B></FONT>
    <P>
    <INPUT type=submit value="更新資料">
  </FORM>


<?PHP

 
?>
