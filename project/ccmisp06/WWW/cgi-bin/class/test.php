<?PHP
  require_once("../library/Reference.php");

  //session_save_path("/NFS/session");  
  $path = session_save_path();
  $sess_id = session_id();
  session_start();
 
  echo "path = $path<BR>\n";
  echo "sess_id = $sess_id<BR>\n";
  echo "session = ";
  print_r($_SESSION);  

?>