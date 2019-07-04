<?PHP
  //////////////////////////////////////////////////////////////////////////////////////////
  /////  Update_Course.php
  /////  依照系統設定，判別是否顯示科目異動資訊
  /////  Updates:
  /////    2009/12/18 Created by Nidalap :D~
 
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "System_Settings.php";

  $system_settings = Get_System_State();
  
  if( $system_settings{"current_system_timeline"} <= 1 ) {
    header("Location:../../Update_Course_nothing.html");
  }else{
    header("Location:../../Update_Course.html");
  }

?>