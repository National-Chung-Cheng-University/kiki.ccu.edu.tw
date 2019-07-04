#!/usr/local/bin/perl

#############################################################################
#####  Update_Index.cgi
#####  ��ܨt�ΰѦҸ���ɮ�, ��������s�ɶ�
#####  Nidalap :D~
#####  2006/09/20
######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

my(%Input);
%Input=User_Input();

 HTML_Head("�t�ΰѦҸ�ƺ޲z�l�t��");
# print("pass = $Input{password}");
 $su_flag = Check_SU_Password($Input{password}, "su");
 if( $su_flag eq "TRUE" ) {
   HTML();
 }else{
   print("Password check error! system logged!!\n");
 }

##################################################################################
sub HTML_Head
{
  my($title);
  ($title)=@_;
  print("Content-type: text/html\n\n");
  print qq(
        <html>
    	  <SCRIPT language=JAVASCRIPT>
      		function Open_Update_Window(link)
   		{
        	  win=open(link,"openwin","width=600,height=800,resizable");
        	  win.creator=self;
      		}
	  </SCRIPT>
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=big5">
            <title>$title</title>
          </head>
          <BODY background="../../../Graph/manager.jpg">
            <CENTER>
              <H1>$title</H1>
              <HR size=2 width=50%>
  );
}         

###################################################################################
sub HTML
{
  print qq (
    <TABLE border=0>
      <TR><TD>
        <FORM action=View_crontab.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="�˵��۰ʧ�s�� crontab">
        </FORM>
        
        </TD><TD>
        
        <FORM action=View_update_log.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="�˵���s�ɮ�LOG">
        </FORM>
      </TR></TR>
    </TABLE>
  );
  print qq(
    <TABLE border=0 width=90%>
      <TR bgcolor=ORANGE><TH>�ɦW</TH><TH>��s�ɶ�</TH><TH>��Ƶ���</TH>
      <TH>����</TH><TH>�����s</TH></TR>      
  );
  
  List_file("grade_now");
  List_file("grade_summer");
  List_file("grade_all");
  List_file("deduct");
  List_file("std_orders");
#  List_file("qualify_english");
#  List_file("genedu_foreign_lang");
  List_file("a14teng_gen_class");
  
  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("dept");
  List_file("dept_com");

  print("<TR><TD colspan=6><HR></TD></TR>");    
  List_file("student");
  List_file("teacher");
  List_file("teacher_edu");
  List_file("change_school_student");
  List_file("dual");
  List_file("minor");
  List_file("early_warning_21_list");
    
  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("allcourse");
  List_file("a30tcourse");
  List_file("course_ncca");
  List_file("student_ncca");

  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("a14tapply_eng_class");
  List_file("a14tapply_eng_deduct_c");
  
  print("<TR><TD colspan=6><HR></TD></TR>");
  List_file("gro");

  print qq(
    </TABLE>
  );

}
###################################################################################
sub List_file
{
  my ($filename) = @_;
  
  my %X, $j, $size, $savetime, $timestring, @lines;

  @{$X{grade_now}}	= ( "��Ǵ����Z��: ���Z�d��, ���׬�ؿz��, �P���ƭײ߿z��|�Ψ�.",
			    $DATA_PATH . "Grade/now.txt",
                    	    "Update_grade_now.php" );  
  @{$X{grade_summer}}	= ( "���~���צ��Z��: ���Z�d��, ���׬�ؿz��, �P���ƭײ߿z��|�Ψ�.",
                    	    $DATA_PATH . "Grade/summer.txt",
                    	    "Update_grade_summer.php" );
  @{$X{grade_all}}	= ( "���~���Z��: ���Z�d��, ���׬�ؿz��, �P���ƭײ߿z��|�Ψ�.",
                            $DATA_PATH . "Grade/score",
                            "Update_grade_all01.php" );
  @{$X{teacher}}	= ( "�Юv��: �}�Ҹ�Ʒ|�Ψ�.",
                    	    $REFERENCE_PATH . "teacher.txt",
                    	    "Update_teacher01.php"  );  
  @{$X{student}}	= ( "���y�����: �ǥͿ��/�d�ߵ��|�Ψ�.",                                                           
                    	    $REFERENCE_PATH . "student.txt",
                    	    "Update_student01.php"  );  
  @{$X{change_school_student}} = ( "��ǥ͸����: �W�Ǵ���һP�z��ɷ|�Ψ�.",
                    	    $REFERENCE_PATH . "Change_School_Student.txt",
                    	    "Update_change_school_student.php" );
  @{$X{dept}}		= ( "�t�Ҹ����: �}�һP�ǥ;��y����.",
                            $REFERENCE_PATH . "Dept",
                            "Update_dept.php" );
  @{$X{dept_com}}	= ( "�t�ҹ����N�X��: �]���t�ҦX�@, �ɭP�t�ҧ��N�X�ҥ�.",
                            $REFERENCE_PATH . "dept_com.txt",
                            "Update_dept_com.php" );
  @{$X{deduct}}		= ( "��K���Z��: ���׬�ؿz��, �P���ƭײ߿z�ﳣ�|�Ψ�.",                                                           
                    	    $DATA_PATH . "Grade/deduct.txt",
                    	    "Update_deduct.php" );  
  @{$X{std_orders}}	= ( "�ǥͱƦW��: �d�ߦ��Z�|�Ψ�.",
                    	    $DATA_PATH . "Grade/std_orders.txt",
                    	    "Update_std_orders01.php"  );
#  @{$X{qualify_english}}= ( "�ǥͭ^���˩w���Z, ���׿z��|�Ψ�.",
#                            $DATA_PATH . "Grade/qualify_english.txt",
#                            "Update_qualify_english.php"  );
#  @{$X{genedu_foreign_lang}} = ("�s�ͭ^�˦��Z��, �Ω�P�O�ǥͭײ߳q�ѥ~�y�ҵ{�̾�.",
#                            $DATA_PATH . "Grade/genedu_foreign_lang.txt",
#                            "Update_genedu_foreign_lang.php" );
  @{$X{a14teng_gen_class}} = ("�q�ѭ^�y���Z��, �Ω�@���妸���J�s�ͳq�ѭ^�y�ҵ{�̾�, �H�ο�ҮɧY�ɧP�_�{�ץ�.",
                            $DATA_PATH . "Grade/a14teng_gen_class.txt",
                            "Update_a14teng_gen_class.php" );
  @{$X{teacher_edu}}	= ( "�ǵ{�����: �i�[��ǵ{���߶}���Ҫ��W��.",
                    	    $REFERENCE_PATH . "teacher_edu.txt",
                    	    "Update_teacher_edu.php" );
  @{$X{dual}}		= ( "���D�צW��: ��Ҵ����P�t�οz������ݭn��s.",
                    	    $REFERENCE_PATH . "double.txt",
                    	    "Update_dual.php" );
  @{$X{minor}}		= ( "���t�W��: ��Ҵ����P�t�οz������ݭn��s.",
                    	    $REFERENCE_PATH . "fu.txt",
                    	    "Update_minor.php" );
  @{$X{early_warning_21_list}} = ("�G�@��t�wĵ�W��: (���z�t)�Ω󻲾ɾǥͿ�Ҫ�����.",
                            $REFERENCE_PATH . "Early_Warning_21_List.txt",
                            "Update_early_warning_21_list.php" );
  @{$X{allcourse}}	= ( "���~�}����: �Ψӧ�s�}�ҨϥΪ����~�}�Ҹ��.",
                    	    $DATA_PATH . "Transfer/allcourse.txt",
                    	    "Update_allcourse01.php" );
  @{$X{course_ncca}}	= ( "<del>��Ǵ��}��/���ʭ���: ���Ǵ��}��/���ʸ�ƭ˨��ݸ�Ʈw.",
                    	    $HOME_PATH . "BIN/NCCA/NCCA020",
                    	    "Update_course_ncca01.php" );
  @{$X{student_ncca}}	= ( "<del>��Ǵ���ҭ���: ���Ǵ���Ҹ�ƭ˨��ݸ�Ʈw.",
                    	    $HOME_PATH . "BIN/NCCA/NCCA090",
                    	    "Update_student_ncca01.php" );
  @{$X{a30tcourse}}	= ( "�}�ҥN�X��: ���F�קK�}�ҨϥΨ� \"���g�}�L�o�S�}��\" ����إN�X, ���b�}�ҫe��s����.",
                            $REFERENCE_PATH . "a30tcourse.txt",
                            "Update_a30tcourse.php" );
  @{$X{gro}}		= ( "����ǵ{�N�X��: ���\\��|�@�֧�s gro_name, gro_dept, gro_cour, gro_std �|�Ӿǵ{�����ɮ�",
                            $REFERENCE_PATH . "gro_name.txt",
                            "Update_gro.php" );
  @{$X{a14tapply_eng_class}} = ( "���έ^�~�y�ǵ{�ͦW��, �Ω�[���������~�y�ҵ{�P�_.",
                            $REFERENCE_PATH . "a14tapply_eng_class.txt",
                            "Update_a14tapply_eng_class.php" );
  @{$X{a14tapply_eng_deduct_c}} = ( "�i�׽ҩ貦�~���e�ǥ�,  �Ω�[���������~�y�ҵ{�P�_.",
                            $REFERENCE_PATH . "a14tapply_eng_deduct_c.txt",
                            "Update_a14tapply_eng_deduct_c.php" );
  

  ($j,$j,$j,$j,$j,$j,$j,$j,$j,$savetime,$j) = stat($X{$filename}[1]);
  my ($sec, $min, $hour, $mday, $mon, $year, $k) = localtime($savetime);
  $year += 1900;
  $mon  ++;
  $timestring = $year . "/" . $mon . "/" . $mday . " - " . $hour . ":" . $min . ":" . $sec;
  $timecolor  = Determine_Time_Color($year, $mon, $mday);
  
  open(REF_FILE, $X{$filename}[1]);
  @lines = <REF_FILE>;
  $size = @lines;
  close(REF_FILE);

  print qq(
    <TR>
      <TD align=RIGHT><B>$filename</TD>
      <TD><FONT size=-1 color=$timecolor>$timestring</TD>
      <TD align=RIGHT>$size</TD>
      <TD><FONT size=-1>$X{$filename}[0]</TD>
      <TD align=CENTER><INPUT type=button value=��s onclick=Open_Update_Window("$X{$filename}[2]")></A></TD>
    </TR>
  );

}
###################################################################################
sub Determine_Time_Color
{
  my ($f_year, $f_mon, $f_mday) = @_;
  my $color;
  
  my ($sec, $min, $hour, $mday, $mon, $year, $k) = localtime();
  $year += 1900;
  $mon  ++;
  
  if( $year == $f_year ) {
    if( $mon == $f_mon )   {
      if( $mday == $f_mday )  {
        $color = "GREEN";			###  �P�~�P��P��
      }else{
        $color = "BLUE";			###  ���P��
      }
    }else{					###  ���P��
      $color = "ORANGE";    
    }  
  }else{					###  ���P�~
    $color = "RED";
  }
    
  return($color);
}