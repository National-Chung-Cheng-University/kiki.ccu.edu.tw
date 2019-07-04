<?PHP
  ///////////////////////////////////////////////////////////////////////////////////////////
  /////  Questionnaire2013_0.php
  /////  中正大學選課系統暨通識篩選原則意見調查表
  /////  此頁顯示一些訊息，然後導到 Questionnaire2013_1.php
  /////  Updates:
  /////    2013/09/06 Created by Nidalap :D~
  
  require_once "../php_lib/Reference.php";
  require_once $LIBRARY_PATH . "Common_Utility.php";
  require_once $LIBRARY_PATH . "Session.php";
  require_once $LIBRARY_PATH . "Password.php";
  require_once $LIBRARY_PATH . "Database.php";
  require_once $LIBRARY_PATH . "Student.php";
  require_once $LIBRARY_PATH . "Dept.php";
  
  $session_id	= $_POST["session_id"] ? $_POST["session_id"] : $_GET["session_id"];

  global $BG_PIC;

  $test = 0;
  if( !$test ) {
    $session_data	= Read_Session($session_id);
    $id				= $session_data{"id"};
    $password		= $session_data{"password"};
    $login_time		= $session_data{"login_time"};
    $ip				= $session_data{"ip"};
    $student		= Read_Student($id);
    $dept			= Read_Dept($student{"dept"});
//    $HEAD_DATA = Form_Head_Data($id, $student{"name"}, $dept{"cname"}, $student{"grade"}, $student{"class"});
//    $HEAD_DATA = Form_Head_Data($id, $student{name}, $dept{cname}, $student{grade}, $student{class});
    Check_Password($id, $password, "", "");
  }else{
    $id = "999999999";
	echo "<H1><FONT COLOR=RED>TEST</FONT></H1>";
  }
  
  $DBH = PDO_connect($KIKI_DB_NAME);
  $sql = "SELECT * FROM questionnaire2013 WHERE stu_id = ?";
  $STH = $DBH->prepare($sql);
  $STH->execute(array($id));
  $ques = $STH->fetch();
?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <TITLE>中正大學選課系統暨通識篩選原則意見調查表</TITLE>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
</head>
<body background=<?PHP echo $BG_PIC; ?>>
<center>
  <?PHP //echo $HEAD_DATA; ?>
    <TABLE border=0 width=70%>
      <TR><TD align=CENTER>
        <H2>中正大學選課系統暨通識篩選原則意見調查表</H2>
      </TD></TR>
	  <TR><TD align="CENTER">
	    本校選課系統將有重大變革！為了解您對選課制度變革的意見，煩請您撥空填答問卷，<BR>
		如同學欲更改問卷填答的內容，請於選課截止9月30日晚上10點前完成修改，<BR>
		為使問卷結果能公正的代表同學們真正的意見，每位同學帳號將僅能填答一份問卷。<BR>
		填答內容以最終修改之結果為準，謝謝您的協助!!
		<P>
		<CENTER>
		  <A href='Questionnaire2013_1.php?session_id=<?PHP echo $session_id ?>'>請點選此處以填寫問卷</A>
		</CENTER>
	  </TD>
    </TABLE>
  </FORM>
</BODY>
  <!--  <script type="text/javascript" src="https://www.google.com/jsapi"></script>  -->
  <SCRIPT type="text/javascript" src="../../javascript/jquery.js"></SCRIPT>
  <script type="text/javascript" language="JavaScript">
//    google.load("jquery", "1.6.2");   
//    alert("ccc");
    $(document).ready(function(){
      $('#my_form').preventDoubleSubmit();
      jQuery.fn.preventDoubleSubmit = function() {
        jQuery(this).submit(function() {
          if (this.beenSubmitted)
            return false;
          else
           this.beenSubmitted = true;
        });
      };
//      $("#submit").click(function(){
//        $(this).attr("disabled", "disabled");
//        alert("ccc");
//        return true;
        
//        $("#form1").submit();
//        $(this).attr("disabled", "disabled");
//        alert("ddd");
//      })
    });
  </SCRIPT>
</HTML>

