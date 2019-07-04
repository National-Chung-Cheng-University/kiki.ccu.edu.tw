<?PHP
/////////////////////////////////////////////////////////////////////////////////
///// Dept.php
///// 系所相關函式
///// Updates:
/////   2012/??/?? 從 perl 版本改來 by Nidalap :D~
/////   2016/06/01 改為到 ccmisp06/07 的 $MAIN_HOME_PATH1/2 讀取資料檔 by Nidalap :D~

///////////////////////////////////////////////////////////////////////////////////
/////  Find_All_Dept
/////  此版本不支援 NO_COM_DEPT 參數。
function Find_All_Dept()
{
//  my($old_dept_only) = @_;

  global $REFERENCE_PATH, $IS_GRA, $MAIN_HOME_PATH2, $MAIN_HOME_PATH1;

//  my($DeptFile) = $REFERENCE_PATH . "Dept";
//  my(@dept,$dept,@TempArray,$temp,$i);
//  my($dept_com_file, @TempArray2, %dept_com, $deptcd, $com_deptcd);
  //$DeptFile = $REFERENCE_PATH . "Dept";
  $DeptFile = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/Dept";

  if( !($DEPT = fopen($DeptFile,"r")) )   return "";
  while( $temp = fgets($DEPT) )  $TempArray[] = $temp;
  fclose($DEPT);

  foreach( $TempArray as $line )  {
    list($temp_dept,$temp) = preg_split("/\s+/",$line);
    $dept[]=$temp_dept;
  }
  return($dept);
}

/////////////////////////////////////////////////////////////////////////////////
function Read_Dept($input_dept)
{
  global $REFERENCE_PATH, $IS_GRA, $MAIN_HOME_PATH2, $MAIN_HOME_PATH1;
  //$dept_file = $REFERENCE_PATH . "Dept";
  $dept_file = ( $IS_GRA ? $MAIN_HOME_PATH2 : $MAIN_HOME_PATH1 ) . "DATA/Reference/Dept";
  
  if( !($fp = fopen($dept_file, "r")) ) {
    echo("系統內部錯誤: 找不到系所資料檔! 請洽程式設計人員！<BR>\n");
    exit();
  }else{
    while( $line = fgets($fp) ) {
      list($id, $cname1, $cname2, $college, $ename) = preg_split('/\t/', $line);
      if( $id == $input_dept ) {
        $dept{'id'}	= $id;
        $dept{'cname'}	= $cname1;
        $dept{'cname2'}	= $cname2;
        $dept{'college'}= $college;
		$dept{'ename'}= $ename;
//        echo("$id, $name1, $name2, $college<BR>\n");
        return($dept);
      }
    }
  }
/*  open(DEPT,$DeptFile) or die("Cannot open file $DeptFile!\n");
   @TempArray = <DEPT>;
  close(DEPT);
  foreach $dept_cd(@TempArray)  {
    ($dept_cd,$temp,$temp2,$college, $junk) = split(/\s+/,$dept_cd);
    if( $dept_cd eq $Input_Dept )
    {
     $dept{id}=$dept_cd;
     $dept{cname}=$temp;
     $dept{cname2}=$temp2;
     $dept{college}=$college;
     $dept{password}="";
     open(PWD,$DEPT_PASSWORD_PATH."/".$dept_cd.".pwd") or goto EXIT;
      $dept{password}=<PWD>;
      $dept{password} =~ s//\n/;
     close(PWD);
     goto EXIT;
    }
  }
  EXIT:
  return(%dept);
*/
}
////////////////////////////////////////////////////////////////////////////////
/////  回傳某系所對應的學院
/////  因應文學院需求-委由各系實際執行開課需求
/////  轉換身份，若一般學系則轉換至「該學院學士班」(X014)
/////  若輸入學系代碼為語言中心，則轉換為通識中心，反之亦然（語言中心開設通識外語需求）
/////  傳入值: 系所代碼
/////  傳回值: 所屬學院代碼
function Find_Dept_College($dept)
{
  global $DEPT_LAN, $DEPT_CGE;
  print "[dept, LAN, CGE] = [$dept, $DEPT_LAN, $DEPT_CGE]<BR>\n";
  
  if( $dept == $DEPT_LAN ) {						///  如果是語言中心
    $college = $DEPT_CGE;
  }else if( $dept == $DEPT_CGE ) {					///  如果是通識中心
    $college = $DEPT_LAN;
  }else{											///  否則傳回該學系所屬學院(目前只有文學院會用)
    //$college = substr($dept, 0, 1) . "01" . substr($dept, 3, 1);
	$college = substr($dept, 0, 1) . "014";			///  「語言所」切換身份仍是開設「文學院學士班」（非碩士班）課程		20150817
  }
  
  return $college;
}




?>