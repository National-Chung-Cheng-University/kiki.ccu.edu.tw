<?PHP

/////////////////////////////////////////////////////////////////////////////////
/////  Teacher.php
/////  處理教師資料
/////  Updates:
/////    2011/08/09 從 perl 版本移植 by Nidalap :D~

function Read_All_Teacher()
{
  global $REFERENCE_PATH;
// my(@Teacher,$temp,$temp1,$i,@Data,$data);
  $teacher_file = $REFERENCE_PATH . "/teacher.txt";
  if( !($handle = fopen($teacher_file, "r")) )
    return;
  while( $temp = fgets($handle) )  $lines[] = $temp;
  fclose($handle);
  
  foreach( $lines as $line ) {
    rtrim($line);
    list($dept, $id, $name) = preg_split("/\s+/", $line);
    $all_teachers[$id]["dept"]	= $dept;
    $all_teachers[$id]["id"]	= $id;
    $all_teachers[$id]["name"]	= $name;
  }
  $all_teachers["99999"]["id"]	 = "99999";
  $all_teachers["99999"]["name"] = "教師未定";

  return $all_teachers;
}


/////////////////////////////////////////////////////////////////////////////////
/////  由傳入陣列 $teachers 教師代碼，傳回教師姓名的字串
/////  使用 global: $all_teachers
/////  Updates:
/////    2011/08/09 從 perl 版本移植 by Nidalap :D~ 
function Format_Teacher_String($teachers)
{
  global $all_teachers;

  $string = "";
#  print("T = $T<BR>\n");
  foreach( $teachers as $teacher ) {
    $string .= $all_teachers[$teacher]["name"] . ", ";
  }
#  print("$string<BR>\n");
  $string = preg_replace("/..$/", "", $string);
  
  return($string);
}

?>