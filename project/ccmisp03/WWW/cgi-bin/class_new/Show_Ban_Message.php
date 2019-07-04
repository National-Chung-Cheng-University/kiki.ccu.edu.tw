<?PHP 
  include "../library/Reference.php";
  include $LIBRARY_PATH . "Error_Message.php";
  include $LIBRARY_PATH . "Common_Utility.php";
  include $LIBRARY_PATH . "Session.php";
      
  $ban_res_time = $_GET['ban_res_time'];
  Show_Ban_Message($ban_res_time);


?>