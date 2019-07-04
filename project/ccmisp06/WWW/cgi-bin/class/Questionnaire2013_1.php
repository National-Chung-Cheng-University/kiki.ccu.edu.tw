<?PHP
  ///////////////////////////////////////////////////////////////////////////////////////////
  /////  Questionnaire2013_1.php
  /////  中正大學選課系統暨通識篩選原則意見調查表
  /////  2013/09 為調查同學對於因通識課程而起的選課制度改革意見，提供的問卷。
  /////  Updates:
  /////    2013/08/28 Created by Nidalap :D~
  
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
  <FORM action="Questionnaire2013_2.php" method=POST id="my_form">
    <TABLE border=0 width=75%>
      <TR><TD align=CENTER>
        <H2>中正大學選課系統暨通識篩選原則意見調查表</H2>
      </TD></TR>
	  <TR><TD>
	    親愛的同學好：
		<P>
		感謝您撥空填寫此份問卷！本問卷的目的在了解您對選課制度變革的意見，據以改善選課制度。
		為使問卷結果能公正的代表同學們真正的意見，每位同學帳號將僅能填答一份問卷，謝謝您的協助!!
		下述修改方案，將彙整各方意見，提教務會議討論，全面宣導後，預計最快於102學年度第2學期實施。
		<P>
		壹、現況
		<P>
		據部分同學反應，目前的通識課程選課讓部分同學有些困擾，包括亂數篩選導致「貧富不均」、
		先搶先贏時段有私自換課疑慮、同學為了想要選到想選的課，長時間守在電腦前等等。
		為解決上述狀況，通識中心、教學組、電算中心及學生會代表多次開會討論，
		並舉辦三次公聽會(分別為5/6與5/8中午12:10，5/13下午6:30)，討論出以下修改方案，
		今欲全面調查全校同學的意見，以做為決定之參考。
		<P>
		請詳閱：<A href="../../201309Course_Change.ppt">2013選課機制改革-教務會議.ptt</A>
		<P>
		貳、修改方案
		<P>
		<!---  問題一  --->
		<TABLE border=0 width=100%>  
		  <TR><TD bgcolor='LIGHTBLUE'>
		    一、一般選課
			<P>
			(一)第一階段選課擬由一次篩選，改為三次篩選，詳述如下：
		    <P>
		    為使多數同學於開學前確知選上何門課程，並解決開學期間出席率太低狀況，
		    第一階段選課擬由一次篩選，改為三次篩選；由於篩選次數增加，第一階段選課時間將延長。
		    <P>
		    <TABLE border=0>
		      <TR>
		        <TD width="20">
			    <TD>
			      <INPUT type="radio" name="q1" value="1" <?PHP if($ques['q1']==1) echo "CHECKED" ?>>贊成<BR>
			      <INPUT type="radio" name="q1" value="2" <?PHP if($ques['q1']==2) echo "CHECKED" ?>>不贊成<BR>
			      <INPUT type="radio" name="q1" value="3" <?PHP if($ques['q1']==3) echo "CHECKED" ?>>其他<BR>
			    </TD>
			    <TD>
			      看法如下：<BR>
			      <TEXTAREA rows=10 cols=60 name="q1_note"><?PHP echo $ques['q1_note']; ?></TEXTAREA>
			    </TD>
		      </TR>
		    </TABLE>
		  </TR></TD>
		</TABLE>

		<!---  問題二  --->
		<TABLE border=0 width=100%>  
		  <TR><TD bgcolor='LIGHTGREEN'>
		    (二)第二階段選課擬由第一週篩選及第二週先選先贏，改為每日三段式選課，詳述如下：
		    <P>
		    為解決第二階段選課第二週(先選先贏時段)同學頻繁換課，及同學因長時間在線上選課致缺課等問題，故第二階段擬改為每日三段式選課。
		    <OL>
		      <LI>系統於第二階段第一天中午12點開放，至第三天早上8點關閉，進行篩選，這段時間系統可加選退選。
		      <LI>從第四天開始每日三段式選課
		      <UL>
			    <LI>每天06:00 – 14:00為退選時段(本時段只可退選課表內之課程，不可加選任何課程)
				<LI>每天16:00 – 20:00為篩選制之加選時段(本時段只可加選，當梯次誤加選之課程可退選)，本次加選之課程須跑篩選。
				<LI>每天20:00 – 22:00為篩選制之篩選時段，系統關閉跑篩選。
				<LI>每天22:00 – 24:00為先選先贏之加選時段(本時段只可加選，當梯次誤加選之課程可退選)。
				<LI>每天24:00 – 06:00系統關閉。
			</OL>
		    <P>
		    <TABLE border=0>
		      <TR>
		        <TD width="20">
			    <TD>
			      <INPUT type="radio" name="q2" value="1" <?PHP if($ques['q2']==1) echo "CHECKED" ?>>贊成<BR>
			      <INPUT type="radio" name="q2" value="2" <?PHP if($ques['q2']==2) echo "CHECKED" ?>>不贊成<BR>
			      <INPUT type="radio" name="q2" value="3" <?PHP if($ques['q2']==3) echo "CHECKED" ?>>其他<BR>
			    </TD>
			    <TD>
			      看法如下：<BR>
			      <TEXTAREA rows=10 cols=60 name="q2_note"><?PHP echo $ques['q2_note']; ?></TEXTAREA>
			    </TD>
		      </TR>
		    </TABLE>
		  </TR></TD>
		</TABLE>
		
		<!---  問題三  --->
		<TABLE border=0 width=100%>  
		  <TR><TD bgcolor='LIGHTBLUE'>
		    二、通識選課
			<P>
			通識二至五領域篩選原則，擬由隨機亂數篩選修改為權重篩選，詳述如下：
			<P>
			通識課程目前實施之篩選原則：二至五領域以大四欠缺該領域學生優先，其餘隨機亂數篩選，
			易造成運氣差之同學於第一階段選課結束後，未選上足夠之通識課程，或未選上任一門通識課程，
			造成貧富不均，故擬調整篩選原則為：
			<OL>
			  <LI>依照選上的科目數量，採優先權逐科下降。(前2門課權重為10，第3門課之權重為9，依此類推)。
			  <LI>當選修人數大於開課人數，權重高的同學優先選上該門課程，權重相同的同學採隨機篩選。
			</OL>
		    <P>
		    <TABLE border=0>
		      <TR>
		        <TD width="20">
			    <TD>
			      <INPUT type="radio" name="q3" value="1" <?PHP if($ques['q3']==1) echo "CHECKED" ?>>贊成<BR>
			      <INPUT type="radio" name="q3" value="2" <?PHP if($ques['q3']==2) echo "CHECKED" ?>>不贊成<BR>
			      <INPUT type="radio" name="q3" value="3" <?PHP if($ques['q3']==3) echo "CHECKED" ?>>其他<BR>
			    </TD>
			    <TD>
			      看法如下：<BR>
			      <TEXTAREA rows=10 cols=60 name="q3_note"><?PHP echo $ques['q3_note']; ?></TEXTAREA>
			    </TD>
		      </TR>
		    </TABLE>
		  </TR></TD>
		</TABLE>		
	  </TD>
    </TABLE>
    <INPUT type=hidden name="session_id" value="<?PHP echo $session_id; ?>">
    <INPUT type="submit" value="送出問卷" id="submit"><p>

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

