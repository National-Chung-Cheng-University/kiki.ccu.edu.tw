#!/usr/local/bin/perl

#############################################################################
#####  index.cgi
#####  ���ѳs��, �ΨӲ��Ͷ}�Ҹ���R�A������, �H�ΥH�ɶ��d�߶}�Ҹ�ƪ����
#####  Nidalap :D~
#####  2008/11/13
######### require .pm files #########
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "Password.pm";
require $LIBRARY_PATH . "Error_Message.pm";

my(%Input);
%Input=User_Input();

 HTML_Head("���Ͷ}���R�A����");
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
        	  win=open(link,"openwin","width=350,height=350,resizable");
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
        <FORM action=Create_Course_View.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="�����R�A�}��HTML����">
        </FORM>
        
        </TD><TD>
        
        <FORM action=Create_Course_View_by_Time.cgi method=POST target=NEW>
          <INPUT type=hidden name=password value=$Input{password}>
          <INPUT type=submit value="���ͥH�}�Үɶ��d�ߪ����">
        </FORM>
      </TR></TR>
    </TABLE>
  );

}
###################################################################################
sub List_file
{
  my ($filename) = @_;
  
  my %X, $j, $size, $savetime, $timestring, @lines;

  @{$X{grade_now}}	= ( "���Ǵ����Z��: ���Z�d��, ���׬�ؿz��, �P���ƭײ߿z��|�Ψ�.",
			    $DATA_PATH . "Grade/now.txt",
                    	    "Update_grade_now.php" );  
  @{$X{grade_summer}}	= ( "���~���צ��Z��: ���Z�d��, ���׬�ؿz��, �P���ƭײ߿z��|�Ψ�.",
                    	    $DATA_PATH . "Grade/summer.txt",
                    	    "Update_grade_summer.php" );
  @{$X{teacher}}	= ( "<del>�Юv��: �}�Ҹ�Ʒ|�Ψ�.",
                    	    $REFERENCE_PATH . "teacher.txt",
                    	    "Update_teacher01.php"  );  
  @{$X{student}}	= ( "���y�����: �ǥͿ��/�d�ߵ��|�Ψ�.",                                                           
                    	    $REFERENCE_PATH . "student.txt",
                    	    "Update_student01.php"  );  
  @{$X{change_school_student}} = ( "<del>��ǥ͸����: �W�Ǵ���һP�z��ɷ|�Ψ�.",
                    	    $REFERENCE_PATH . "Change_School_Student.txt",
                    	    "Update_change_school_student.php" );
  @{$X{deduct}}		= ( "��K���Z��: ���׬�ؿz��, �P���ƭײ߿z�ﳣ�|�Ψ�.",                                                           
                    	    $DATA_PATH . "Grade/deduct.txt",
                    	    "Update_deduct.php" );  
  @{$X{std_orders}}	= ( "�ǥ;��~�ƦW: �d�ߦ��Z�|�Ψ�.",
                    	    $DATA_PATH . "Grade/std_orders.txt",
                    	    "Update_std_orders.php"  );
  @{$X{qualify_english}}= ( "�ǥͭ^���˩w���Z, ���׿z��|�Ψ�.",
                            $DATA_PATH . "Grade/qualify_english.txt",
                            "Update_qualify_english.php"  );
  @{$X{teacher_edu}}	= ( "�ǵ{�����: �i�[��ǵ{���߶}���Ҫ��W��.",
                    	    $REFERENCE_PATH . "teacher_edu.txt",
                    	    "Update_teacher_edu.php" );
  @{$X{dual}}		= ( "���D�צW��: ��Ҵ����P�t�οz������ݭn��s.",
                    	    $REFERENCE_PATH . "double.txt",
                    	    "Update_dual.php" );
  @{$X{minor}}		= ( "���t�W��: ��Ҵ����P�t�οz������ݭn��s.",
                    	    $REFERENCE_PATH . "fu.txt",
                    	    "Update_minor.php" );
  @{$X{allcourse}}	= ( "���~�}����: �Ψӧ�s�}�ҨϥΪ����~�}�Ҹ��.",
                    	    $DATA_PATH . "Transfer/allcourse.txt",
                    	    "Update_allcourse01.php" );
  @{$X{course_ncca}}	= ( "<del>���Ǵ��}��/���ʭ���: ����Ǵ��}��/���ʸ�ƭ˨��ݸ�Ʈw.",
                    	    $HOME_PATH . "BIN/NCCA/NCCA020",
                    	    "Update_course_ncca01.php" );
  @{$X{student_ncca}}	= ( "<del>���Ǵ���ҭ���: ����Ǵ���Ҹ�ƭ˨��ݸ�Ʈw.",
                    	    $HOME_PATH . "BIN/NCCA/NCCA090",
                    	    "Update_student_ncca01.php" );
  @{$X{a30tcourse}}	= ( "�}�ҥN�X��: ���F�קK�}�ҨϥΨ� \"���g�}�L�o�S�}��\" ����إN�X, ���b�}�ҫe��s����.",
                            $REFERENCE_PATH . "a30tcourse.txt",
                            "Update_a30tcourse.php" );
  @{$X{gro}}		= ( "����ǵ{�N�X��: ���\\��|�@�֧�s gro_name, gro_dept, gro_cour, gro_std �|�Ӿǵ{�����ɮ�",
                            $REFERENCE_PATH . "gro_name.txt",
                            "Update_gro.php" );

                  

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