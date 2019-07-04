<?PHP

//////////////////////////////////////////////////////////////////////////////
/////  System_Settings.pm
/////  系統相關設定
/////  一些系統相關設定資料的讀取, 另有部分存於 Reference.pm 中
/////  Coder: Nidalap :D~
/////  Date: 
/////    2007/02/10 改寫為 php
/////    2015/09/22 加入 Write_System_Settings()
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
/////  儲存系統設定相關資料
/////  2015/09/23  針對客製化學程的三個日期，特別另存資料到課程地圖中
function Write_System_Settings($flags)
{
  global $REFERENCE_PATH;
  
  $setting_file = $REFERENCE_PATH . "System_Settings.txt";
  if( !($fp = fopen("$setting_file", "w")) )
     print("Cannot open system setting file! abort!!<BR>\n");

  foreach( $flags as $key => $val ) {
    if($key == "modify_flag")  break;
	fputs($fp, "$key\t$val\n");
  }
  fclose($fp);
 
  /////  將客製化學程的三個日期，另外寫到課程地圖系統的系統設定資料表 a36tsys_settings 中
  $DBH_cm = PDO_connect("coursemap");
  $sql = "
	UPDATE a36tsys_settings 
		  SET my_program_start = '" . $flags["my_program_start"] . "', 
				 my_program_accept = '" . $flags["my_program_accept"] .  "',
				 my_program_end = '" . $flags["my_program_end"] . "'
  ";
  $DBH_cm->query($sql);
}



//////////////////////////////////////////////////////////////////////////////
/////  Read_System_Settings
/////  讀取系統設定檔
/////  此函式沒有必要存在, 請使用 Reference.php -> Get_System_State()
/*function Read_System_Settings()
{
  global $REFERENCE_PATH;
  $setting_file = $REFERENCE_PATH . "System_Settings.txt";
  if( $SYS_SETTINGS = fopen($setting_file, "r") ) {

    while( list($key, $value) = fscanf($SYS_SETTINGS, "%s\t%s\n") ) {
      $flags{$key} = $value;
    }
    return($flags);
  }else{						//  開檔錯誤! Internal Error!
    print("系統設定檔讀取錯誤! 請洽系統管理者!!<BR>\n");
  }
}
*/





?>
