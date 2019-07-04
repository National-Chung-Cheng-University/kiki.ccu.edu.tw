<?PHP

/////////////////////////////////////////////////////////////////////////////////////
/////  連結資料庫
function db_connect($keep_going = NULL, $db_kiki = NULL)
{
    global $link, $DATABASE_IP, $DATABASE_NAME, $KIKI_DB_NAME;
    $host = $DATABASE_IP;
    $user="acapassword";
    $password="HowDidTheyFindThis!!";

//    sybase_min_message_severity(1000);
//    echo "start connect<BR>";
//    echo("$host,$user,$password");

    if ($link=sybase_pconnect($host,$user,$password)) {		/// 資料庫連結成功
//      echo "DB connect succeed<BR>";
    }else{							/// 資料庫連結失敗
      if( $keep_going == 1 ) {					///   檢查傳入變數 $keep_going
//        echo sybase_get_last_message();
        return("0");						///     傳回 0，繼續進行
      }else{
//      echo("($host, $user, $password)");
        Error_Call_For_Help();					///     停止處理，顯示錯誤訊息
      }
    }

//    $database="public_run";
//    sybase_select_db($database);
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



function Get_Email($id)
{
  global $link, $TABLE;

  $table = $TABLE['EMAIL'];
  $query_string = "SELECT * from " . $table . " WHERE std_no = '" . $id . "'";
  $result_id = sybase_query($query_string, $link);
  $rowcount = sybase_num_rows($result_id);
  $datarow = sybase_fetch_row($result_id);
  list($junk, $email) = $datarow;

/*
  echo("link = $link<BR>\n");
  echo("q_string = $query_string<BR>\n");
  echo("result_id = $result_id<BR>\n");
  echo("rowcount = $rowcount<BR>\n");
  echo("datarow = $datarow<BR>\n");
  echo("email = $email<BR>\n");
*/
  return($email);


}
////////////////////////////////////////////////////////////////////////////////////
function Update_Email($id, $email)
{
  $flag = 0;
  global $link, $TABLE;

  $table = $TABLE['EMAIL'];
  $query_string = "UPDATE " . $table . " SET e_mail_addr = '" . $email . "' WHERE std_no = '" . $id . "'";
//  echo("$query_string<BR>\n");
  $flag = sybase_query($query_string, $link);

  return $flag;
}
////////////////////////////////////////////////////////////////////////////////////
function Update_Password($id, $password)
{
  global $link, $TABLE;

  $table = $TABLE['PASSWORD'];
  $query_string = "UPDATE " . $table . " SET pwd = '" . $password . "' WHERE std_no = '" . $id . "'";
  if( $result_id = sybase_query($query_string, $link) )  {		///  成功 Update
//	echo sybase_get_last_message();
	  list($junk, $day_time) = gettime("");
	//  $ip = getenv('REMOTE_ADDR');
	  $ip = getenv("HTTP_X_FORWARDED_FOR");
	  if( $ip == "" ) { $ip = getenv("REMOTE_ADDR"); }

	  $detail = $ip . " 更新密碼(kiki)";
	  
	  $table = $TABLE['NETLOG'];
	  $query_string = "INSERT INTO " . $table . " ( user_id, day_time, detail ) VALUES ( '";
	  $query_string .= $id . "', '" . $day_time . "', '" . $detail . "' )";

	  $result_id2 = sybase_query($query_string, $link);
  }
  return($result_id);
}
////////////////////////////////////////////////////////////////////////////////////
function Read_Personal_Data_From_Sybase($id)
{
  global $link, $TABLE;
  $debug = 0;

  $table1 = "dbo." . $TABLE['STD_REC'];
  $table2 = "dbo." . $TABLE['DEPT'];
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

//  $query_string = "UPDATE " . $table . " SET pwd = '" . $password . "' WHERE std_no = '" . $id . "'";
  if( $debug )  {
    echo("query_string = $query_string<BR>\n");
  }
  $result_id = sybase_query($query_string, $link);
  $row = sybase_fetch_row($result_id);
  list($personid, $name, $dept, $dept_name, $grade, $class, $pwd) = $row;
//  $len = strlen($pwd);
//  echo("len = $len, [$pwd]<BR>\n");
  if( ($pwd == "") or ($pwd == " ")  )  {	// 如果密碼欄是空白(應該是新生)
    $pwd = $personid;				//  以身份證號取代之
  }
  
  $row = array($personid, $name, $dept, $dept_name, $grade, $class, $pwd);
//  echo("$personid, $name, $dept, $dept_name, $grade, $class, $pwd<BR>\n");

  
  return $row;
//  list($name, $dept, $grade, $class) = sybase_fetch_row($result_id);
//  return($name, $dept, $grade, $class);
}
////////////////////////////////////////////////////////////////////////////////////
function Read_Personal_Data_From_Sybase_Batch()
{
  global $link, $TABLE;

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
  $result_id = sybase_query($query_string, $link);

  while( $temp = sybase_fetch_row($result_id) ) {
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