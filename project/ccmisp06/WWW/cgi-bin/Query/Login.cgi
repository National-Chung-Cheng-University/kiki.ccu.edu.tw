#!/usr/local/bin/perl
###########################################################################
#####  Login.cgi
#####  查詢選課學生名單
#####  列出系所供選擇.
#####  系統關閉查詢功能時, 會不允許查詢
#####  Modified: 
#####    2001/09/11
#####    2009/05/13 將系所查詢的也指過來，另，判斷傳入系所代碼，帶出為預設值
#####    2009/12/29 可查詢最近六個學期的修課名單  Nidalap :D~
#####    2010/04/20  系所下拉選單加入 optgroup 以示區別學院 Nidalap :D~
#####    2010/06/08 馬賽克改為只針對未經系所登入者才會做。  Nidalap :D~
#####  Coder: Nidalap :D~
###########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Select_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

%Input = User_Input();
#foreach $key (keys %Input) {
#  print("$key -> $Input{$key}<BR>\n");
#}

$sys_state = Whats_Sys_State();
if( $sys_state == 0 ) {
  print qq(
    <html>
      <head>
        $EXPIRE_META_TAG
        <title>第二版開排課系統</title>
      </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><HR>
         目前系統暫不開放查詢!
  );
}else{
  ($year, $term) = Last_Semester(1);
  %system_settings = Read_System_Settings();

#  foreach $key (keys %system_settings) {   
#    print("$key => $system_settings{$key}<BR>\n");
#  }

  if( $system_settings{redirect_to_query} == 1 ) {			###  如果系統目前正在開新學期的課
    $selected1 = "";							###    那就預設選擇上學期資料
    $selected2 = "selected=\"selected\"";
  }else{
    $selected1 = "selected=\"selected\"";
    $selected2 = "";
  }

  print qq(
    <html>
      <head>
	    $EXPIRE_META_TAG
		<title>第二版開排課系統</title>
	  </head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><p>
         <h4>請選擇「開課」系所</h4><p><br>
         <form method=post action=Query_1.cgi>
		   <INPUT type='hidden' name='open_dept' value="$Input{open_dept}">
           <table border=0>
             <tr>
               <th><h3>系別:</h3></th>
               <td><select name=dept_cd>
  );
  my(@Dept,$dept,%Dept);
  @Dept=Find_All_Dept("NO_COM_DEPT");

%college = Read_College();
$last_college = "";
foreach $dept (@Dept)
{
  %Dept=Read_Dept($dept);
  if( is_GRA() == 1 ) {
    next if( $dept !~ /6$/ );
  }
  if( $last_college ne $Dept{college} ) {
    print qq[</optgroup>]  if( $last_college ne "" );
    print qq[<optgroup label="$college{$Dept{college}}">];
  }
  $last_college = $Dept{college};  
  if( $Dept{id} eq $Input{dept_id} ) {				###  若由系所登入
    print("<option value=$Dept{id} SELECTED>$Dept{cname2}\n");	###  將該系設為預設值
  }else{
    print("<option value=$Dept{id}>$Dept{cname2}\n");  		###  若無，不特定設定預設值
  }
}
#  foreach $dept(@Dept) {
#    if( $dept eq $Input{dept_id} ) {
#      $selected = "SELECTED";
#    }else{
#      $selected = "";
#    } 
#    %Dept=Read_Dept($dept);
#    print "<option value=$Dept{id} $selected>$Dept{cname}\n";
#  }


  print qq(
                  </select>
               </td>
             </tr>
           </table>
           <INPUT type=CHECKBOX name=query_count value=1>查詢各科目選課人數<P>
           <SELECT name=last_semester>
  );
  for( $i=0; $i<6; $i++ ) {
    ($year, $term) = Last_Semester($i);
    print("<OPTION value=$i ");
    print("SELECTED ")  if( $i==0 );
    print(">$year 學年度第 $term 學期資料</OPTION>\n");
  }
  print qq(
           </SELECT>
           <P>
  );
  
  if( $Input{dept_id} and $Input{password} ) {		###  只有系所登入要傳此值
    print qq(
      <INPUT type="hidden" name="login_dept_id" value="$Input{dept_id}">
      <INPUT type="hidden" name="password"      value="$Input{password}">
    );
  }
  print qq(
           <input type="submit" value="資料填寫完畢"> 
         </form>
       </center>
     </body>
   </html>
  );
}
