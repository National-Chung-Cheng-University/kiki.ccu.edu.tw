#!/usr/local/bin/perl -w

#############################################################################
#####  Update_teacher03.cgi
#####  ���Ϳ�ܱЮv javascript �� $FileName, �Ѷ}�Үɿ�ܥ�
#####    1. �ѤH�ƨt��upload�s���Юv�ɫ�, �n�b�}�ƽҨt�ΤW���s���Ѯv, 
#####       ���ݥ��]�L�o�ӵ{��, ��s�̷s��( $FileName )��, �}�Ҩt�ΤW�����.
#####    2. �t�~�p�G���s�t��, �]�n�t�]�LClassifyDept.pl�çⲣ�� ��html code�[��
#####       AddTeacherWindow.html��.
#####  Updates:
#####    199?       Coder: Ionic, Hanchu(199?)
#####    2000/02/15 �i�@�B�B�z����r��, ��֨ƫ�ݤ�ʧ���ɮת����D Nidalap)
#####    2009/02/05 �q Generate_Teachers_Classification.pl �ק令���z�L��������.(Nidalap)
#############################################################################

$| = 1;
require "../../library/Reference.pm";
require $LIBRARY_PATH."Teacher.pm";

print("Content-type:text/html\n\n");
print ("<BODY background=\"../../../Graph/manager.jpg\">");
print ("<CENTER><H1>��s�Юv�����</H1><HR>\n");
print ("���b��s�}�ҿ�ܱЮv��ƺ��� Teacher.js, �åB�B�z����X...<P>\n");

#$source = $REFERENCE_PATH . "teacher_temp.txt";
my($FileName)=$CGI_PATH . "project/Teachers.js";

open(TEACHERCLASS,">$FileName") or 
             die("Cannot open file $FileName.\n");

####    print ���Ϊk���A�ϥ� ' ����޸��A�i�H�������Ҥ������@�ǯS��r��
####    �]�����|�N�o�ǯS��r�����ܼƪ��}�Y�ӨϥΡA�]���i�H�w�ߨϥΦC�L
####    ���\��C

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

  @exception_words = ('�\\\\', '�\\\\');
  
  $exception_flag = 0;
  if($Teacher_Name{$Teacher} =~ /\\/g) {
    foreach $word (@exception_words) {			### �o�Ǧr�������ӥ[�W escape �X, �_�h js ����|����.
      if( $Teacher_Name{$Teacher} =~ /$word/ ) {
        $exception_flag = 1;
      }
    }
    if( $exception_flag != 1 ) {
      $Teacher_Name{$Teacher} =~ s/\\/\\\\/;
      $escape++;
#      print("��줤�����X�íץ�: $Teacher_Name{$Teacher}<BR>\n");
    }else{
      $ignore++;
#      print("��줤�����X�����L: * $Teacher_Name{$Teacher}<BR>\n");
    }
#    $Teacher_Name{$Teacher} = "(temp)";
  }

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
   ��줤�����X�íץ�: $escape �����<BR>
   ��줤�����X�����L: $ignore �����<P>
   
   ����!<P>
   
  <INPUT type=button value="��������" onClick="window.close()">
];