<?PHP
/////////////////////////////////////////////////////////////////////////////////////////////////
/////  Select_Course.php
/////  選課相關函式, 包含系統設定相關, 在可否選課方面的判定
/////  2007/02/14 改寫 php
/////  Nidalap :D~

/////////////////////////////////////////////////////////////////////////////////////////////////
/////  Check_Time_Map()
/////  檢查各年級各系所學生是否可以選課
/////     Step 1: 取得學生的年級
/////     Step 2: 讀取相關的時間設定檔
/////  Update: 2007/02/15 改寫 php 版本 (Nidalap :D~)

function Check_Time_Map($student)
{
//  print_r($student);
  global $REFERENCE_PATH, $IS_SUMMER;
  
  $grade	= Check_Student_Grade($student);
  $map_file	= $REFERENCE_PATH . "SelectTimeMap/" . $grade . ".map";
  
  ###  違章建築 讓註冊次數 0 的學生無法選課  2010/06/23  Nidalap :D~
  ###  此規則只套用在暑修/專班暑修系統上，不再是違章建築。  2010/09/08  Nidalap :D~
  if( ($IS_SUMMER) and ($student{"enrollnum"} == 0) ) {
    return(0);
  }
  if( $fp = fopen($map_file, "r") ) {
    while( list($dept, $temp_permission) = fscanf($fp, "%s\t%s\n") ) {
      if( $dept == $student{'dept'} )  {
        $permission = $temp_permission;
      } 
    }
   //  比起 perl 版本, 這裡省略了讀取 T?.map 檔案, 
   //  所以沒有了開放時段可言. 所有開放時間都是 24 小時.
   //  若需關閉系統, 建議透過 crobtab 執行之
    
    return($permission);
  }else{
    echo("內部錯誤: 無法讀取系統設定檔 SelectTimeMap! 請洽系統管理人員!<BR>\n");
    exit();
  }

}

////////////////////////////////////////////////////////////////////////////////////////////////
/////  Check_Student_Grade
/////  由Check_Time_Map()呼叫, 傳回某個學生的年級
/////  Updates:
/////    2010/09/08  移除 $limit_id 限制，因為現在所有轉學生資料均為當學年轉進來的  Nidalap :D~

function Check_Student_Grade($student)
{
  global $YEAR, $TERM;
//  $limit_id = $YEAR - 1;
//  $limit_id = "4" . $limit_id;      	///  限制轉學生學號前三碼為 4 . "YEAR-1"
                                    	///  以避免老轉學生, 也被視同新生允許選課. (2008/09/08)
                                        
  $change_school_student = Find_Change_School_Student();
  if( isset($change_school_student[$student["id"]]) and ($TERM == 1) ) {
    return(1);                		///  第一學期轉學生視同新生(2008/09/08)
  }

  if($student{'dept'}%10 <= 4){	//  大一至大四
    return($student{'grade'});
  }else{
    if($student{'grade'} == 1){	//  研一或博一
      return(5);
    }else{			//  研二以上含博士班學生
      return(6);
    }
  }
}
////////////////////////////////////////////////////////////////////////////////
/*function Head_of_Individual($name, $id, $dept, $grade, $class)
{
  global $SUPERUSER;
  
  $HEAD_DATA  = "  <table width=800 border=0>\n";
  $HEAD_DATA .= "  <tr>\n";
  $HEAD_DATA .= "    <th>姓名：$name</th>\n";
  $HEAD_DATA .= "    <th>學號：$id</th>\n";
  $HEAD_DATA .= "    <th>系所：$dept</th>\n";
  $HEAD_DATA .= "    <th>年級：$grade</th>\n";
  $HEAD_DATA .= "    <th>班別：$class</th>\n";
  if( $SUPERUSER == 1 )
     $HEAD_DATA .= "    <th><FONT color=RED>*</TH>\n";
  $HEAD_DATA .= "  </tr>\n";
  $HEAD_DATA .= "  </table>\n";

  return($HEAD_DATA);
}
*/
/*
/////////////////////////////////////////////////////////////////////////////////////////
/////  尚待加入的（目前只有 perl 版本有的）函式：
/////  2014/10/14
function Head_of_Individual($P_name,$P_id,$P_dept,$P_grade,$P_class)
{
}
function CREDIT_TABLE()
{
}
function Whats_Sys_State()
{
}
function Check_Student_Grade($User)
{
}
function Read_Time_Map()
{
}
function Check_Time_Map($user)
{
}
function Check_Course_Upper_Limit_Immune($course_id, $course_group, $stu_id)
{
}
function Upper_Limit_Immune_Add($course_id, $course_group, $stu_id)
{
}
function Check_Course_Upper_Limit_Immune_Count($course_id, $course_group, $selected_flag)
{
}
function Enter_Menu_Sys_State_Forbidden($HEAD_DATA)
{
}
*/


?>