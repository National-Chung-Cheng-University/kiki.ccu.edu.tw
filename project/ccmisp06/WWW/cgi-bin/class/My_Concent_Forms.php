<?PHP

//////////////////////////////////////////////////////////////////////////////////////////
/////  My_Concent_Forms.php
/////  學生「我的加簽單」畫面
/////  列出該學生所有加簽單申請狀態一覽表
/////  Updates:
/////    2010/08/17 Created by Nidalap :D~
/////    2012/02/16 若系統設定目前不可申請加簽，則不顯示「新增加簽課程」連結。 Nidalap :D~
/////    2012/11/06 改採 PDO 連線資料庫 by Nidalap :D~
/////    2015/05/06 行動版相關修改 by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Error_Message.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "System_Settings.php";
require_once $LIBRARY_PATH . "Session.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Student.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "English.php";

session_start();
  
//print_r($_GET);
$session_id	= quotes($_GET["session_id"]);
$session	= Read_Session($session_id);
Renew_Session($session_id);

$id = $session["id"];
$student = Read_Student($session["id"]);
$dept = Read_Dept($student["dept"]);
if( Check_SU_Password($session["password"], "", $student["id"]) ) {
  $_SESSION["SUPERUSER"] = 1;           ///  檢查 SU password
}else{
  unset($_SESSION["SUPERUSER"]);
}
//print_r($session);

if( $IS_ENGLISH ) {
  $HEAD_DATA = Form_Head_Data($id, $student{"ename"}, $dept{"ename"}, $student{"grade"}, $student{"class_"});
}else{
  $HEAD_DATA = Form_Head_Data($id, $student{"name"}, $dept{"cname"}, $student{"grade"}, $student{"class_"});
}

$HTML_BANNER = Print_HTML_Banner();

$DBH = PDO_connect();		///  連到 academic_kiki 資料庫
$txt = Init_Text_Values();								///  初始化顯示文字（中文或英文）

$apply_data = Concent_Form_Apply_Status($student["id"], "", "", "", "");

Print_My_Concent_Forms($apply_data);

//////////////////////////////////////////////////////////////////////////////////////////////////
function Print_My_Concent_Forms($apply_data)
{
  global $GRAPH_URL, $student, $session_id, $txt, $IS_ENGLISH;
  if( count($apply_data) == 0 ) {
    echo $txt{'not_found'};
  }else{
    $course = Course_of_Student($student["id"]);
    foreach( $course as $cou ) {
      $temp = $cou["id"] . "_" . $cou["group"];
      $selected[$temp] = 1;							///  將學生目前已選修課程標記起來
    }
    echo "<TABLE border=1 width=95%>";
    echo "<TR bgcolor=YELLOW>
            <TH>" . $txt{'apply_time'} . "</TH>
            <TH>" . $txt{'review'} . "</TH>
            <TH>" . $txt{'selected'} . "</TH>
            <TH>" . $txt{'cid'} . "</TH>
            <TH>" . $txt{'group'} . "</TH>
            <TH>" . $txt{'cname'} . "</TH>
          </TR>";
  
    $not_selected = 0;
    foreach( $apply_data as $form ) {
      $form["apply_time"] = preg_replace("/ ..:..:..$/", "", $form["apply_time"]);
      if( !$form["verified"] )  $verified_text = "<IMG height=20 width=20 src=" . $GRAPH_URL . "X.gif>";
      else			$verified_text = "<IMG height=20 width=20 src=" . $GRAPH_URL . "O.gif>";
            
      $temp = $form["course_id"] . "_" . $form["grp"];
      if( array_key_exists($temp, $selected) ) {			//  學生已選課
        $selected_text = "<IMG height=20 width=20 src=" . $GRAPH_URL . "O.gif>";
      }else{								//  學生尚未選課
        if( $form["verified"] )  {
          $not_selected ++;
          $selected_text = "<IMG height=20 width=20 src=" . $GRAPH_URL . "X.gif>"; 
        }else{
          $selected_text = "--";
        }
      }
	  	  
      echo "
        <TR>
          <TD align=CENTER>" . $form["apply_time"] . "</TD>
          <TD align=CENTER>" . $verified_text . "</TD>
          <TD align=CENTER>" . $selected_text . "</TD>
          <TD align=CENTER>" . $form["course_id"] . "</TD>
          <TD align=CENTER>" . $form["grp"] . "</TD>
          <TD>" . ($IS_ENGLISH ? $form['ename'] : $form["cname"]) . "</TD>
        </TR>
      ";
    }
    echo "</TABLE>";
    if( $not_selected ) {
      echo "<P><FONT color=RED>" . $txt['not_sel1'] .  $not_selected . $txt{'not_sel2'} . "</FONT>";
    }
    //list($concent_form_allowed, $cf_msg) = Concent_Form_Allowed();          /// 目前是否允許申請加簽 
	list($concent_form_allowed, $cf_msg) = Apply_Form_Allowed("concent");          /// 目前是否允許申請加簽 
//    echo $concent_form_allowed . $cf_msg;
    if( $concent_form_allowed == 1 ) {
	  if( $IS_ENGLISH )  $eng = "&e=1";
      echo "<P>【<A href='Add_Course00.cgi?session_id=$session_id$eng'>" . $txt{'add_course'} . "</A>】";
    }
    echo "
      </CENTER><HR><P>
        <B>" . $txt{'note'} . "</B>
        <OL>
          <LI>" . $txt{'note1'} . "
		  <LI>" . $txt{'note2'} . "
		  <LI>" . $txt{'note3'} . "
		  <LI>" . $txt{'note4'} . "
        </OL>
    ";
//    echo "<P><LI>本列表中的「本人已選課」僅供參考，選課狀態以<A href='Selected_View00.cgi?session_id=$session_id'>檢視已選修科目</A>為主";    
  }

}

//print_r($apply_data);

/*
if( $application == -1 ) {		///  尚未加簽過此科目: 新增加簽資料
  $message = "
        您正要申請加簽此科目：  
        <P>  
        <CENTER>  
          <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
        </CENTER>  
        <P>  
        是否正確？  
        若是請點選「是，我要申請」，並列印下頁加簽單。  
  ";
  $submit_text = "是，我要申請";
}else{					///  曾經加簽過此科目: 帶出舊資料
  $message = "
        您已經在 " . $application["apply_time"] ." 申請加簽過此科目：
        <P>  
        <CENTER>  
          <B><U>" . $course["cname"] . "(代碼 $cid 班別 $grp)</U></B>  
        </CENTER>  
        <P>  
        若要重新列印請點選「是，我要重新列印」，並列印下頁加簽單。
  ";
  $submit_text = "是，我要重新列印";
}

//print_r($application);

echo "
  <P>
  <TABLE border=1 width=50%>
    <TR>
      <TD bgcolor=LIGHTYELLOW>$message</TD>
    </TR>
  </TABLE>
 
  <FORM action='Concent_Form_Apply2.php' method='POST'>
    <INPUT type=SUBMIT value='$submit_text'>
    <INPUT type=BUTTON value='否，我要回上頁' onclick='javascript:history.back()'>
  </FORM>
";
*/
//////////////////////////////////////////////////////////////////////////////////////
function Print_HTML_Banner()
{
  global $EXPIRE_META_TAG, $BG_PIC, $GRAPH_URL, $HEAD_DATA;

  print "
    <HTML>
      <HEAD>
        <TITLE></TITLE>
        $EXPIRE_META_TAG
      </HEAD>
    <BODY background='$BG_PIC'>
      <CENTER>
        $HEAD_DATA
        <HR>
  ";
}
  //////////////////////////////////////////////////////////////////////////////////////////////
  /////  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2015/05/06
  function Init_Text_Values()
  {
    global $IS_ENGLISH, $KIKI_URL, $HOME_URL, $CLASS_URL, $QUERY_URL;
	global $session_id, $student, $ban_res_time, $password_last_time;
	global $system_settings, $year, $term;
		
	$sname = $IS_ENGLISH ? $student['ename'] : $student['name'];
	$last_term_get_str = '';
	if( $system_settings['redirect_to_query'] == 1 ) {
	  $last_term_get_str = '&year=' . $year . '&term=' . $term;
	}
	
	$txtall = array(
	  'html_title'	=> array('c'=>'我的加簽單', 'e'=>'My Course Adding Slip'), 
	  'title'		=> array('c'=>'我的加簽單', 'e'=>'My Course Adding Slip'), 
	  'not_found'	=> array('c'=>'您尚未申請任何加簽單！', 'e'=>"You havn't applied for any course adding slip yet."),
	  
	  'apply_time'	=> array('c'=>'申請時間', 'e'=>'Time of aplication'),
	  'review'		=> array('c'=>'教學組審核', 'e'=>'Education Section Review'),
	  'selected'	=> array('c'=>'本人已選課', 'e'=>'Course Selected'),
	  'cid'			=> array('c'=>'科目代碼', 'e'=>'Course ID'),
	  'group'		=> array('c'=>'班別', 'e'=>'Class'),
	  'cname'		=> array('c'=>'科目名稱', 'e'=>'Course Title'),
	  'not_sel1'	=> array('c'=>'您擁有', 'e'=>'There are '),
	  'not_sel2'	=> array('c'=>'門已通過審核但尚未選課的加簽申請單，請儘速於選課截止前自行加選！', 
							 'e'=>"course approved, but you hav't selected yet. Please select these courses before ASAP."),
	  'add_course'	=> array('c'=>'新增加簽課程', 'e'=>'Apply for another course adding slip'),
	  
	  'note'		=> array('c'=>'請注意：', 'e'=>'Please note that:'),
	  'note1'		=> array('c'=>'<FONT color="RED">加簽通過不代表無條件可選上。</FONT>加簽僅可迴避以下幾點： 
								限修人數額滿限制、擋修系所年級班級限制、先修課程限制、每學期限修一門軍訓課限制、
								第二階段不開放加選語言中心課程。', 
							 'e'=>'Completed the signatures of the slip does not mean the course is selected successfully. 
								The slip is limited to the following circumstances: course full; course is limited to certain departments, majors, and classes; prerequisite courses; a military training course only per semester; Language Center’s courses on the second phase of course adding or dropping.'),
	  'note2'		=> array('c'=>'其餘如重複修習、衝堂等限制，不在加簽範圍。', 
							 'e'=>'Limitations also include the refresher course and time conflict courses.'),
	  'note3'		=> array('c'=>'若有超修需求，請至教學組辦理超修手續。', 
							 'e'=>'For taking exceed courses, please file the application in Education Section.'),
	  'note4'		=> array('c'=>'若系統上無加簽選項，但確實有加簽需求，請逕洽教學組以特例辦理。', 
							 'e'=>'If there is no course adding option shown on the system when you need to do course adding,
								please report to the Education Section'),
	  

	  
	  'announce'	=> array('c'=>'選課系統公告', 'e'=>'Announcement', 
						'url'=>'announce.php?session_id=' . $session_id),
	  'about'		=> array('c'=>'選課系統相關', 'e'=>'Course Selection Menu'),
	  'add'			=> array('c'=>'加選', 'e'=>'Add', 
						'url'=> 'Add_Course00.cgi?session_id=' . $session_id),
	  'del'			=> array('c'=>'退選', 'e'=>'Drop',
						'url'=> 'Del_Course00.cgi?session_id=' . $session_id),
	  'view'		=> array('c'=>'檢視已選修科目', 'e'=>'Preview Courses Selected', 
						'url'=> 'Selected_View00.cgi?session_id=' . $session_id),
	  'view_warning'=> array('c'=>'檢視篩選公告', 'e'=>'View Course Screening Result',
						'url'=> 'View_Warning.cgi?session_id=' . $session_id),
	  'view_pdf'	=> array('c'=>'檢視選課結果單PDF', 'e'=>'View Final Courses Selection List',
						'url'=> 'Print_Course_pdf.cgi?session_id=' . $session_id),
	  'my_concent'	=> array('c'=>'我的加簽單', 'e'=>'View Add Permission Form',
						'url'=> 'My_Concent_Forms.php?session_id=' . $session_id),
	  'print'		=> array('c'=>'列印選課單', 'e'=>'Print Final Course Selection List',
						'url'=> 'Print_Course.cgi?session_id=' . $session_id),
	  'change_pwd'	=> array('c'=>'更改密碼', 'e'=>'Change Password',
						'url'=> 'Change_Password00.php?session_id=' . $session_id),
	  'support'		=> array('c'=>'支援本班課程', 'e'=>'Courses with Priority Screening',
						'url'=> 'Support_Courses.cgi?session_id=' . $session_id),
	  'query'		=> array('c'=>'資料查詢', 'e'=>'Search'),
	  'query_course'=> array('c'=>'查詢開課資料', 'e'=>'Browse Courses',
						'url'=> $HOME_URL . 'Course/index.html'),
	  'query_adv'	=> array('c'=>'進階開課資料查詢', 'e'=>'Advanced Course Search',
						'url'=> '../Query/Query_by_time1.cgi?session_id=' . $session_id . '&get_my_table=1'),
	  'show_gro'	=> array('c'=>'跨領域學程', 'e'=>'Interdisciplinary Courses', 
						'url'=> 'Show_All_GRO.cgi?session_id=' . $session_id),
	  'update_course'=> array('c'=>'所有異動科目', 'e'=>'Courses with Recent Revision',
						'url'=> 'Update_Course.php'),
	  'query_grade'	=> array('c'=>'成績查詢', 'e'=>'Grade Inquiry',
						'url'=> '../Query/index.html'),
	  'print_last'	=> array('c'=>'上學期功課表', 'e'=>'Course Schedule(Last Semester)',
						'url'=>'Selected_View00.cgi?year=' . $year . '&term=' . $term . '&session_id=' . $session_id),
	  'view_last'	=> array('c'=>'上學期選課單', 'e'=>'Course List(Last Semester)',
						'url'=>'Print_Course.cgi?year=' . $year . '&term=' . $term . '&session_id=' . $session_id),
	  'qa'			=> array('c'=>'問題與表單下載', 'e'=>'Q&A and Download'),
	  'general_qa'	=> array('c'=>'一般問題', 'e'=>'General Q&A',
						'url'=> $KIKI_URL . 'contact.html'),
	  'manual'		=> array('c'=>'系統操作手冊', 'e'=>'User Manual',
						'url'=> $KIKI_URL . 'user_manual/user_manual.htm'),
	  'doc'			=> array('c'=>'課表doc檔', 'e'=>'Schedule Template(doc file)',
						'url'=> $KIKI_URL . 'ccu_timetable.doc'),
	  'pwd_remind'	=> array('c'=>'提醒您, 選課密碼請定期更新(最好三個月一次), 以策安全!<BR>' 
							. '您的密碼已經有 ' . $password_last_time . ' 天沒有更新了!',
						'e'=>'You have not changed your password for ' . $password_last_time 
							. ' days. Please do it now before you login to the system.'),
	  'pwd_default'	=> array('c'=>'<FONT color=RED size=-1>您使用預設密碼或是尚未填寫 email 信箱，請先 '
							. '<A target=basefrm href="Change_Password00.php?session_id=' . $session_id . '">更新您的密碼</A><FONT>', 
						'e'=>'You are now either still using the default password or havn\'t'
							. ' provided your E-mail address, please change your password first.'),
	  'pwd_remind2'	=> array('c'=>'您的密碼已經有 ' . $password_last_time . ' 天沒有更新了!<BR>'
							. '<FONT color=RED>您必須先更新密碼後，方能選課!</FONT>' 
							. '<P><A href="Change_Password00.php?session_id=' . $session_id . '" target=basefrm>更新密碼與email信箱</A><P>', 
						'e'=>'You have not changed your password for ' . $password_last_time 
							. ' days. Please do it now before you login to the system.'
							. '<P><A href="Change_Password00.php?e=1&session_id=' . $session_id . '" target=basefrm>Click here to change password.</A><P>'),
	  'new_msg'		=> array('c'=>'您有一封來自系統的訊息!!', 'e'=>'You have a new message!!'),
	  'ban_msg'		=>array('c'=>'停權公告', 'e'=>'Ban Message',
						'url'=>'Show_Ban_Message.php?ban_res_time=' . $ban_res_time),
	  'withdrawal'	=> array('c'=>'申請棄選', 'e'=>'Withdrawal Application',
						'url'=>'Selected_View00.cgi?session_id=' . $session_id . $last_term_get_str),
	  'my_withdrawal'	=> array('c'=>'我的棄選單', 'e'=>'My Withdrawal Application Form',
						'url'=>'My_Withdrawal_Form.php?session_id=' . $session_id),
	  'my_plan'		=> array('c'=>'<SPAN style="background:YELLOW; color:RED">我的選課計畫</SPAN>', 
						'e'=>'<SPAN style="background:YELLOW; color:RED">My Course Plans</SPAN>',
						'url'=>'My_Plan_Course.php?session_id=' . $session_id),
	  'graduate'	=> array('c'=>'檢視畢業資格審查表', 'e'=>'Qualification Form for Graduation',
						'url'=>'Print_Graduate_pdf.cgi?session_id=' . $session_id),
	  'logout_btn'	=> array('c'=>'登出系統', 'e'=>'logout'),
	);

	foreach( $txtall as $k=>$v ) {
	  if( $IS_ENGLISH )	{
	    $txt[$k] = $v['e'];
		if( isset($v['url']) ) {
		  if( strstr($v['url'], "?") )
		    $txt[$k."_url"] = $v['url'] . "&e=1";
		  else
		    $txt[$k."_url"] = $v['url'] . "?e=1";
		}
	  }else{
	    $txt[$k] = $v['c'];
		if( isset($v['url']) )
		  $txt[$k."_url"] = $v['url'];
	  }
	}	
    return $txt;
  }
  


?>