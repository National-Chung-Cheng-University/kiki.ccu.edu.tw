#!/usr/local/bin/perl -w

###################################################################################################################
#####  Select_Class_Control02.cgi
#####  學生選課時程設定 (step 3/3)
#####  設定該年級若干係所的學生加退選權限，並顯示於畫面
#####  Updates:
#####    199?/??/??  Created
#####    2009/09/08  為避免管理者疏忽，在此頁的年級欄上方顯示該年級可選課的系所數量  Nidalap :D~ 


####    require these .pm modual    ####
require "../../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Dept.pm";
########################################

######### Main Program Here #########
%Input=User_Input();

@SDept=split(/\*:::\*/,$Input{dept});

if($Input{grade} <= 4){
  @Dept=Find_College_Dept();
}else{
  @Dept=Find_Graduate_Dept();
}

#
#  Check Password
#

WRITE_MAP();
$DATA=VIEW_MAP_RESULT();
CREAT_HTML($DATA);

#######################################
sub CREAT_HTML
{
my($Data)=@_;
print << "End_of_HTML"
Content-type: text/html


<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title> 學生選課時程 </title>

</head>

<body bgcolor=white text=#666666>
<center>
<font size=5 color=#777777> 學生選課時程設定結果</font>
$Input{dept}<br>
<hr size=1>
$Data
<hr size=1>
</center>
</body>
</html>
End_of_HTML

}

sub VIEW_MAP_RESULT
{
#   my(@Dept)=Find_All_Dept();
    my($FileName)=$REFERENCE_PATH."SelectTimeMap/".$Input{grade}.".map";

    open(FILE,"<$FileName");
    @temp=<FILE>;

      foreach $item(@temp){
        my($dept, $state)=split(/\s+/,$item);
        $Old_Time{$dept}=$state;
      }

    my($DATA)="";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$Dept0)="";

    $DATA = $DATA . "<table width=800 border=0>\n";
    $DATA = $DATA . "   <tr><th bgcolor=#99ffff width=135>工學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>管理學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>社會科學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>文學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>法學院</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>通識中心</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=135>共同科</th></tr>\n";

    $Dept0=$Dept0."<font color=red size=2>".$Old_Time{I000}."</font>";
    $Dept0=$Dept0."<font size=2>"."共同科</font><br>\n";

    foreach $dept(@Dept){
        %Dept=Read_Dept($dept);
        if($Dept{id} != "I000"){
          if($Dept{id}/1000 >= 7){
        $Dept7=$Dept7."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept7=$Dept7."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 6){
        $Dept6=$Dept6."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept6=$Dept6."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 5){
        $Dept5=$Dept5."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept5=$Dept5."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 4){
        $Dept4=$Dept4."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept4=$Dept4."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 3){
        $Dept3=$Dept3."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept3=$Dept3."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 2){
        $Dept2=$Dept2."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept2=$Dept2."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
          elsif($Dept{id}/1000 >= 1){
        $Dept1=$Dept1."<font color=red size=2>".$Old_Time{$dept}."</font>";
        $Dept1=$Dept1."<font size=2>".$Dept{cname2}."</font><br>\n";
          }
        }
    }

    $DATA = $DATA ."<tr>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept4."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept2."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept5."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept3."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept1."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept6."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept7."</td>\n";
    $DATA = $DATA ."    <td valign=top>".$Dept0."</td>\n";
    $DATA = $DATA ."</tr>\n";
    $DATA = $DATA . "   </table>\n";

    return($DATA);
}

sub WRITE_MAP
{


#   my(@Dept)=Find_All_Dept();
#   my(@SDept)=split(/\*:::\*/,$Input{dept});
#   my($FileName)=$REFERENCE_PATH."Select_Time.map";

    my($FileName)=$REFERENCE_PATH."SelectTimeMap/".$Input{grade}.".map";

    if(-e $FileName){
      open(FILE,"<$FileName");
      @Orignal=<FILE>;
      foreach $item(@Orignal){
        my($dept, $state)=split(/\s+/,$item);
        $Old_Time{$dept}=$state;
      }
    }else{
      open(FILE,">$FileName");
      foreach $dept(@Dept){
        $Old_Time{$dept}=0;
        print FILE << "End_of_Print_to_File"
$dept \t 0
End_of_Print_to_File
      }
      close(FILE);
    }

    open(FILE,">$FileName")
                        or die("Cannot open file $FileName!\n");
    foreach $dept(@Dept){
      if(not defined $Input{$dept}){
        print FILE << "End_of_Print_to_File"
$dept \t $Old_Time{$dept}
End_of_Print_to_File
      }else{
        print FILE << "End_of_Print_to_File"
$dept \t $Input{TimeClass}
End_of_Print_to_File
      }
    }
}
################################################

