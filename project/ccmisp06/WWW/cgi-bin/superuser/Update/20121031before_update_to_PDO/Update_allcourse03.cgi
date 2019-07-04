#!/usr/local/bin/perl -w

###########################################################################################################
#####  Update_allcourse03.cgi
#####  ���Ϳ�ܥ��׬����( $FileName )
#####  �}�ҵ{����, �ݭn��ܥ��׬�خ�, �I�� "��ܥ��׬��" �����, ���X�@��
#####  HTML�����ѿ��, ��HTML�����Y�Ѱ��榹�{���Ҳ���. HTML�������]�t�����~
#####  �}�Ҹ��, �G�ݰʺA����. 
#####
#####  �ݭn�ɮ�: $DATA_PATH/History/Course/*
#####            $REFERENCE_PATH/Dept
#####  �����ɮ�: ~/WWW/cgi-bin/project/Add_Precourse_Window.html
#####  ����ɾ�: �C�Ǵ��}�ҫe.
#####  ps.
#####    ���M�w�b�Юv�W�r���ˬd�������X, �����ͪ�Javascript�ɦb�Y�Ǫ���browser
#####    �������D, �ì�����X���D.
#####  Updates:
#####    2001/04/17 �� Generate_Teacher_Classification.pl ��g. Nidalap :D~
#####    2009/06/06 �N���{���q�W�ߪ�����Generate_Precourse_Classification.pl�A�h��@�t�C��s���~�}�Ҹ�ƥ\��.
#####               �P�ɰt�X�t�ҦX�@�ݨD�A�N���}�Ҫ��t�ҥh��(�z�L�I�s Find_All_Dept ���Ѽ�)  Nidalap :D~
#############################################################################################################

require "../../library/Reference.pm";
require $LIBRARY_PATH . "Dept.pm";
require $LIBRARY_PATH . "Course.pm";

print("Content-type:text/html\n\n");

print ("<BODY background=\"../../../Graph/manager.jpg\">");
print ("<CENTER><H1>��s���~�}�Ҹ����</H1><HR>\n");
print ("���b��s���׬�ؿ�ܺ��� Add_Precourse_Window.html,<BR>�åB�B�z����X...<P>\n");

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
    <HEAD><TITLE>�s�W���׬�ص���</TITLE></HEAD>
    <! -------------------------------------------------- !>
    <! ��HTML�ɬO�ѵ{������, �D���n�ФŪ����ק糧�ɮפ��e !>
    <! -------------------------------------------------- !>
);   
      

$precourse_count = Create_JS_Data_Code();
Create_JS_Code();
Create_HTML_Code();
#Create_JS_Data_Code();

print qq [
   �@�B�z $precourse_count ���}�Ҹ��, �����I<P>   
  <INPUT type=button value="��������" onClick="window.close()">
];

#############################################################################
#####  Create_JS_Code()
#####  ��HTML������Javascript�{��, �]�A�Ҧ�Javascript�ұ���欰
#############################################################################
sub Create_JS_Code
{
  print HTML qq(
      <SCRIPT language=JAVASCRIPT>
        
        // �ϥΪ̧��t�ҫ�, ����Өt�Ҫ��Ҧ����~��ئb�����a�X�� 
        function OnChangeDept(dept, course)
        {
          course.length = 1;
          var i=1;
          var flag = 0;
          var temp;
          
          course.options[0].text	= "�L";
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
        
        //  ��ܦn�t��, ���, ���ƫ�, AddPrecourse()���ưe�^�}�ҥD����
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
            alert('�п�ܥ��׬�ئA�e�X���!');
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
#####  ��HTML�����ͭn�q�X�Ӫ�HTML�X, �]�A��ܨt��, ���, ���Ƥ�����FORM���
#############################################################################
sub Create_HTML_Code
{
  print HTML qq(
    <BODY background = "../../Graph/ccu-bg.jpg" onload=JSCreatePrecourse()>
      <CENTER>
        <H2>�s�W���׬�ر��󭭨�</H2>
      </CENTER>
        <HR>
        <FORM name=precourse_form>
          <FONT size=-1>�п�ܨt��:</FONT><BR>
          &nbsp&nbsp
          <SELECT name="dept" onChange="OnChangeDept(document.precourse_form.dept, document.precourse_form.course)">
            <OPTION value=99999>�п�ܨt��\n
  );
  foreach $dept (@dept) {
    %dept = Read_Dept($dept);
    print HTML ("<OPTION value=$dept>$dept{cname2}\n");
  }
  print HTML qq(          
          </SELECT>
          <BR>
          <FONT size=-1>�п�ܥ��׬��:</FONT><BR>
          &nbsp&nbsp
          <SELECT name="course">
            <OPTION value=99999>�L�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@
          </SELECT>
          <BR>
          <FONT size=-1>�п�ܥ��׬�ؤ��ƭ���:</FONT><BR>
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
          <INPUT type=button value="�e�X���" onclick="AddPrecourse(this.form)">
        </FORM>
        <FONT size=-1>
          1. �ϥλ���: �Х���ܨt�ҫ�, �A��ܥ��׬�ؤΤ��ƭ���,
          �̫��I��e�X���, �t�η|�N�z�ҿ�ܪ���Ʊa��}�ҥD����.<BR>
          2. �Y�X�{���~�T��, ��������������, �A�b�}�ҥD�������I��"��ܥ��׬��".
             
      </CENTER>
    <BODY>
  );
}
#############################################################################
#####  Create_JS_Data_Code()
#####  ��HTML������Javascript�{���һݸ��, �D�n�O�U���~��ت����l�ƪ�JS�X.
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
