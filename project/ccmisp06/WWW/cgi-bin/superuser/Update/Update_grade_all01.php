<?php
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_grade_all.php
  /////  更新學生所有學期成績資料
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2009/12/18  Created by Nidalap :D~
  /////    2010/06/24  學年度改為由大至小排序 Nidalap :D~
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////

  include "../../php_lib/Reference.php";
//  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $year_from = 78;						///  開始有成績的年份
  
  $filename   = "now.txt";
  $outputfile = $DATA_PATH . "Grade/" . $filename;
//  $outputfile = "./ccc.txt";

  $time_start = time();
  
  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新歷年成績檔 - 1/2</H1><HR>");
  echo("<FORM action=Update_grade_all02.php method=POST>");
  echo("學年度: <SELECT name=year>");
  for( $year=$YEAR; $year>=$year_from; $year-- ) {
    if( strlen($year) == 2 ) {
      $year_ = "0" . $year;
    }else{
      $year_ = $year;
    }
    echo("<OPTION>$year_</OPTION>");
  }
  echo("</SELECT><BR>");
  echo("學期: <SELECT name=term><OPTION>1</OPTION><OPTION>2</OPTION></SELECT><P>");
  echo("<INPUT type=SUBMIT value='下一步'></FORM>");

?>

<INPUT type=button value="關閉視窗" onClick="window.close()">
