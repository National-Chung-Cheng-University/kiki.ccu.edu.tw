1;

############################################################################################
#####  English.pm
#####  英文版選課系統相關函式
#####  Updates:
#####    2013/07/24 從 English.php 移植而來 by Nidalap :D~
 
%Input=User_Input();


###  判別是否行動版，設定變數 IS_MOBILE
if( ($_Input{'m'} == 1 ) or ( $Input{'m'} == 1) ) {
  $IS_MOBILE		=	1;
}else{
  $IS_MOBILE		=	0;
}

###  判別是否英文版，設定變數 IS_ENGLISH
if( $Input{'e'} == 1 ) {
  $IS_ENGLISH		=	1;
}else{
  $IS_ENGLISH		=	0;
}

#print "is english = $IS_ENGLISH<BR>\n";
#####  顯示學年學期文字資訊(英文版不使用學年，而是用西元年)
sub Year_Term_English()
{
  my $term;
  my($sec, $min, $hour, $day, $mon, $year) = localtime(time);
  $year += 1900;
  if( 1 == $TERM ) {			###  上學期
	$term = "Fall";
  }elsif( 2 == $TERM ) {		###  下學期
	$term = "Spring";
  }else{						###  暑修(3)
	$term = "Summer";			###  ???
  }
  return $term . " semester of " . $year;
}

#########################################################################
#####  顯示行動板需要的 jQuery Mobile 引用程式碼
sub Create_jQuery_Mobile_Script
{
  my($dev) = @_;
  
  $html = "<meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=yes, minimum-scale=1.0' />\n";
  
  if( $dev ) {
    $html .= "
	  <link rel='stylesheet' href='http://demos.jquerymobile.com/1.2.0/css/themes/default/jquery.mobile-1.2.0.css' />	  
	  <link rel='stylesheet' href='" . $HOME_URL . "javascript/jquery_mobile/kiki.css' />
	  <script src='https://code.jquery.com/jquery-2.1.3.min.js' /></script>
	  <script src='https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js' /></script>
    ";
  }else{
    $html .= "
	  <link rel='stylesheet' href='" . $HOME_URL . "javascript/jquery_mobile/jquery.mobile.css' />
	  <link rel='stylesheet' href='" . $HOME_URL . "javascript/jquery_mobile/kiki.css' />
	  <script src='" . $HOME_URL . "javascript/jquery.js' /></script>
	  <script src='" . $HOME_URL . "javascript/jquery_mobile/jquery.mobile.js' /></script>
    ";
  }
  return $html;
}
#########################################################################
sub Create_jQuery_Mobile_Title_Tag
{
    return "
	  <DIV data-role='page'>
	  <CENTER>
	  <DIV data-role='header' data-theme='a'>
	    <IMG src='../../Graph/mobile/title310px.gif'>
	  </DIV>
	  <DIV data-role='content'>
	"; 
}	
#########################################################################
sub Create_jQuery_Mobile_Footer_Tag
{
    ($stu_name) = @_;
    #global $student, $id, $session_id;

	#$session_data = Read_Session($session_id);
	#$id	= $session_data{"id"};
	#$Student = Read_Student($id);
	
	#print $Student{name};
	
	my %time = gettime($session_data{'login_time'});
		
	$welcome_msg  =  $stu_name . "同學，歡迎！<BR>\n";
	$welcome_msg .= "您本次的登入時間是:[$time{time_string}]";
    $footer = 
	  "</DIV>
	     <DIV data-role='footer'  data-theme='a'>
	       $welcome_msg
	     </DIV>
	     </CENTER>
	   </DIV>  <!-- page -->
	  ";
	return $footer;
}



1;
