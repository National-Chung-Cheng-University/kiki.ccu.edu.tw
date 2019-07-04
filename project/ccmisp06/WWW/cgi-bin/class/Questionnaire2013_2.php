<?PHP
  ///////////////////////////////////////////////////////////////////////////////////////////
  /////  Questionnaire2013_1.php
  /////  中正大學選課系統暨通識篩選原則意見調查表
  /////  2013/09 為調查同學對於因通識課程而起的選課制度改革意見，提供的問卷。
  /////  Updates:
  /////    2013/08/30 Created by Nidalap :D~
  
  require_once "../php_lib/Reference.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Dept.php";
  
  $session_id	= $_POST["session_id"] ? $_POST["session_id"] : $_GET["session_id"];
  global $BG_PIC;
  
  $q1		= quotes($_POST['q1']);
  $q2		= quotes($_POST['q2']);
  $q3		= quotes($_POST['q3']);
  $q1_note	= quotes($_POST['q1_note']);
  $q2_note	= quotes($_POST['q2_note']);
  $q3_note	= quotes($_POST['q3_note']);
  
  $test = 0;
  if( !$test ) {
    $session_data	= Read_Session($session_id);
    $id				= $session_data{"id"};
    $password		= $session_data{"password"};
    $login_time		= $session_data{"login_time"};
    $ip				= $session_data{"ip"};
    $student = Read_Student($id);
    $dept = Read_Dept($student{"dept"});
    $HEAD_DATA = Form_Head_Data($id, $student{"name"}, $dept{"cname"}, $student{"grade"}, $student{"class"});
	Check_Password($id, $password, "", "");
  }else{
    $id = "999999999";
	echo "<H1><FONT COLOR=RED>TEST</FONT></H1>";
  }
    
  $DBH = PDO_connect($KIKI_DB_NAME);
  $sql = "SELECT * FROM questionnaire2013 WHERE stu_id = ?";
  $STH = $DBH->prepare($sql);
  $STH->execute(array($id));
  $ques = $STH->fetch(PDO::FETCH_ASSOC);

  $update_time = date('Y-m-d H:i:s');  //time();
  $update_ip = getIP();

  if( $ques ) {											///  已經填過了: UPDATE
	$msg_type = "更改";
	$update_count = $ques['update_count'] + 1;
    $sql = 
	  "UPDATE questionnaire2013 
		  SET q1 = '$q1',
			  q2 = '$q2',
			  q3 = '$q3',
			  q1_note = '$q1_note',
			  q2_note = '$q2_note',
			  q3_note = '$q3_note',
			  update_time = '$update_time',
			  update_count = $update_count,
			  update_ip = '$update_ip'
		WHERE stu_id = '$id'
	  ";
	  
  }else{												///  尚未填過：INSERT
    $msg_type = "填寫";
	$update_count = 0;
    $sql = 
	  "INSERT INTO questionnaire2013
	    (stu_id,q1,q1_note,q2,q2_note,q3,q3_note,update_time,update_count,update_ip)
	   VALUES 
	    (
		  '$id',
		  '$q1', '$q1_note',
		  '$q2', '$q2_note',
		  '$q3', '$q3_note',
		  '$update_time',
		  $update_count,
		  '$update_ip'
		)
	  ";
	  
  }
  
//  echo "sql = $sql<BR>\n";
  if( $STH = $DBH->query($sql) ) {
    $msg = "您已經順利" . $msg_type . "問卷，謝謝您的填答！";
  }else{ 
    echo "問卷更新失敗，請洽系統管理員(校內分機 14203 李先生)<BR>\n";
    print_r($DBH->errorInfo());
  }

  
?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <TITLE>中正大學選課系統暨通識篩選原則意見調查表</TITLE>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
</head>
<body background=<?PHP echo $BG_PIC; ?>>
<center>
  <H2>中正大學選課系統暨通識篩選原則意見調查表</H2>
  <HR>
  <?PHP echo $msg ?>
  <BR>
  如同學欲更改問卷內容，請於選課截止9月30日晚上10點前完成修改。<P>
  <A target="bookmark" href="bookmark.php?session_id=<?PHP echo $session_id ?>">[回主選單]</A>

