#!/usr/local/bin/perl
###############################################################################
#####  Add_Course_00.cgi
#####  加選功能 -- 選擇科目的系所年級
#####  動態列出四個年級和所有系所供選擇
#####  Coder   : Nidalap :D~
#####  Modified: May 23, 2002
##### 	2008/06/03 增加跨領域學程開課連結
#####	2010/03/10 選擇通識時，「年級」選項會變成「領域」  Nidalap :D~
#####   2011/07/29 僅供查詢期間可執行此網頁.  Nidalap :D~
#####   2013/07/24 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~
#####   2013/12/06 因應通識改制，新增通識「向度」選項，以取代原有領域。  Nidalap :D~
#####	2016/06/13 專班系統預設只顯示一年級選項（不等 javascrip 驅動）。  Nidalap :D~

#$| = 1;
print("Content-type:text/html\n\n");
print("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>");
#$| = 0;

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
#require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."System_Settings.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Session.pm";
require $LIBRARY_PATH."English.pm";

#print("Content-type:text/html\n\n");
%Input = User_Input();
#%txt = Init_Text_Values();

Read_GRO();
($Input{id}, $Input{password}, $login_time, $ip) = Read_Session($Input{session_id}, 1, 1);

$online_help = Online_Help();

my(%Student,%Dept);

#%Input=User_Input();
%Student=Read_Student($Input{id});
#print("dept = $Student{dept}<BR>\n");
%Dept=Read_Dept($Student{dept});
%system_flags = Read_System_Settings();
%system_settings = %system_flags;

($cate_ref, $subcate_ref) = Get_CGE_Categories();
%category = %{$cate_ref};
%subcategory = %{$subcate_ref};
$use_cge_new_cate = Student_Suit_CGE_New_Category($Student{'id'});		###  判別學生是否適用 103 學年度後的通識「向度」

%txt = Init_Text_Values();

Check_Student_Password($Input{id}, $Input{password});

########    若不開放查詢，則顯示不可進入  #########
#if($SUPERUSER != 1){     ## 非 superuser 的使用者
#  if( Whats_Sys_State() == 0  ){
#    Enter_Menu_Sys_State_Forbidden($HEAD_DATA);
#  }
#}

if( $IS_ENGLISH ) {
  $HEAD_DATA = Head_of_Individual($Student{ename},$Student{id},$Dept{ename},$Student{grade},$Student{class});
}else{
  $HEAD_DATA = Head_of_Individual($Student{name},$Student{id},$Dept{cname},$Student{grade},$Student{class});
}
if( !$IS_MOBILE ) {
  print "
    <html>
    $online_help
    <head>
      <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
      <META HTTP-EQUIV='CACHE-CONTROL' CONTENT='NO-CACHE'>
      <TITLE>" . $txt{'html_title'} . "</TITLE>
    </head>
    <body background='" . $GRAPH_URL . "./ccu-sbg.jpg'>
    <center>
      $HEAD_DATA
      <hr>
  ";
}

#####  依系統設定, 檢查該生是否在停權黑名單中, 以及是否在停權期間 2009/02/25 Nidalap :D~
#####  即使關閉此功能, 系統仍會紀錄 log, 差別在於是否顯示警訊和是否給加退選.
if( $system_settings{black_list} == 1 ) {   		       ### 如果開啟黑名單功能
  $ban_time = Read_Ban_Record($Student{id}, $BAN_COUNT_LIMIT); ### 停權尚須多久恢復(大於0就是停權中)
  if($ban_time > 0) {
    Show_Ban_Message($ban_time, 1);
  }
}

##### 檢核是否需要先確認畢業資格審查表. 若必須確認卻尚未確認, 則不給選課
##### 2005/09/07 Nidalap :D~
if( Verify_For_Graduate_pdf($Student{id}, $Student{grade}) == 2 ) {
  if( not if_Confirmed_For_Graduate_pdf($Student{id}) ) {
    print("<P>請先確認您的畢業資格審查表, 再進行加退選!<BR>");
    my($LINK)=Select_Course_Link($Input{id},$Input{password});
    print("$LINK");

    exit();
  }
}

if( $IS_MOBILE ) {			###  顯示行動化介面
  $mobile_temp = Create_jQuery_Mobile_Script();
  print qq(
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	  $mobile_temp
      <TITLE>加選 - 選擇系所年級($Student{name})</TITLE>
    </head>
  );
  print Show_M_Javascript();
  print Create_jQuery_Mobile_Title_Tag();
  
  #print "<HR><CENTER><DIV id='debug_div'>debug</DIV></CENTER><HR>";
  
  print Show_M_Form_Start();
  print Show_M_College_Sel();
  print Show_M_Dept_Sel();
  print Show_M_Grade_Sel();
  print Show_M_Form_End();
  print Create_jQuery_Mobile_Footer_Tag($Student{name});
  exit();
}else{						###  顯示電腦版介面
  my($DATA)=DEPT_TABLE();
  SELECT_MENU($HEAD_DATA,$Student{id},$Student{password},$DATA);
}

####################################################################################################
sub Show_M_Form_Start
{
  my $html = qq|
    <form action="Add_Course01.cgi" method="GET" id=form1 data-ajax="false">
    <input type=hidden name="session_id" value="$Input{session_id}">
	<input type=hidden name="use_cge_new_cate" id="use_cge_new_cate" value="$use_cge_new_cate">
    <input type=hidden name="m" value=1>
  |;
  return $html;
}
####################################################################################################
sub Show_M_Form_End
{
  my $html = qq|
    <INPUT type='submit' value="檢視科目列表">
    </FORM>
  |;
  return $html;
}
####################################################################################################
sub Show_M_Grade_Sel
{
  my $html;
  
  my @grade = (1..4);
  
  $html = "<SPAN id='m_grade_caption'>年級</SPAN>：<SELECT data-role=select name='grade' id='m_grade_sel'>";
  foreach $grade (sort @grade) {
    $html .= "<OPTION value='$grade'>$grade	\n";
  }
  $html .= "</SELECT><P>\n";
  return $html;

}
####################################################################################################
#####  行動化介面的 Javascript
sub Show_M_Javascript
{
  my $m_javascript_dept_obj = Show_M_Javascript_Dept_Obj();
  my $html = "";
  #$html = qq|<SCRIPT type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>|;
  $html .= qq|
    <SCRIPT language="javascript">
	  $m_javascript_dept_obj
	  \$(document).ready(function(){
	    /////  若學院選項改變了，則學系選項變為該學院下所有學系
		\$("#m_college_sel").change(function(){
		  var college_sel = \$("#m_college_sel").val();
		  \$sel = \$('#m_dept_sel');
		  \$sel.empty();
	  
		  \$.each(AllDept, function(deptid, dept) {
			if( dept.college == college_sel ) {
		      \$sel.append('<option value="' + deptid + '">' + dept.abbrev + '</option>');
//			  \$('#debug_div').html(dept.abbrev);
//			  \$sel.html(dept.abbrev);
//			  \$sel.append('<option value="0">Add new location...</option>');
//			  \$sel.append(\$('<option>', {value: 'deptid', text : dept.abbrev }));
//			  \$sel.append(\$("<option></option>").attr("value", deptid).text(dept.abbrev));
			}
		  });
		  \$sel.selectmenu("refresh", true);
		});
		/////  若學系選項改變了，則年級依大學部、研究所、通識課程、跨領域學程等條件調整/
		\$("#m_dept_sel").change(function(){
		  var dept = \$("#m_dept_sel").val();
		  if( dept == "I001" ) {
		    //alert(dept);
			var use_cge_new_cate = \$('#use_cge_new_cate').val();
			if( use_cge_new_cate == 1 ) {
			  var grade_options = [
			    "基礎通識 - 中國語文知識與應用", "基礎通識 - 英文能力訓練",
			    "基礎通識 - 資訊能力課程","基礎通識 - 基礎概論課程",
				"博雅通識 - 跨向度課程「中正講座」", "博雅通識 - 藝術與美學", 
				"博雅通識 - 能源、環境與生態", "博雅通識 - 人文思維與生命探索", 
				"博雅通識 - 公民與社會參與", "博雅通識 - 經濟與國際脈動", 
				"博雅通識 - 自然科學與技術"];
			  m_grade_caption
			}else{
			  var grade_options = ["第一領域","第二、五領域","第三領域","第四領域"];
			}
		  }else if( dept.length == 2 ) {
		    //alert("2");
			var grade_options = ["不適用"];
		  }else if( dept.substring(3) == 6 ) {
		    //alert("6");
			var grade_options = [1,2];
		  }else{
		    //alert("4");
			var grade_options = [1,2,3,4];
		  }
		  \$sel = \$('#m_grade_sel');
		  \$sel.empty();
		  \$.each(grade_options, function(i, grade) {
			\$sel.append(\$("<option></option>")
				 .attr("value", i+1).text(grade));
		  })
		  \$sel.selectmenu("refresh", true);
		})
		
	  });
	</SCRIPT>
  |;
  return $html;
}
####################################################################################################
sub Show_M_Javascript_Dept_Obj
{
  my $js;
  @Dept=Find_All_Dept("NO_COM_DEPT");
    
  foreach $gro_name (keys %gro_name) {                                ###  將跨領域學程視為系所
    if( $gro_name{$gro_name}{gro_name} ne "" ) {
	  push(@Dept, $gro_name);
    }
  }
  
  $js = "var AllDept = { ";
  foreach $dept (@Dept){
    next if($dept eq "");
    if( length($dept) == 2 ) {              ###  跨領域學程代碼是兩碼
      %Dept=("id"=>"$dept", "cname2"=>"$gro_name{$dept}{gro_name}", "college"=>"J");
    }else{                                  ###  一般系所代碼是四碼
      %Dept=Read_Dept($dept);
    }

    if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {    ###  專班系統不列出大學部
      next  if($dept =~ /4$/);
	  next  if(length($dept) == 2);
    }
    if( length($dept) == 2 ) {				###  if 跨領域學程
      $gro_link = $CLASS_URL . "Show_All_GRO.cgi?gro_no=" . $dept;
	  #$Dept8 .= "<A href=$gro_link>$gro_name{$dept}{gro_name}</A><br>\n";
	}
    $js .= "'$dept' : { 'college':'$Dept{college}', 'abbrev':'$Dept{cname2}'},\n";
  }
  $js .= "};";
  
  return $js;
}

####################################################################################################
sub Show_M_College_Sel
{
  my %col = ("1"=>"文學院", "2"=>"理學院", "3"=>"社會科學院", "4"=>"工學院", 
             "5"=>"管理學院", "6"=>"法學院", "7"=>"教育學院", "I"=>"其他", "J"=>"跨領域學程");
  my $html;
  $html = "學院：<SELECT data-role=select name='college' id='m_college_sel'>";
  foreach $col (sort keys %col) {
    $html .= "<OPTION value='$col'>$col{$col}	\n";
  }
  $html .= "</SELECT><P>\n";
  return $html;

}
####################################################################################################
sub Show_M_Dept_Sel
{
  my $html;
  $html = "系所：<SELECT data-role=select name='dept' id='m_dept_sel'>";
  my(@Dept)=Find_All_Dept("NO_COM_DEPT");
    
  foreach $gro_name (keys %gro_name) {                                ###  將跨領域學程視為系所
    if( $gro_name{$gro_name}{gro_name} ne "" ) {
      push(@Dept, $gro_name);
    }
  }
  
  foreach $dept (sort @Dept){
    next if($dept eq "");
    if( length($dept) == 2 ) {              ###  跨領域學程代碼是兩碼
      %Dept=("id"=>"$dept", "cname2"=>"$gro_name{$dept}{gro_name}", "college"=>"J");
    }else{                                  ###  一般系所代碼是四碼
      %Dept=Read_Dept($dept);
    }

    if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {    ###  專班系統不列出大學部
      next  if($dept =~ /4$/);
	  next  if(length($dept) == 2);
    }
    if( length($dept) == 2 ) {				###  if 跨領域學程
      $gro_link = $CLASS_URL . "Show_All_GRO.cgi?gro_no=" . $dept;
	  #$Dept8 .= "<A href=$gro_link>$gro_name{$dept}{gro_name}</A><br>\n";
	}
    #print "$dept -> $Dept{$dept}<BR>\n";
	
	###  記得拿回來！
    $html .= "<OPTION value='$dept'>$Dept{cname2}	\n";
	
	
  }
  $html .= "</SELECT><P>\n";
  return $html;

}
####################################################################################################
sub SELECT_MENU
{
my($HEAD_DATA,$id,$password,$DATA)=@_;
$show_help = Show_Online_Help('ADD_COURSE_GRADE');

print qq|
    <SCRIPT type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
    <SCRIPT language="javascript">
	  \$(document).ready(function(){
		\$("#grade_cge").hide();
		\$("#grade_cge_new").hide();
		\$(".cge_subcate").hide();
		\$("#grade_na").hide();

	    var deptcd = \$("input[name=dept]:checked").val();
		//alert(deptcd);
		if( deptcd == "I001" ) {					///  如果系所預設是通識（只會發生在使用者BACK）
		  //\$("input[name=dept]").trigger("click");
		  var use_cge_new_cate = \$('#use_cge_new_cate').val();
		  if( use_cge_new_cate == 0 ) {				///  102學年度前(含)舊生使用通識五領域的選項
			//alert("ccc");
			\$("#grade_normal").hide();
			\$("#grade_cge").show();
			\$("#grade_cge_new").hide();
		  }else{									///  103學年度後(含)新生使用通識多個向度選項
		    //alert("ddd");
		    \$("#grade_normal").hide();
		    \$("#grade_cge").hide();
			\$("#grade_cge_new").show();
			//alert("eee");
		  }
		}
	
		
		//////  依照選通識與否，判斷該顯示「年級」還是「領域」
		\$("input[name=dept]").click(function(){
			//alert(\$(this).val());
			var use_cge_new_cate = \$('#use_cge_new_cate').val();
			//alert(use_cge_new_cate);
			
			if(\$(this).val()=="I001"){					///  如果點了通識課程, 顯示第一~第五領域
			  if( use_cge_new_cate == 0 ) {				///  102學年度前(含)舊生使用通識五領域的選項
			    \$("#grade_normal").hide();
			    \$("#grade_cge").show();
				\$("#grade_cge_new").hide();
			  }else{									///  103學年度後(含)新生使用通識多個向度選項
			    \$("#grade_normal").hide();
			    \$("#grade_cge").hide();
				\$("#grade_cge_new").show();
			  }
			}else{										///  如果點了一般系所, 顯示一~四年級
			  \$("#grade_normal").show();
			  \$("#grade_cge").hide();
			  \$("#grade_cge_new").hide();
			}
			var dept_type = check_dept_type(\$(this).val());
			//alert(dept_type);
			if( dept_type == 2 ) {					    ///  若選擇碩士班，則只可選擇一年級
			  \$("#grade_normal234").hide();
			  \$("#g11").attr("checked", true);
			}else{										///  若選擇一般系所，可選 1~4 年級
			  \$("#grade_normal234").show();
			}
            if( dept_type == 3) {						///  若選擇跨領域學程，則無年級選項
			  \$("#grade_na").show();
			  \$("#grade_normal").hide();
			  \$("#grade_cge").hide();
			  \$("#grade_cge_new").hide();
			}else{
			  \$("#grade_na").hide();
			}		
		})
		\$(".cge_cate").click(function(){
		  var cate = \$(this).val();
		  //alert(cate);
		  \$(".cge_subcate").hide();
		  \$("#cge_subcate" + cate).show();
		});

		//////  設定 1~4 年級與 1~4 領域的選項 checked 關聯(這樣寫很笨我知道)
		\$("#g11").click(function() { \$("#g21").attr("checked", true); })
		\$("#g12").click(function() { \$("#g22").attr("checked", true); })
		\$("#g13").click(function() { \$("#g23").attr("checked", true); })
		\$("#g14").click(function() { \$("#g24").attr("checked", true); })
		\$("#g21").click(function() { \$("#g11").attr("checked", true); })
		\$("#g22").click(function() { \$("#g12").attr("checked", true); })
		\$("#g23").click(function() { \$("#g13").attr("checked", true); })
		\$("#g24").click(function() { \$("#g14").attr("checked", true); })
	  })
	  ////////////////////////////////////////////////////////////////////////////////////////
      /////  判斷系所類別
	  function check_dept_type(id) 
	  {
	    var len = id.length;
//		alert("hehe");
		
		if( len == 2 )  return 3; 						///  跨領域學程
	    var a = id.substring(0,1);
		var b = id.substring(3);
        aa = Number(a);
		bb = Number(b);
        if( (a>=1) && (aa<=7) && (bb==6) )  {			///  碩士班
		  return 2;
		}else{											///  學士班
		  return 1;
		}
	  }

	</SCRIPT>
|;

if( $IS_ENGLISH ) {
  $input_e = "<input type=hidden name=e value=1>";
}else{
  $input_e = "<input type=hidden name=e value=0>";
}

$cge_cate_subcate_sel_html = Create_CGE_Category_Subcategory_Selection_HTML();

print '
	<br>
    <form action="Add_Course01.cgi" method="post" id=form1>
    <input type=hidden name="session_id" value="' . $Input{session_id} . '">
	<input type=hidden name="use_cge_new_cate" id="use_cge_new_cate" value=' . $use_cge_new_cate . '>
    <input type=hidden name="page" value=0>
	' . $input_e . '
    <table border=0 width=85%>
    <tr>
      <th bgcolor=pink> ' . $txt{'grade'} . '</th>
      <td>
	    <DIV id="grade_normal">
		  <input type=radio name=grade id=g11 value=1 checked>' . $txt{'grade1'}
	;

if( !$IS_GRA ) {						###  專班系統不顯示二三四年級  added 20160613 Nidalap :D~
  print '
 	      <SPAN id="grade_normal234">
		    <input type=radio name=grade id=g12 value=2>' . $txt{'grade2'} . '
            <input type=radio name=grade id=g13 value=3>' . $txt{'grade3'} . '
            <input type=radio name=grade id=g14 value=4>' . $txt{'grade4'} . '
		  </SPAN>
	  ';
}
print '
		</DIV>
		<DIV id="grade_cge">
		  <input type=radio name=grade2 id=g21 value=1 checked>' . $txt{'cge1'} . '
 	      <input type=radio name=grade2 id=g22 value=2>' . $txt{'cge2'} . '
          <input type=radio name=grade2 id=g23 value=3>' . $txt{'cge3'} . '
          <input type=radio name=grade2 id=g24 value=4>' . $txt{'cge4'} . '
		</DIV>
		<DIV id="grade_cge_new">' 
		  . $cge_cate_subcate_sel_html . '
		</DIV>
		<DIV id="grade_na">
		    ' . $txt{'none'} . '
		</DIV>
	  </td>
    </tr>
    <tr>
    <th bgcolor=pink>' . $txt{'dept'} . '</th>
    <td colspan=6>' . $DATA . '</td>
    </tr>
    </table>
	<INPUT type=hidden name="use_cge_new_cate" id="use_cge_new_cate" value=$use_cge_new_cate>
    <input type=submit value="' . $txt{'browse'} . '">
    </form>
</center>
</body>
</html>
'
}

sub DEPT_TABLE
{
    my(@Dept)=Find_All_Dept("NO_COM_DEPT");
    
    foreach $gro_name (keys %gro_name) {                                ###  將跨領域學程視為系所
      if( $gro_name{$gro_name}{gro_name} ne "" ) {
        push(@Dept, $gro_name);
      }
    }    

    my($DATA)="";
    my($Dept1,$Dept2,$Dept3,$Dept4,$Dept5,$Dept6,$Dept7,$DeptI)="";

    $DATA = $DATA . "<table width=100% border=0>\n";
    $DATA = $DATA . "	<tr><th bgcolor=#99ffff width=10%>" . $txt{'col1'} . "</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col2'} . "</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col3'} . "</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col4'} . "</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col5'} . "</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col6'} . "</th>\n";  
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col7'} . "</th>\n";
    $DATA = $DATA . "       <th bgcolor=#99ffff width=10%>" . $txt{'col8'} . "</th>\n";        
    if( ($SUB_SYSTEM!=3) and ($SUB_SYSTEM!=4) ) {
      $DATA = $DATA . "       <th bgcolor=#99ffff width=15%>" . $txt{'col9'} . "</th>\n";   ### 專班不列出
    }
    $DATA = $DATA . "   </tr>\n";
            

    foreach $dept(@Dept){
	  next if($dept eq "7176");					###  違章建築：移除 7176 教育學研究所教育學碩士班  20150626
      if( length($dept) == 2 ) {              ###  跨領域學程代碼是兩碼
        %Dept=("id"=>"$dept", "cname2"=>"$gro_name{$dept}{gro_name}");
      }else{                                  ###  一般系所代碼是四碼
        %Dept=Read_Dept($dept);
      }
	  
	  if( $Student{dept} eq $dept ) {
	    $Dept{cname2} = "<SPAN style='background:YELLOW; color:RED'>" . $Dept{cname2} . "</SPAN>";
		$dept_selected = " CHECKED ";
	  }else{
	    $dept_selected = "";
	  }

      if( ($SUB_SYSTEM==3) or ($SUB_SYSTEM==4) ) {    ###  專班系統不列出大學部
        next  if($dept =~ /4$/);
		next  if(length($dept) == 2);
      }
      #####  第一階段選課時, 數學系所開設之課程採先選先贏額滿為止制, 系統採不同天選課因應之
      if( $system_flags{allow_select_math} == 1 ) {     ###  只開放非數學系課程
        next if( is_Math_Dept($Dept{id}) );
      }elsif( $system_flags{allow_select_math} == 2 ) { ###  只開放數學系課程
        next if( not is_Math_Dept($Dept{id}) );
      }

      if( length($dept) == 2 ) {				###  if 跨領域學程
        $gro_link = $CLASS_URL . "Show_All_GRO.cgi?gro_no=" . $dept;
#        $Dept8 .= "<A href=$gro_link>$gro_name{$dept}{gro_name}</A><br>\n";
  	$Dept8 .= "<input type=radio name=dept value=\"".$Dept{id}."\">";
	$Dept8 .= $Dept{cname2}."<BR>\n"
      }else{							##  else 一般系所
	    if( $IS_ENGLISH ) {
		  $dept_show = "<SPAN title='" . $Dept{ename} . "'>$Dept{ename}</SPAN>";
		}else{
		  $dept_show = "<SPAN title='" . $Dept{cname} . "'>$Dept{cname2}</SPAN>";
		}
        if    ($Dept{college} eq "I") {
          $DeptI=$DeptI."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $DeptI=$DeptI.$dept_show."<BR>\n";
        }elsif($Dept{college} eq "7") {
          $Dept7=$Dept7."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept7=$Dept7.$dept_show."<br>\n";
        }elsif($Dept{college} eq "6") {
          $Dept6=$Dept6."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept6=$Dept6.$dept_show."<br>\n";
        }elsif($Dept{college} eq "5"){
          $Dept5=$Dept5."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept5=$Dept5.$dept_show."<br>\n";
        }elsif($Dept{college} eq "4"){
          $Dept4=$Dept4."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept4=$Dept4.$dept_show."<br>\n";
        }elsif($Dept{college} eq "3"){
          $Dept3=$Dept3."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept3=$Dept3.$dept_show."<br>\n";
        }elsif($Dept{college} eq "2"){
          $Dept2=$Dept2."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept2=$Dept2.$dept_show."<br>\n";
        }elsif($Dept{college} eq "1"){
          $Dept1=$Dept1."<input type=radio name='dept' value='".$Dept{id}."'  $dept_selected>";
          $Dept1=$Dept1.$dept_show."<br>\n";
        }
      }
    }

    $DATA = $DATA ."<tr>\n";
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept1."</td>\n";		# 文
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept2."</td>\n";		# 理
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept3."</td>\n";		# 社
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept4."</td>\n";		# 工
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept5."</td>\n";		# 管
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept6."</td>\n"; 	# 法
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept7."</td>\n"; 	# 教
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$DeptI."</td>\n";		# 其他
    $DATA = $DATA ."    <td valign=top><FONT size=2>".$Dept8."</td>\n";         # 跨領域學程
    $DATA = $DATA ."</tr>\n";
    $DATA = $DATA . "   </table>\n";

    return($DATA);
}
##################################################################################
sub Create_CGE_Category_Subcategory_Selection_HTML
{
  my $html;

  my $display_type;
  #$display_type = 1;	### SELECT 選擇方式
  $display_type = 2;	### RADIO BUTTON 選擇方式
  
  $html = "\n";
  
  foreach $cate (sort keys %category) {
    $html .= "<INPUT type=radio name=cge_cate class=cge_cate 
					 id=cge_cate" . $cate . " value=" . $cate . ">" . $txt{'cge_new' . $cate} . "\n";
  }

  $html .= "<BR>\n";
  foreach $cate (sort keys %subcategory ) {
	if( $display_type == 1 ) {
	  $html .= "<SELECT name='cge_subcate" . $cate . "' id='cge_subcate" . $cate . "' class='cge_subcate'>\n";
      foreach $subcate (sort keys %{$subcategory{$cate}}) {
        $cate_subcate = $cate . "_" . $subcate;
        $html .= "<OPTION value=$cate_subcate>$subcate. " . $txt{'cge_subcate'.$cate_subcate} . "\n";
      }
	  $html .= "</SELECT>\n";
	}else{
	  $html .= "<SPAN class=cge_subcate id=cge_subcate" . $cate . ">\n";
      foreach $subcate (sort keys %{$subcategory{$cate}}) {
	    $cate_subcate = $cate . "_" . $subcate;
	    $html .= "<INPUT type=radio  name=cge_subcate value=" . $subcate . ">" 
			  . $subcate . ". " . $txt{'cge_subcate'.$cate_subcate} . "\n";
		if( ($cate == 2) and ($subcate == 3) ) {			###  換行
		  $html .= "<BR>";
		}
      }
	  $html .= "</SPAN>\n";
	}
  }
  
  return $html;
}
##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/24
sub Init_Text_Values
{
  my %txtall;
  
  %txtall = (
    'html_title'=> {'c'=>'加選分類表', 'e'=>'Please select department & grade'},
	'grade'		=> {'c'=>'年級', 'e'=>'Year Standing'},
	'class'		=> {'c'=>'班別', 'e'=>'Class'},
	'dept'		=> {'c'=>'系所', 'e'=>'Department'},
	'grade1'	=> {'c'=>'一年級', 'e'=>'1'},
	'grade2'	=> {'c'=>'二年級', 'e'=>'2'},
	'grade3'	=> {'c'=>'三年級', 'e'=>'3'},
	'grade4'	=> {'c'=>'四年級', 'e'=>'4'},
	'cge1'		=> {'c'=>'第一領域', 'e'=>'First (General Education Course) Module'},
	'cge2'		=> {'c'=>'第二、五領域', 'e'=>'Second and Fifth Module'},
	'cge3'		=> {'c'=>'第三領域', 'e'=>'Third Module'},
	'cge4'		=> {'c'=>'第四領域', 'e'=>'Fourth Module'},
	'browse'	=> {'c'=>'察看該系所開課資料', 'e'=>'Browse Course List'},
	
	'cname'		=> {'c'=>'科目名稱與代碼', 'e'=>'Course Title & ID'},
	'teacher'	=> {'c'=>'授課教師', 'e'=>'Instructor'},
	'credit'	=> {'c'=>'學分', 'e'=>'Credit'},
    'property'	=> {'c'=>'學分歸屬', 'e'=>'Credit Type'},
    'weekday'	=> {'c'=>'星期節次', 'e'=>'Day/Period'},
    'classroom'	=> {'c'=>'教室', 'e'=>'Class Location'},
	'none'		=> {'c' =>'(無選項)', 'e'=>'(none)'},
	
	'nodel'		=> {'c'=>'請勿退選本科目！若退選後，將無法加選，需填寫加簽單，並完成加簽程序後方可選課。', 
	                'e'=>'請勿退選本科目！若退選後，將無法加選，需填寫加簽單，並完成加簽程序後方可選課。'},
	'del_button'=> {'c'=>'確定刪除標記中科目', 'e'=>'Delete all courses with selection marks'},
	'tea_undefined'	=> {'c'=>'教師未定', 'e'=>'教師未定'},
	'col1'		=> {'c'=>'文學院', 'e'=>'College of Humanities'},
	'col2'		=> {'c'=>'理學院', 'e'=>'College of Sciences'},
	'col3'		=> {'c'=>'社會科學院', 'e'=>'College of Social Sciences'},
	'col4'		=> {'c'=>'工學院', 'e'=>'College of Engineering'},
	'col5'		=> {'c'=>'管理學院', 'e'=>'College of Management'},
	'col6'		=> {'c'=>'法律學院', 'e'=>'College of Law'},
	'col7'		=> {'c'=>'教育學院', 'e'=>'College of Education'},
	'col8'		=> {'c'=>'其他', 'e'=>'Others'},
	'col9'		=> {'c'=>'跨領域學程', 'e'=>'Interdisciplinary'},
	'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
	'mark'		=> {'c'=>'標記', 'e'=>'Mark'},
  );

  #####  處理通識向度的中英文資料
  foreach $cate (keys %category) {
    #print ("$cate : " . $category{$cate}{'cname'} . "<BR>\n");
	$txtall{'cge_new'.$cate} = {'c'=>$category{$cate}{'cname'}, 'e'=>$category{$cate}{'ename'}};
  }
  foreach $cate (keys %subcategory) {
    foreach $subcate (keys %{$subcategory{$cate}} ) {
	  #print ("$cate : $subcate : " . $subcategory{$cate}{$subcate}{'cname'} . "<BR>\n");
	  $txtall{'cge_subcate'.$cate.'_'.$subcate} = {'c'=>$subcategory{$cate}{$subcate}{'cname'}, 
												   'e'=>$subcategory{$cate}{$subcate}{'ename'}};
	}
  }
    
  foreach $k (keys %txtall) {
	if( $IS_ENGLISH ) {
	  $txt{$k} = $txtall{$k}{'e'};
	}else{
	  $txt{$k} = $txtall{$k}{'c'};
	  #print "$k -> " . $txt{$k} . "<BR>\n";
	}
  }
  
  return %txt;  
}
