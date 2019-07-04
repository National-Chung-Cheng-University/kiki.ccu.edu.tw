#!/usr/local/bin/perl -w

#############################################################################
#####  Update_teacher03.cgi
#####  產生選擇教師 javascript 檔 $FileName, 供開課時選擇用
#####    1. 由人事系統upload新的教師檔後, 要在開排課系統上選到新的老師, 
#####       必需先跑過這個程式, 更新最新的( $FileName )檔, 開課系統上方能選擇.
#####    2. 另外如果有新系所, 也要另跑過ClassifyDept.pl並把產生 的html code加到
#####       AddTeacherWindow.html內.
#####  Updates:
#####    199?       Coder: Ionic, Hanchu(199?)
#####    2000/02/15 進一步處理跳脫字元, 減少事後需手動更改檔案的問題 Nidalap)
#####    2009/02/05 從 Generate_Teachers_Classification.pl 修改成為透過網頁執行.(Nidalap)
#############################################################################

$| = 1;
require "../../library/Reference.pm";
require $LIBRARY_PATH."Teacher.pm";

print("Content-type:text/html\n\n");
print $EXPIRE_META_TAG;
print ("<BODY background=\"../../../Graph/manager.jpg\">");
print ("<CENTER><H1>更新教師資料檔</H1><HR>\n");
print ("正在更新開課選擇教師資料網頁 Teacher.js, 並且處理跳脫碼...<P>\n");

#$source = $REFERENCE_PATH . "teacher_temp.txt";
my($FileName)=$CGI_PATH . "project/Teachers.js";

open(TEACHERCLASS,">$FileName") or 
             die("Cannot open file $FileName.\n");

####    print 的用法中，使用 ' 的單引號，可以忽略標籤之中的一些特殊字元
####    因為不會將這些特殊字元當成變數的開頭來使用，因此可以安心使用列印
####    的功能。

print TEACHERCLASS << 'EndOfTeacherDef';
function JSTeacher()
{
	this.Dept="";
	this.Code="";
	this.Name="";
	return(this);
}

EndOfTeacherDef

@Teachers=Read_Teacher_File();
$num_of_teachers=@Teachers;

#########################################################################

my($Data_Stream)="";
my($Count)=1;

foreach $Teacher(sort { $Teacher_Name{$a} cmp $Teacher_Name{$b} } @Teachers)
{
 $Data_Stream=$Data_Stream."\tTeachers[$Count]=new JSTeacher();\n";
 $Data_Stream=$Data_Stream."\tTeachers[$Count]."."Code=";
 $Data_Stream=$Data_Stream."\"".$Teacher."\"".";\t";
 $Data_Stream=$Data_Stream."Teachers[$Count]."."Dept=";
 $Data_Stream=$Data_Stream."\"".$Teacher_Dept{$Teacher}."\"";
 $Data_Stream=$Data_Stream.";\t";
 $Data_Stream=$Data_Stream."Teachers[$Count]."."Name=";

  #@exception_words = ('珮\\\', '功\\\');
  
  $exception_flag = 0;
#  if($Teacher_Name{$Teacher} =~ /\\/g) {
#    foreach $word (@exception_words) {			### 這些字都不應該加上 escape 碼, 否則 js 執行會有錯.
#      if( $Teacher_Name{$Teacher} =~ /$word/ ) {
#        $exception_flag = 1;
#      }
#    }
#    if( $exception_flag != 1 ) {
#      $Teacher_Name{$Teacher} =~ s/\\/\\\\/;
#      $escape++;
##      print("找到中文跳脫碼並修正: $Teacher_Name{$Teacher}<BR>\n");
#    }else{
#      $ignore++;
##      print("找到中文跳脫碼但略過: * $Teacher_Name{$Teacher}<BR>\n");
#    }
##    $Teacher_Name{$Teacher} = "(temp)";
#  }

 $Data_Stream=$Data_Stream."\"".$Teacher_Name{$Teacher}."\"";
# $Data_Stream=$Data_Stream."\'".$Teacher.$Teacher_Name{$Teacher}."\'";
 $Data_Stream=$Data_Stream.";\n";
 $Count++;
}

print TEACHERCLASS << "EndOfTeachers";
Teachers=new Array();

function JSCreatAllTeachers()
{
$Data_Stream
}

EndOfTeachers

open(FIRSTDEPT,">./FirstDept.txt");
foreach $Teacher(@Teachers)
{
	if($Teacher_Dept{$Teacher} eq "1104"){
		print FIRSTDEPT "<Option value=".$Teacher.">";
		print FIRSTDEPT $Teacher_Name{$Teacher}."\n";
	}

}

print qq [
   找到中文跳脫碼並修正: $escape 筆資料<BR>
   找到中文跳脫碼但略過: $ignore 筆資料<P>
   
   完成!<P>
   
  <INPUT type=button value="關閉視窗" onClick="window.close()">
];