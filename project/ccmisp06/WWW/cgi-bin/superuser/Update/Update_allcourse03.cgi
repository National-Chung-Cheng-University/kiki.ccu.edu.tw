#!/usr/local/bin/perl -w

###########################################################################################################
#####  Update_allcourse03.cgi
#####  產生選擇先修科目檔( $FileName )
#####  開課程式中, 需要選擇先修科目時, 點選 "選擇先修科目" 按鍵後, 跳出一個
#####  HTML視窗供選擇, 該HTML視窗即由執行此程式所產生. HTML視窗中因含有歷年
#####  開課資料, 故需動態產生. 
#####
#####  需要檔案: $DATA_PATH/History/Course/*
#####            $REFERENCE_PATH/Dept
#####  產生檔案: ~/WWW/cgi-bin/project/Add_Precourse_Window.html
#####  執行時機: 每學期開課前.
#####  ps.
#####    雖然已在教師名字中檢查中文跳脫碼, 但產生的Javascript檔在某些版本browser
#####    仍有問題, 疑為中文碼問題.
#####  Updates:
#####    2001/04/17 由 Generate_Teacher_Classification.pl 改寫. Nidalap :D~
#####    2009/06/06 將此程式從獨立的執行Generate_Precourse_Classification.pl，搬到一系列更新歷年開課資料功能.
#####               同時配合系所合一需求，將不開課的系所去除(透過呼叫 Find_All_Dept 的參數)  Nidalap :D~
#############################################################################################################

require "../../library/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";

print("Content-type:text/html\n\n");

print $EXPIRE_META_TAG;
print ("<BODY background=\"../../../Graph/manager.jpg\">");
print ("<CENTER><H1>更新歷年開課資料檔</H1><HR>\n");
print ("正在更新先修科目選擇網頁 Add_Precourse_Window.html,<BR>並且處理跳脫碼...<P>\n");

my($FileName) = $CGI_PATH . "project/Add_Precourse_Window.html";
#my($FileName) = "Add_Precourse_Window.html";
open(HTML,">$FileName") or die("Cannot open file $FileName.\n");

@dept = Find_All_Dept("NO_COM_DEPT");
@precourse = Read_All_History_Course();

#foreach $p (@precourse) {
#  foreach $k (keys %{$p}) {
#    print("$k -> $$p{$k}\n");
#  }
#}

print HTML qq(
  <HTML>
    <HEAD>
	  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	  <TITLE>新增先修科目視窗</TITLE>
	</HEAD>
    <! -------------------------------------------------- !>
    <! 本HTML檔是由程式產生, 非必要請勿直接修改本檔案內容 !>
    <! -------------------------------------------------- !>
);   
      

$precourse_count = Create_JS_Data_Code();
Create_JS_Code();
Create_HTML_Code();
Create_JS_Data_Code();

print qq '
   共處理 $precourse_count 筆開課資料, 完成！<P>   
  <INPUT type=button value="關閉視窗" onClick="window.close()">
';

#############################################################################
#####  Create_JS_Code()
#####  於HTML中產生Javascript程式, 包括所有Javascript所控制的行為
#############################################################################
sub Create_JS_Code
{
  print HTML qq(
      <SCRIPT language=JAVASCRIPT>
        
        // 使用者更改系所後, 應把該系所的所有歷年科目在科目欄帶出來 
        function OnChangeDept(dept, course)
        {
          course.length = 1;
          var i=0;
          var flag = 0;
          var temp;
          
          course.options[0].text	= "無";
          course.options[0].value	= "99999";
          course.options[0].selected	= true;
          while( i < Precourse.length ) {
            if( Precourse[i].Dept == dept.options[dept.selectedIndex].value ) {
              flag = 1;
              temp = "[" + Precourse[i].Id + "]" + Precourse[i].Name;
              course.options[course.length-1].value = Precourse[i].Id;
              course.options[course.length-1].text  = temp;
              if( i==2 ) {
                course.options[course.length-1].selected = true;
              }
              course.length ++;
            }
            i++;
          }
          course.length --;
        }
        
        //  選擇好系所, 科目, 分數後, AddPrecourse()把資料送回開課主視窗
        function AddPrecourse(form)
        {
          var course_string_to_select;
          var course_string_hidden;
          
          course_string_to_select = form.dept[form.dept.selectedIndex].text
                                  + ":" + form.course[form.course.selectedIndex].text
                                  + "-" + form.grade[form.grade.selectedIndex].text;
                                  
          course_string_hidden = form.dept[form.dept.selectedIndex].value
                               + ":" + form.course[form.course.selectedIndex].value
                               + ":" + form.grade[form.grade.selectedIndex].value;

          if( form.dept[form.dept.selectedIndex].value == 99999) {
            alert('請選擇先修科目再送出資料!');
          }else if(creator.document.form1.Precourse.options[0].value == 99999){
            creator.document.form1.Precourse.options[0].text = course_string_to_select;
            creator.document.form1.Precourse.options[0].value = course_string_hidden;
            creator.document.form1.Precourse.options[0].selected = true;
          }else{
            var index=creator.document.form1.Precourse.length;
            creator.document.form1.Precourse.length++;
            creator.document.form1.Precourse.options[index].text = course_string_to_select;
            creator.document.form1.Precourse.options[index].value = course_string_hidden;
            creator.document.form1.Precourse.options[index].selected=true;
          }
          
        }
        
     </SCRIPT>
  );

}
#############################################################################
#####  Create_HTML_Code()
#####  於HTML中產生要秀出來的HTML碼, 包括選擇系所, 科目, 分數之類的FORM資料
#############################################################################
sub Create_HTML_Code
{
  print HTML qq(
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <BODY background = "../../Graph/ccu-bg.jpg" onload=JSCreatePrecourse()>
      <CENTER>
        <H2>新增先修科目條件限制</H2>
      </CENTER>
        <HR>
        <FORM name=precourse_form>
          <FONT size=-1>請選擇系所:</FONT><BR>
          &nbsp&nbsp
          <SELECT name="dept" onChange="OnChangeDept(document.precourse_form.dept, document.precourse_form.course)">
            <OPTION value=99999>請選擇系所\n
  );
  foreach $dept (@dept) {
    %dept = Read_Dept($dept);
    print HTML ("<OPTION value=$dept>$dept{cname2}\n");
  }
  print HTML qq(          
          </SELECT>
          <BR>
          <FONT size=-1>請選擇先修科目:</FONT><BR>
          &nbsp&nbsp
          <SELECT name="course">
            <OPTION value=99999>無　　　　　　　　　　　　　　　
          </SELECT>
          <BR>
          <FONT size=-1>請選擇先修科目分數限制:</FONT><BR>
          &nbsp&nbsp
          <SELECT name="grade">
  );
  foreach $grade (reverse sort keys %GRADE) {
    print HTML ("<OPTION value=$grade>$GRADE{$grade}\n");
  }
  print HTML qq(          
          </SELECT>
          <BR>
          <CENTER>
          <INPUT type=button value="送出資料" onclick="AddPrecourse(this.form)">
        </FORM>
        <FONT size=-1>
          1. 使用說明: 請先選擇系所後, 再選擇先修科目及分數限制,
          最後點選送出資料, 系統會將您所選擇的資料帶到開課主視窗.<BR>
          2. 若出現錯誤訊息, 請關掉本視窗後, 再在開課主視窗中點選"選擇先修科目".
             
      </CENTER>
    <BODY>
  );
}
#############################################################################
#####  Create_JS_Data_Code()
#####  於HTML中產生Javascript程式所需資料, 主要是各歷年科目物件初始化的JS碼.
#############################################################################
sub Create_JS_Data_Code
{
  print HTML qq(
    <SCRIPT language=JAVASCRIPT>
      function JSPrecourse()
      {
        this.Id = "";
        this.Dept = "";
        this.Name = "";
        return(this);
      }
      Precourse = new Array();
      
      function JSCreatePrecourse()
      {
  );
  
  my $precourse_count = @precourse;
  
#  print("$precourse_count\n");
  for($i=0; $i < $precourse_count; $i++) {
    print HTML qq(    
        Precourse[$i] = new JSPrecourse();
        Precourse[$i].Id   = "$precourse[$i]{id}";
        Precourse[$i].Dept = "$precourse[$i]{dept}";
        Precourse[$i].Name = "$precourse[$i]{cname}";
    );
  }
    
  print HTML qq(
    }
    </SCRIPT>
  );
  return($precourse_count);
}
