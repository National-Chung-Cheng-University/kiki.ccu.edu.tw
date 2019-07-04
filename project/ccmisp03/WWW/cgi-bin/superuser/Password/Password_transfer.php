<?php
	set_time_limit(300);
	include("sybase_connect.php");
        $PASSWORD_PATH = "/ultra2/project/ccmisp06/DATA/Password/student/";

#	$table="a11tpassword";
#	$query="select * from ".$table." order by std_no";

        chdir($PASSWORD_PATH);
        $PASS_DIR = opendir(".");
        while($file = readdir($PASS_DIR) ) {
          if( ereg("..........pwd", $file) ) {     ## 如果是正確的密碼檔
            $FILE = fopen("$file", "r");
            $passwd = fread($FILE, 13);
            fclose($FILE);
            $std_no = ereg_replace("\.pwd", "", $file);
            
            $query = "INSERT INTO a11tpassword VALUES ('$std_no', '$passwd')";
            $result_id = sybase_query($query,$link);
            echo("$query<BR>\n");
          } 
        }

#	else { echo "failed to open $outputfile";}
#	sybase_close($link);
	echo "done<br>";
?>
