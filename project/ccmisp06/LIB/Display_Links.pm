1;

sub Links1
{
 ($t1,$t2,$t3,$crypt,$t4)=@_;

 if($crypt eq "") {  $crypt = "1"; }
 print "<table border=0 width=50%><tr><th>
         <form>
         <input type=button onclick=history.back() value=回上一畫面>
         </form></th><th>
         <form action=Class_Menu.cgi method=post>
         <input type=hidden name=session_id value=\"$Input{session_id}\">
         <input type=hidden name=dept_cd value=$t1>
         <input type=hidden name=grade value=$t2>
         <input type=hidden name=password value=$t3>
         <input type=hidden name=crypt value=$crypt>
		 <input type=hidden name=open_dept value=$t4>
         <input type=submit value=回開課主選單>
         </form></th>
         </tr><tr>
         <th><a href=\"http://www.ccu.edu.tw\" target=_top>回到中正大學首頁</a></th>
         <th><a href=\"$HOME_URL\" target=_top>回到開排課系統首頁</a> </th>
         </tr></table>"; 
}

sub Links2
{
 print "<table border=0 width=50%><tr><th colspan=2>
         <form>
         <input type=button onclick=history.back() value=回上一畫面>
         </form></td></tr><tr>
         <th><a href=\"http://www.ccu.edu.tw\" target=_top>回到中正大學首頁</a></th>
         <th><a href=\"$HOME_URL\" target=_top>回到開排課系統首頁</a 
         </tr></table>"; 
}
##########################################################################
sub Links3                        ## 同Link1, 但沒有回上一頁的選項
{
 ($t1,$t2,$t3,$t4)=@_;
 print "<p><center>
          <form method=post
                action=Class_Menu.cgi>
          <input type=hidden name=session_id value=\"$Input{session_id}\">
          <input type=hidden name=dept_cd value=$t1>
          <input type=hidden name=grade value=$t2>
          <input type=hidden name=password value=$t3>
		  <input type=hidden name=open_dept value=$t4>
          <input type=hidden name=crypt value=1>
          <input type=submit value=回開課主選單>
          </form>
         <a href=\"http://www.ccu.edu.tw\" target=_top>回到中正大學首頁</a>
         <a href=\"$HOME_URL\" target=_top>回到開排課系統首頁</a> </th>
  ";
}


sub Select_Course_Link  ##  普通一般的連結
{
my($id, $password)=@_;
my($Buffer)="";

$Buffer=$Buffer."    <center>\n";
$Buffer=$Buffer."    <hr size=1>\n";
$Buffer=$Buffer."   <script language=\"JavaScript\" src=\"ActionLocation\.js\">\n";
$Buffer=$Buffer."    </script>\n";
$Buffer=$Buffer."    <form action=\"\" name=\"MainMenuForm\" method=POST>\n";
$Buffer=$Buffer."        <input type=hidden name=session_id value=\"";
$Buffer=$Buffer.$Input{session_id}."\">\n";
$Buffer=$Buffer."    <table border=0 size=640>\n";
$Buffer=$Buffer."    <tr>\n";
$Buffer=$Buffer."      <th>\n";
$Buffer=$Buffer."        <input type=button value=\"回主選單\" onClick=\"SelectAction(0)\">\n";
$Buffer=$Buffer."      </th>\n";
#$Buffer=$Buffer."      <th>\n";
#$Buffer=$Buffer."        <input type=button value=\"回加選分類表\" onClick=\"SelectAction(1)\">\n";
#$Buffer=$Buffer."      </th>\n";
#$Buffer=$Buffer."      <th>\n";
#$Buffer=$Buffer."        <input type=button value=\"至退選選單\" onClick=\"SelectAction(2)\">\n";
#$Buffer=$Buffer."      </th>\n";
#$Buffer=$Buffer."      <th>\n";
#$Buffer=$Buffer."        <input type=button value=\"檢視已選修科目\" onClick=\"SelectAction(4)\">\n";
#$Buffer=$Buffer."      </th>\n";
$Buffer=$Buffer."    </tr>\n";
$Buffer=$Buffer."    </table>\n";
$Buffer=$Buffer."    </form>\n";
$Buffer=$Buffer."    </center>\n";


return($Buffer);
}

sub Select_Course_Link_2
{
my($id, $password)=@_;
my($Buffer)="";

$Buffer=$Buffer."    <center>\n";
$Buffer=$Buffer."    <hr size=1>\n";
$Buffer=$Buffer."   <script language=\"JavaScript\" src=\"ActionLocation\.js\">\n";
$Buffer=$Buffer."    </script>\n";
$Buffer=$Buffer."    <form action=\"\" name=\"MainMenuForm\" method=POST>\n";
$Buffer=$Buffer."	 <input type=hidden name=session_id value=\"";
$Buffer=$Buffer.$session_id."\">\n";
$Buffer=$Buffer."    <table border=0 size=640>\n";
$Buffer=$Buffer."    <tr>\n";
$Buffer=$Buffer."      <th>\n";
$Buffer=$Buffer."	 <input type=button value=\"回主選單\" onClick=\"SelectAction(0)\">\n";
$Buffer=$Buffer."      </th>\n";
$Buffer=$Buffer."    </tr>\n";
$Buffer=$Buffer."    </table>\n";
$Buffer=$Buffer."    </form>\n";
$Buffer=$Buffer."    </center>\n";

return($Buffer);
}
###########################################################################################
#####  因為加了 CGI.pm, 不在 form 中傳 hidden value
#####  Added on 2005/02/16 Nidalap :D~

sub Select_Course_Link_2_Safe
{
  my($session_id)=@_;
  my($Buffer)="";
  
  $Buffer=$Buffer."    <center>\n";
  $Buffer=$Buffer."    <hr size=1>\n";
  $Buffer=$Buffer."   <script language=\"JavaScript\" src=\"ActionLocation\.js\">\n";
  $Buffer=$Buffer."    </script>\n";
  $Buffer=$Buffer."    <form action=\"\" name=\"MainMenuForm\" method=POST>\n";
  $Buffer=$Buffer."        <input type=hidden name=session_id value=\"";
  $Buffer=$Buffer. $session_id."\">\n";
  $Buffer=$Buffer."    <table border=0 size=640>\n";
  $Buffer=$Buffer."    <tr>\n";
  $Buffer=$Buffer."      <th>\n";
  $Buffer=$Buffer."        <input type=button value=\"回主選單\" onClick=\"SelectAction(0)\">\n";
  $Buffer=$Buffer."      </th>\n";
  $Buffer=$Buffer."    </tr>\n";
  $Buffer=$Buffer."    </table>\n";
  $Buffer=$Buffer."    </form>\n";
  $Buffer=$Buffer."    </center>\n";
  return($Buffer);
}
