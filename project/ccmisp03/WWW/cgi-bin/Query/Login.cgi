#!/usr/local/bin/perl
###########################################################################
#####  Login.cgi
#####  查詢選課學生名單
#####  列出系所供選擇.
#####  系統關閉查詢功能時, 會不允許查詢
#####  Modified: 2001/09/11
#####  Coder: Nidalap :D~
###########################################################################
print "Content-type: text/html","\n\n";

require "../library/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Select_Course.pm";
require $LIBRARY_PATH . "Common_Utility.pm";
require $LIBRARY_PATH . "System_Settings.pm";

$sys_state = Whats_Sys_State();
if( $sys_state == 0 ) {
  print qq(
    <html>
      <head><title>第二版開排課系統</title></head>
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
      <head><title>第二版開排課系統</title></head>
      <body background=$GRAPH_URL/ccu-sbg.jpg>
        <center>
         <img src=$GRAPH_URL/open.jpg><P>
         <h4>查詢修課學生名單功\能</h4><p>
         <h4>請選擇系所</h4><p><br>
         <form method=post action=Query_1.cgi>
           <table border=0>
             <tr>
               <th><h3>系別:</h3></th>
               <td><select name=dept_cd>
  );
  my(@Dept,$dept,%Dept);
  @Dept=Find_All_Dept();
  foreach $dept(@Dept) {
    %Dept=Read_Dept($dept);
    print "<option value=$Dept{id}>$Dept{cname}\n";
  }
  print qq(
                  </select>
               </td>
             </tr>
           </table>
           <INPUT type=CHECKBOX name=query_count value=1>查詢各科目選課人數<P>
           <SELECT name=semester>
             <OPTION value="this" $selected1>$YEAR 學年度第 $TERM 學期資料</OPTION>
             <OPTION value="last" $selected2>$year 學年度第 $term 學期資料</OPTION>
           </SELECT>
           <P>
           <input type="submit" value="資料填寫完畢"> 
           <input type="reset" value="重新填寫資料">
         </form>
       </center>
     </body>
   </html>
  );
}
