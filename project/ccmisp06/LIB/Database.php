<?PHP

/////////////////////////////////////////////////////////////////////////////////////
/////  透過 PDO 連結資料庫
/////  依據 $DATABASE_TYPE 是 sybase 或 postgresql 決定如何連結
function PDO_connect($dbname="academic_kiki")
{
  global $USE_TEST_DATABASE, $DATABASE_TYPE, $DATABASE_IP, $KIKI_DB_NAME, $PUBLIC_DB_NAME, $PERSONNELDB_DB_NAME;
  $host = $DATABASE_IP;
  $user="acapassword";

  $db_users = array(
	"academic_kiki"	=> array("user" => "acapassword", "pass" => "passwordChanging@academic"),
	"academic"		=> array("user" => "ccumis", "pass" => "!misdbadmin@ccu"),
	"academic_gra"	=> array("user" => "ccumis", "pass" => "!misdbadmin@ccu"),
	"personneldb"	=> array("user" => "ccumis", "pass" => "!misdbadmin@ccu"),
	"ccucore"		=> array("user" => "ccumis", "pass" => "!misdbadmin@ccu"),
	"coursemap"		=> array("user" => "coursemap", "pass" => "roadmapOFccuCURSE")
  );
  $user		= $db_users[$dbname]['user'];
  $password	= $db_users[$dbname]['pass'];
  
  $debug = 0;
  if( $debug ) {
    echo "connecting to $DATABASE_TYPE $DATABASE_IP...<BR>\n";
    echo("[host, user, password, dbname] = [$host,$user,$password,$dbname]<BR>\n");
  } 
  try {
    if( $DATABASE_TYPE == "postgresql" ) {
      $DBH = new PDO("pgsql:dbname=$dbname;host=$host", $user, $password );
    }else{
      $DBH = new PDO("dblib:host=$host:4100;dbname=$dbname", $user, $password);
    }
  }
  catch( PDBException $e ) {
    echo $e->getMessage();
    exit("內部錯誤: 無法連結資料庫. 請洽系統維護人員!<BR>");
  }

//  print_r($DBH->errorInfo());
  
  return $DBH;
}



/////////////////////////////////////////////////////////////////////////////////////
/////  連結資料庫
function db_connect($keep_going="", $db_kiki="")
{
    global $link, $DATABASE_IP, $DATABASE_NAME, $KIKI_DB_NAME;
    $host = $DATABASE_IP;
    $user="acapassword";
    $password="HowDidTheyFindThis!!";

    if ($link=sybase_pconnect($host,$user,$password)) {		/// 資料庫連結成功
//      echo "DB connect succeed<BR>";
    }else{							/// 資料庫連結失敗
      if( $keep_going == 1 ) {					///   檢查傳入變數 $keep_going
        return("0");						///     傳回 0，繼續進行
      }else{
//      echo("($host, $user, $password)");
        Error_Call_For_Help();					///     停止處理，顯示錯誤訊息
      }
    }

    if( $db_kiki == 1 ) {					///  連線至 kiki 的資料庫
      $database = $KIKI_DB_NAME;
    }else{							///  連線至學籍資料庫
      $database = $DATABASE_NAME;
    }
    $select_db_result = sybase_select_db($database);

    $debug = 0;
    if($debug) {
      echo("$host,$user,$password<BR>\n"); 
      echo("link = $link<BR>\n");
      echo("database = $database<BR>\n");
      echo("select_db_result = $select_db_result<BR>\n");
    }
}
////////////////////////////////////////////////////////////////////////////////////
function db_connect_public()
{
    global $link, $DATABASE_IP, $PUBLIC_DB_NAME;
    $host = $DATABASE_IP;
    $user="ccureader";
    $password="More?read!";

    if ($link=sybase_pconnect($host,$user,$password)) {
//      echo "DB connect succeed<BR>";
    }else{
//      echo("($host, $user, $password)");
      Error_Call_For_Help();
    }

//    $database="public_run";
//    sybase_select_db($database);
    $database = $PUBLIC_DB_NAME;
    $select_db_result = sybase_select_db($database);

//    echo("$host,$user,$password<BR>\n"); 
//    echo("database = $database<BR>\n");
//    echo("select_db_result = $select_db_result<BR>\n");
}
////////////////////////////////////////////////////////////////////////////////////
function db_connect_personneldb()
{
    global $link, $DATABASE_IP, $PERSONNELDB_DB_NAME;
    $host = $DATABASE_IP;
    $user="ccumis";
    $password="xzsbcs2!";

    if ($link=sybase_pconnect($host,$user,$password)) {
//      echo "DB connect succeed<BR>";
    }else{
//      echo("($host, $user, $password)");
      Error_Call_For_Help();
    }

//    $database="public_run";
//    sybase_select_db($database);
    $database = $PERSONNELDB_DB_NAME;
    $select_db_result = sybase_select_db($database);

//    echo("$host,$user,$password<BR>\n"); 
//    echo("database = $database<BR>\n");
//    echo("select_db_result = $select_db_result<BR>\n");
}
////////////////////////////////////////////////////////////////////////////////////
function query($sql)
{
  $debug = 0;
  
  $result = sybase_query($sql);
  
  if( $debug ) {
    if( !$result )  echo sybase_get_last_message();
  }
  return $result;
}
////////////////////////////////////////////////////////////////////////////////////
function fetch_assoc($result)
{
  $row = sybase_fetch_assoc($result);
  return $row;
}

////////////////////////////////////////////////////////////////////////////////////
function Get_Email($id)
{
  global $DBH, $TABLE, $DATABASE_NAME;
  
  if( !isset($DBH) )   $DBH = PDO_connect($DATABASE_NAME);

  $table = $TABLE['EMAIL'];
  $sql = "SELECT * from " . $table . " WHERE std_no = '" . $id . "'";
//  $result_id = sybase_query($sql, $link);
//  $rowcount = sybase_num_rows($result_id);
//  $datarow = sybase_fetch_row($result_id);

  $STH = $DBH->prepare($sql);
  $STH->execute();
  
//  echo "sql = $sql<BR>\n";
//  print_r($DBH->errorInfo());
  
//  $STH = $DBH->query($sql);
  $datarow = $STH->fetch();
  list($junk, $email) = $datarow;

//  echo("link = $link<BR>\n");


/*  echo("q_string = $sql<BR>\n");
  echo("datarow = $datarow<BR>\n");
  echo("email = $email<BR>\n");
*/
  return($email);
}
////////////////////////////////////////////////////////////////////////////////////
function Update_Email($id, $email)
{
  $flag = 0;
  global $DBH, $TABLE;

  $table = $TABLE['EMAIL'];
  $query_string = "UPDATE " . $table . " SET e_mail_addr = '" . $email . "' WHERE std_no = '" . $id . "'";
//  echo("$query_string<BR>\n");
  $STH = $DBH->query($query_string);
//  $flag = sybase_query($query_string, $link);

  return is_object($STH);
}
////////////////////////////////////////////////////////////////////////////////////
function Update_Password($id, $password)
{
  global $DBH, $TABLE;

  $table = $TABLE['PASSWORD'];
  $query_string = "UPDATE " . $table . " SET pwd = '" . $password . "' WHERE std_no = '" . $id . "'";

//  if( $result_id = sybase_query($query_string, $link) )  {		///  成功 Update
//  echo "sql = $query_string";

  $STH = $DBH->query($query_string);
  if( is_object($STH) )		$succeed = 1;
  else						$succeed = 0;
  if( is_object($STH) )  {		///  成功 Update
//    echo "$query_string : succeed... ";
//	print_r($DBH->errorInfo());
//    echo "query = $query_string<BR>\n";
//    echo sybase_get_last_message();
	list($junk, $day_time) = gettime("");
	//  $ip = getenv('REMOTE_ADDR');
	$ip = getenv("HTTP_X_FORWARDED_FOR");
	if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }

	$detail = $ip . " 更新密碼(kiki)";
	  
	$table = $TABLE['NETLOG'];
	$query_string = "INSERT INTO " . $table . " ( user_id, day_time, detail ) VALUES ( '";
	$query_string .= $id . "', '" . $day_time . "', '" . $detail . "' )";
	$STH = $DBH->query($query_string);
//	$result_id2 = sybase_query($query_string, $link);
  }else{
    print_r($DBH->errorInfo());
    die("Error updating password!");
  }
  return( $succeed );
}
////////////////////////////////////////////////////////////////////////////////////
function Read_Personal_Data_From_Database($id)
{
  global $DBH, $TABLE;
  $debug = 0;

  $table1 = $TABLE['STD_REC'];		//  a11tstd_rec
  $table2 = $TABLE['DEPT'];		//  h0rtunit_a_
//  $query_string = "SELECT name, deptcd, now_grade, now_class from " . $table . " WHERE std_no = '" . $id . "'";
  $query_string = "
  SELECT dbo.a11tstd_rec.personid,
         dbo.a11tstd_rec.name,   
         dbo.a11tstd_rec.now_dept,   
         dbo.h0rtunit_a_.name,   
         dbo.a11tstd_rec.now_grade,   
         dbo.a11tstd_rec.now_class,
         dbo.a11tstd_rec.pwd  
    FROM $table1,   
         $table2  
   WHERE ( dbo.a11tstd_rec.now_dept = dbo.h0rtunit_a_.cd ) and  
         ( ( dbo.a11tstd_rec.std_no = \"$id\" )   
         )";
  $query_string = "
    SELECT personid, stu.name, now_dept, dept.name, now_grade, now_class, pwd
	  FROM a11tstd_rec AS stu, h0rtunit_a_ AS dept
	 WHERE now_dept = cd
 	   AND std_no = '$id'
  ";
  if( $debug )  {
    echo("query_string = $query_string<BR>\n");
  }
//  $result_id = sybase_query($query_string, $link);
//  $row = sybase_fetch_row($result_id);
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  $row = $STH->fetch();

  list($personid, $name, $dept, $dept_name, $grade, $class, $pwd) = $row;
//  $len = strlen($pwd);
//  echo("len = $len, [$pwd]<BR>\n");
  if( ($pwd == "") or ($pwd == " ")  )  {	// 如果密碼欄是空白(應該是新生)
    $pwd = $personid;				//  以身份證號取代之
  }
  $pwd = chop($pwd);
  
  $row = array($personid, $name, $dept, $dept_name, $grade, $class, $pwd);
  if( $debug )  {
    echo("[$personid, $name, $dept, $dept_name, $grade, $class, $pwd]<BR>\n");
  }

  
  return $row;
//  list($name, $dept, $grade, $class) = sybase_fetch_row($result_id);
//  return($name, $dept, $grade, $class);
}
////////////////////////////////////////////////////////////////////////////////////
function Read_Personal_Data_From_Database_Batch()
{
  global $DBH, $TABLE;

  $table = "dbo." . $TABLE['STD_REC'];
//  $table2 = "dbo." . $TABLE['DEPT'];
//  $query_string = "SELECT name, deptcd, now_grade, now_class from " . $table . " WHERE std_no = '" . $id 
  $query_string = "
  SELECT dbo.a11tstd_rec.std_no,
         dbo.a11tstd_rec.name,   
         dbo.a11tstd_rec.now_dept,   
         dbo.a11tstd_rec.now_grade,   
         dbo.a11tstd_rec.now_class,
         dbo.a11tstd_rec.pwd  
    FROM $table
  ";

//  $query_string = "UPDATE " . $table . " SET pwd = '" . $password . "' WHERE std_no = '" . $id . "'";
//  echo("q_string = $query_string<BR>\n");
//  $result_id = sybase_query($query_string, $link);
  $STH = $DBH->prepare($query_string);
  $STH->execute();

//  while( $temp = sybase_fetch_row($result_id) ) {
  while( $temp = $STH->fetch() ) {
    list($std_no, $name, $dept, $grade, $class, $pwd) = $temp;
//    echo("[$personid, $name, $dept, $grade, $class, $pwd]\n");
    $data[$std_no] = $pwd;
//    $data[$personid] = array($personid, $name, $pwd);
  }
  
//  list($personid, $name, $dept, $dept_name, $grade, $class, $pwd) = $row;
//  $len = strlen($pwd);
//  echo("len = $len, [$pwd]<BR>\n");
/*  if( ($pwd == "") or ($pwd == " ")  )  {       // 如果密碼欄是空白(應該是新生)
    $pwd = $personid;                           //  以身份證號取代之
  }
*/
//  $row = array($name, $dept, $dept_name, $grade, $class, $pwd);
//  echo("$personid, $name, $dept, $dept_name, $grade, $class, $pwd<BR>\n");


  return $data;
//  list($name, $dept, $grade, $class) = sybase_fetch_row($result_id);
//  return($name, $dept, $grade, $class);
}

//////////////////////////////////////////////////////////////////////////////////////
/////  將 Sybase 讀取到的資料存入檔案
/////  用於存入諸如 student.txt, deduct.txt, teacher.txt 等相關資料檔
/////  需事先執行 sybase_query 得到 result_id 方可呼叫此函式.
/////  Nidalap :D~
/////  2006/09/21
function Save_Update_File($outputfile, $result_id, $rowcount)           
{
    $save_succeed = 0;
    $columncount  = sybase_num_fields($result_id);
    
    print("[outputfile, result_id, rowcount] = [$outputfile, $result_id, $rowcount]<BR>\n");

    if( $rowcount != 0 ) {                        //  如果沒有抓到任何資料, 不寫入檔案
        $fp = fopen ($outputfile,"w+");
        if ($fp)
        {
                set_file_buffer($fp, 65536);
                for ($i=0;$i<$rowcount;$i++)
                {
                        $output="";
                        $datarow=sybase_fetch_row($result_id);
                        for ($j=0;$j<$columncount;$j++)
                        {
                          if( ($j==0) and ($output.$datarow[$j]=="7006") )
                            $output.$datarow[$j] = "I001";	// 通識中心7006->I001, [20080505]
                          if( $j == ($columncount-1) ) {
                            $output=$output.$datarow[$j];       // 最後一欄不加 TAB
                          }else{
                            $output=$output.$datarow[$j]."\t";
                          }
                        }
                        $output=$output."\n";
                        fputs($fp, $output);
                }
                fclose($fp);
                $time_end=time();
                $save_succeed = 1;
        }else{                                  //  如果開檔失敗
          $save_succeed = 0;
        }
    }
    if( !$save_succeed )  echo sybase_get_last_message();
    return($save_succeed);
}

//////////////////////////////////////////////////////////////////////////////////////
/////  將 PDO 讀取到的資料存入檔案
/////  用於存入諸如 student.txt, deduct.txt, teacher.txt 等相關資料檔
/////  需事先執行 PDO_connect 得到 $DBH 與 $STH 方可呼叫此函式.
/////  Updates:
/////    2012/10/30  從 Save_Update_File() 複製修改而來 by Nidalap :D~
function Save_Update_File_PDO($outputfile)
{
	global $DBH, $STH;
    $save_succeed = 0;
	
//	$data = $STH->fetchAll(PDO::FETCH_NUM);
//    $rowcount = count($data);
//	$columncount = count($data[0]);
	
//    print("[outputfile, rowcount, columncount] = [$outputfile, $rowcount, $columncount]<BR>\n");
    $datarow = $STH->fetch(PDO::FETCH_NUM);	//  先抓一行資料
    $rowcount = 0;
	if( $datarow ) {                        //  如果沒有抓到任何資料, 不寫入檔案
        $fp = fopen($outputfile,"w+");
        if ($fp)
        {
                set_file_buffer($fp, 65536);
				$i = 0;								///  行數
				do {
                        $output="";
                        $columncount = count($datarow);
                        for ($j=0;$j<$columncount;$j++)
                        {
                          if( ($j==0) and ($output.$datarow[$j]=="7006") )
                            $output.$datarow[$j] = "I001";	// 通識中心7006->I001, [20080505]
                          if( $j == ($columncount-1) ) {
                            $output=$output.$datarow[$j];       // 最後一欄不加 TAB
                          }else{
                            $output=$output.$datarow[$j]."\t";
                          }
                        }
                        $output=$output."\n";
                        fputs($fp, $output);
						$i++;
                } while( $datarow = $STH->fetch(PDO::FETCH_NUM) ) ;	//  繼續抓後續資料
                fclose($fp);
				chmod($outputfile, 0666);
                $time_end=time();
				$rowcount = $i;
                $save_succeed = 1;
        }else{                                  //  如果開檔失敗
          $save_succeed = 0;
        }
    }
    //if( !$save_succeed )  echo sybase_get_last_message();
	if( !$save_succeed )  {
	  if( $rowcount == 0 ) {
		echo "資料庫中沒有任何資料！<P>";
	  }
	  print_r($STH->errorInfo());
	}
    return array($save_succeed, $rowcount);

}

////////////////////////////////////////////////////////////////////////////////////
function Error_Call_For_Help()
{
  global $BG_PIC, $HEAD_DATA;
  
  echo("<HTML><HEAD><TITLE>內部錯誤(無法連結資料庫)</TITLE></HEAD>\n");
  echo("<BODY background = $BG_PIC>\n");
  echo("$HEAD_DATA\n");
  echo("<HR><CENTER><P>\n");
  echo("<TABLE border=0 width=50%><TR><TD>");
  echo("<FONT color=RED>內部錯誤: 無法連結資料庫. 請洽系統維護人員!</FONT><P>");
  Print_Contact("fatal");
  echo("</TD></TR></TABLE>");
  exit();
}

?>