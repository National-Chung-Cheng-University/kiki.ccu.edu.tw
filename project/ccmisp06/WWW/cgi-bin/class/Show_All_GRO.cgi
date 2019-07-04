#!/usr/local/bin/perl

###################################################################################################
#####  Show_All_GRO.cgi
#####  顯示所有跨領域學程, 及特定學程的科目.
#####  若有傳入 session_id, 則顯示加選選項, 連往加選網頁.
#####  2008/05/28 Nidalap :D~
#####   2015/07/27 英文版相關增修：將顯示文字拉到 Init_Text_Values() 中設定。 Nidalap :D~

print("Content-type: text/html\n\n");

require "../library/Reference.pm";
require $LIBRARY_PATH."GetInput.pm";
require $LIBRARY_PATH."Common_Utility.pm";
require $LIBRARY_PATH."Display_Links.pm";
require $LIBRARY_PATH."Dept.pm";
require $LIBRARY_PATH."Student_Course.pm";
require $LIBRARY_PATH."Course.pm";
require $LIBRARY_PATH."Password.pm";
require $LIBRARY_PATH."English.pm";
require $LIBRARY_PATH."Select_Course.pm";
require $LIBRARY_PATH."Student.pm";
require $LIBRARY_PATH."Error_Message.pm";
require $LIBRARY_PATH."Teacher.pm";
require $LIBRARY_PATH."Classroom.pm";

########    讀取使用者輸入資料    ########
%Input=User_Input();
@dept = Find_All_Dept();
foreach $dept (@dept) {
  @course = Find_All_Course($dept);
  foreach $course (@course) {
#    print("$$course{id}  $$course{group}<BR>\n");
    $cou_dept{$$course{id}} = $dept;
#    print("$$course{id} belongs to  $dept<BR>\n");
  }
}

#$fs2 = "<FONT size=2>";

#%the_Course=Read_Course($Input{dept},$Input{course},$Input{group});
##########################################

%txt = Init_Text_Values();
Read_GRO();			###  讀入 %gro_name, @gro_dept, @gro_cour
print '
  <HTML>
    <HEAD>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <TITLE>' . $txt{'html_title'} . ' </TITLE>
      <LINK rel="stylesheet" type="text/css" href="' . $HOME_URL . '/font.css">
    </HEAD>
    <BODY background=$GRAPH_URL/ccu-sbg.jpg>
    <CENTER>
      <SPAN class="title2">' . $txt{'html_title2'} . '</SPAN>
      <HR>
    </CENTER>
    <SPAN class="font2">
    <P class="illustration">    
';

if($Input{gro_no} eq "") {
  List_All_GRO();
}else{
  Show_GRO($Input{gro_no});
}

##############################################################################################
sub Show_GRO()
{
  my($gro_no) = @_;
  my($TH, $TH2); 
  if( $Input{session_id} ne "" ) {
    $TH = "<TH>" . $txt{'add'} . "</TH>";
#    $TH2 = "<TD><A href=\"Add_Course01.cgi?session_id=$Input{session_id}?dept=$dept\">加選</A></TD>";
  }
  print  $txt{'list1'} . "
     <FONT color=RED>" . $gro_name{$gro_no}{gro_name} . "</FONT>" . $txt{'list2'} . ":<P>
    <CENTER>
    <TABLE border=1 class=font2>
      <TR bgcolor=YELLOW>$TH<TH>" . $txt{'dept'} . "</TH><TH>" . $txt{'cid'} . "</TH><TH>" . $txt{'cname'} . "</TH><TH>" . $txt{'credit'} . "</TH></TR>
  ";
  foreach $gro_cour (@gro_cour) {                             ###  相關課程
    if( $$gro_cour{gro_no} eq $gro_no )  {
      $dept = $cou_dept{$$gro_cour{cour_cd}};      
#      print("reading: $dept, $$gro_cour{cour_cd}...<BR>\n");
      %course = Read_Course($dept, $$gro_cour{cour_cd}, "01", "", "");
      %dept = Read_Dept($dept);      

      if( $Input{session_id} ne "" ) {
	    $url = "Add_Course01.cgi?session_id="  . $Input{session_id} . "&dept=" . $dept . "&grade=" . $course{grade};
		$url .= "&e=1"	if( $IS_ENGLISH );
        $TH2 = "<TD><A href='$url'>" . $txt{'add'} . "</A></TD>";
      }

      if( $course{dept} ne "" ) {     
        if( $last_dept ne $dept ) {				###  改變系所則改變 TD 底色
          if($high_light =~ /FFFFFF/) {
            $high_light = "bgcolor = FFFF77";
          }else{
            $high_light = "bgcolor = FFFFFF";
          }
        }
  
		if( $IS_ENGLISH ) {
		  $dept_name		= $dept{'ename'};
		  $course_name		= $course{'ename'};
		}else{
		  $dept_name		= $dept{'cname2'};
		  $course_name		= $course{'cname'};
		}
  
        print "
          <TR $high_light>
            $TH2
            <TD>$dept_name</TD>
            <TD>$$gro_cour{cour_cd}</TD>
            <TD>$course_name</TD>  
            <TD>$course{credit}</TD>
          </TR>
        ";
        $last_dept = $dept;
      }
    }
  }
  print("</TD></TR>\n");
    


}

###############################################################################################
sub List_All_GRO()
{
  print qq(
    <CENTER>
    <TABLE border=1 class=font2>
      <TR bgcolor=YELLOW><TH>學程名稱</TH><TH>科目數</TH><TH>相關系所</TH></TR>
  );

  foreach $gro_no (keys %gro_name) {			###  所有 GRO
    $course_count = 0;
    foreach $gro_cour (@gro_cour) {				###  相關課程
      if( $$gro_cour{gro_no} eq $gro_no )  { 
        $dept = $cou_dept{$$gro_cour{cour_cd}};
        %course = Read_Course($dept, $$gro_cour{cour_cd}, "01", "", "");
        $course_count++  if( $course{cname} ne "" );      	###  本學期有開才++
      } 
    } 

    print qq(
      <TR>
        <TD><A href="Show_All_GRO.cgi?session_id=$Input{session_id}&gro_no=$gro_no">$gro_name{$gro_no}{gro_name}</A></TD>
        <TD>$course_count</TD>
        <TD>
    );
    foreach $gro_dept (@gro_dept) {				###  相關係所
      if( $$gro_dept{gro_no} eq $gro_no ) {
        %dept = Read_Dept($$gro_dept{dept});
        print(" $dept{cname2} ");
      }
    }
    print("</TD></TR>\n");
  }  
}

##################################################################################
#####  因應英文版本，將所有要顯示的文字在此整理，依照 $IS_ENGLISH 自動判別  2013/07/24
sub Init_Text_Values
{
  my %txtall;
  
  $yt_eng = Year_Term_English();
  
  %txtall = (
    'html_title'=> {'c'=>'跨領域學程 ' . $YEAR . ' 學年度第 ' . $TERM . ' 學期', 
						'e'=>"Interdiscplinary($yt_eng)"},
	'html_title2'=> {'c'=>'跨領域學程<BR>' . $YEAR . ' 學年度第 ' . $TERM . ' 學期', 
						'e'=>"Interdiscplinary<BR>$yt_eng"},
	'list1'			=> {'c'=>'以下是 ', 'e'=>'Below is the course list of '},
	'list2'			=> {'c'=>' 的相關課程', 'e'=>''},

	'add'			=> {'c'=>'加選', 'e'=>'Add course'},
	'dept'		=> {'c'=>'開課系所', 'e'=>'Department'},
	'cid'			=> {'c'=>'科目代碼', 'e'=>'Course ID'},
	'cname'		=> {'c'=>'科目名稱', 'e'=>'Course Title'},
	'credit'		=> {'c'=>'學分', 'e'=>'Credit'},

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













