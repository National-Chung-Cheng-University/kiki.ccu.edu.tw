<?PHP
//  echo "ccc";

  require "../../../LIB/Reference.php";
  require $LIBRARY_PATH . "Common_Utility.php";
  require $LIBRARY_PATH . "Database.php";

//  db_connect(0,1);
  $DBH = PDO_connect();
  $sql = "SELECT * FROM concent_form";
  $STH = $DBH->query($sql);
  
  if( $STH->fetch() ) {
    echo "Database is alive\n";
  }else{
    echo "Database unreachable!\n";
  }


?>