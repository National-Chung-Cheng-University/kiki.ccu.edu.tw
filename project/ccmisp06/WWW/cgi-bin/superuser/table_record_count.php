<?PHP
  require_once("../library/Reference.php");
  require_once($LIBRARY_PATH . "Database.php");

  $DBH = PDO_connect();

  ///  澂S墯V潬@潿I table 墬M蝔?  
  if( $DATABASE_TYPE == "postgresql" ) {
    $sql = "SELECT table_name FROM information_schema.tables 
                 WHERE table_type = 'BASE TABLE' AND table_schema = 'public'
                         ORDER BY table_type, table_name";
  }else{                                                //  sybase
    $sql = "select name from sysobjects where type='U' ORDER by name ";
  }

  $STH = $DBH->query($sql);
  print_r($DBH->errorInfo());

  while( $row = $STH->fetch(PDO::FETCH_NUM) )
    $tables[] = $row[0];

  foreach( $tables as $table ) {
    $sql = "SELECT count(*) FROM $table";
        $STH = $DBH->query($sql);
        list($temp) = $STH->fetch(PDO::FETCH_NUM);

        $rec_count[$table] = $temp;
  }

  echo "<TABLE border=1>";
  echo "<TR><TH>銵冽墬M蝔?/TH><TH>鞈G潽Y蝑F潫?/TR>\n";
  foreach( $rec_count as $table => $count ) {
    echo "  <TR><TD>$table</TD><TD>$count</TD></TR>\n";
  }

  echo "</TABLE>";

//  print_r($tables);



?>
