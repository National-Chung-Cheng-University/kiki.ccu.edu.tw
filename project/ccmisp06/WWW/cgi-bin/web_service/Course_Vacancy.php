<?PHP

//////////////////////////////////////////////////////////////////////////////////
/////  Course_Vacancy.php
/////  �]�Ѯջڿ�Ҩt�Ρ^�ǤJ�ҵ{�N�X�B�Z�O�B�}�Ҩt�ҡA�Ψ�L�w���ˬd��T�A
/////  �^�Ǧ��ҵ{�ثe�|�i��פH�Ƶ���T�A�ѧP�_�ջڥͿ�ҬO�_�ݥ[ñ�C
/////  �^�Ǹ�ơG
/////    �Y���}�Ҹ��: (�}�ҭ��פH�� - �ثe��ҤH��), �}�ҭ��פH��, �ثe��ҤH��
/////    �Y�L�}�Ҹ��: -1
/////  2016/04/18 Created by Nidalap :D~
/////  2016/05/18 �Y�䤣��}�Ҹ�ơA�h�^�� -1�C  by Nidalap :D~
/////  2016/08/31 ���u�^�ǥi�[��H�ơA�אּ�^�ǥi�[��H�ơB���פH�ơB�ثe��ҤH�ơC by Nidalap :D~

require_once "../library/Reference.php";
require_once $LIBRARY_PATH . "Database.php";
require_once $LIBRARY_PATH . "Common_Utility.php";
require_once $LIBRARY_PATH . "Dept.php";
require_once $LIBRARY_PATH . "Course.php";
require_once $LIBRARY_PATH . "Password.php";
require_once $LIBRARY_PATH . "Student_Course.php";
require_once $LIBRARY_PATH . "Error_Message.php";

$system_settings = Get_System_State();

$cour_id	= Verify_Specific_Data($_REQUEST['cour_id'], "course_id");
$grp		= Verify_Specific_Data($_REQUEST['grp'], "grp");
$password	= Verify_Specific_Data($_REQUEST['password'], "text", 20);
$key		= Verify_Specific_Data($_REQUEST['key'], "text", 20);

//die("2,60,58");


if( array_key_exists("dept_id", $_REQUEST) ) {			///  �p�G�ǤJ�F�t�ҥN�X�A�ϥΦ����
  $dept_id	= Verify_Specific_Data($_REQUEST['dept_id'], "dept_id");
}else{													///  �p�G�S���ǤJ�}�Ҩt�ҥN�X�A�o��������X�ӡ]����C�^
  $all_course_dept = Read_All_Course_Dept();
  $dept_id = $all_course_dept[$cour_id]["dept_id"];
  
  //print_r($all_course_dept);
  
  if( !array_key_exists($cour_id, $all_course_dept) ) {	///  �p�G�䤣��t�ҡ]�}�Ҹ�Ƥ��s�b�^�A�^�� -1
	echo "-1";
	die();
  }
}

//Check_Key($key, $cour_id.$grp, $password);			///  �w���ˬd: �ˬd $key �O�_���T
//Check_Source_URL();									///  �w���ˬd: �ˬd�ӷ����� URL

//echo "$id, $password<br>\n";
//echo '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">';

//echo "[$dept_id, $cour_id, $grp]<BR>\n";

$course = Read_Course($dept_id, $cour_id, $grp);		///  ����}�Ҹ��

if( preg_match("/FONT color/", $course['cname']) ) {	///  �p�G�䤣��t�ҡ]�}�Ҹ�Ƥ��s�b�^�A�^�� -1
  echo "-1";
  die();
}
//print_r($course);

$stu_in_cour = Student_in_Course($cour_id, $grp);		///  ����ثe��ҦW��
$stu_in_cour = count($stu_in_cour);						///  �ثe��ҤH��

$vacancy = $course["number_limit"] - $stu_in_cour;

if( $vacancy < 0 )  $vacancy = 0;

$vacancy_str = implode(",", array($vacancy, $course["number_limit"], $stu_in_cour));
echo $vacancy_str;
  
?>