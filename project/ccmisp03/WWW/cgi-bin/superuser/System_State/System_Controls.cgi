#!/usr/local/bin/perl
print("Content-type:text/html\n\n");
#############################################################################
#####  System_Controls.cgi 
#####  ��Ҩt�ά����]�w
#####  ��X��Ҩt�Ϊ��@�ǭ���}���]�w
#####  Coder: Nidalap :D~
#####   Date: 2002/06/06
#############################################################################
require "../../library/Reference.pm";
require $LIBRARY_PATH . "GetInput.pm";
require $LIBRARY_PATH . "System_Settings.pm";

@{$option{cge_ban_grade}}		= ("������", "���}��j�|", "���}��j�T�j�|");
@{$option{allow_print_student_course}}	= ("���}��C�L", "�}��C�L");
@{$option{show_last_total}}		= ("����ܿz���l�B���", "��ܿz���l�B���");
@{$option{show_immune_count}}		= ("����ܥi�[��W�B���", "��ܥi�[��W�B���");
@{$option{allow_query_last_select_namelist}} = ("���i�d�ߤW���z���W��", "�i�d�ߤW���z���W��");
@{$option{no_ban}}			= ("���\\�����t�׭�", "�����t�׭׳]�w�L��");
@{$option{allow_select_math}}		= ("�}��[��ƾǨt�ҤΨ�L�t�ҵ{","�u�}��[��D�ƾǨt�ҽҵ{","�u�}��[��ƾǨt�ҽҵ{");
@{$option{allow_print_pdf}}		= ("���}��C�L", "�}��C�L");
@{$option{allow_print_graduate_pdf}}	= ("���}��C�L", "�}��C�L");
@{$option{force_print_graduate_pdf}}	= ("���n�D�T�{", "�n�D�T�{");
@{$option{redirect_to_query}}		= ("���t�ΤW�u��", "�ШϥΪ̳s�u�ܬd�ߨt��");
@{$option{black_list}}			= ("�����¦W��\\��", "�}�Ҷ¦W��\\��");

%Input = User_Input();

if( $Input{modify_flag} == 1 ) {
  Write_System_Settings(%Input);
}

%flags = Read_System_Settings();
Show_Page();
#############################################################################
sub Show_Page()
{
  print qq (
    <HTML>
      <HEAD><TITLE>��Ҩt�ά����]�w</TITLE></HEAD>
      <BODY background="$GRAPH_URL/ccu-sbg.jpg">
      <CENTER>
      <H1>��Ҩt�ά����]�w</H1>
      <HR>
      <FORM action="System_Controls.cgi" method=POST>
      <TABLE border=1>
        <TR>
          <TH>�]�w�W��</TH>
          <TH>�]�w����</TH>
          <TH>�]�w</TH>
        </TR>
  );
  Show_Selection("cge_ban_grade", "�q�Ѥ��߽ҵ{���}��j�|���",
                 "�q�Ѥ��߽ҵ{���}��j�T�j�|�ǥͭ׽�.
                  �ѩ�q�Ѥ��߬F��, �Ĥ@���q���}��j�T�j�|�ͭ׽�.");
  
  Show_Selection("allow_print_student_course", "�}��C�L��ҳ�",
                 "�u���b�ĤG���q��ҫ�~�C�L��ҳ檺�\\��,
                  ���]�w�M�w�ӥ\\��O�_�}��.");
  Show_Selection("allow_print_pdf", "�}��C�L��ҽT�{pdf��",
                 "�[�h�ﵲ����ѱоǲղ��Ϳ�ҵ��G�T�{��(pdf��), 
                  ��ѹq�⤤�߰����ɮפ��t�{�����i�}��.");

  Show_Selection("allow_print_graduate_pdf", "�}��C�L���~���f�dpdf��",
                 "�оǲդ��w����s���~���f��pdf��, 
                  ��ѹq�⤤�߰����ɮפ��t�{�����i�}��.");

  Show_Selection("force_print_graduate_pdf", "�n�D�T�{���~���f�dpdf��",
                 "��󦳲��~���f�d�ɪ��P��, �j��n���T�{�Ӹ�ƫ�~����.
                  �Y�}�Ҧ��ﶵ, �W�@�ӿﶵ�]�����}��."); 

  Show_Selection("show_last_total", "�O�_��ܤW���z���l�B",
                 "�b�ĤG���q���h���z��L�{��,
                  ��ܦ���ƥi�קK�ǥͿ�@�Ǥ��ӥi���W����.
                  �����N��ܦb�[��ɪ���ؿ�椤");
  Show_Selection("show_immune_count", "�O�_��ܥi�[��W�B�H��",
                 "�b�����Ĺ���ɬq��, ��ܦ����,
                 �i�[��W�B = (���פH��) + (�w�[�諸�[ñ�H��) - (�ثe�Ҧ���פH��)
                 �����N��ܦb�[��ɪ���ؿ�椤");
  Show_Selection("allow_query_last_select_namelist", "�O�_�i�H�d�ߤW���z���W��",
                 "(�Юv)�d�߿�ҦW��\\�त, 
                 �O�_�X�{�i�d�� \"�W���z���W��\" �ﶵ");
  Show_Selection("no_ban", "�O�_���\\�����t�׭�",
                 "(�ĤG���q��Ү�)�Y�]�w�������t�׭׵L��,
                 �Ҧ��W�L�Q�Ӭ�ت��׭׳]�w(���P�������t)�N���@��(�q�ѻP�x�V�ҵ{���b����)");
  Show_Selection("allow_select_math", "�O�_�}��[��ƾǨt�Ҷ}�]���ҵ{",
                 "�Ĥ@���q��Ү�, �ƾǨt�Ҫ��ҵ{�ĥ����Ĺ�B������, 
                 �t�οW�߬Y�@�ѱM����׼ƾǨt�Ҷ}�]���ҵ{, �G�����ﶵ");
  Show_Selection("redirect_to_query", "�O�_�ШϥΪ̳s�u�ܬd�ߨt��",
                 "�t�ηǳƤU�Ǵ��}�Ҵ���, �|�⥻�Ǵ���ƲM��,
                 ���ɭn�]�w�ШϥΪ̳s�u�ܸ�Ƭd�ߺ���(ccmisp03/04)");
  Show_Selection("black_list", "�O�_�}�Ҷ¦W��\\��",
                 "�[�隸�ƤӹL�����¦W��. �Y�O�}�Ҧ��\\��, 
                 �¦W�椤���ǥͷ|�b�D���ݨ�ĵ�i�T��. �Y�������\\��,
                 �t�Τ��|���� log, �u�O���|���ĵ�T.");

  print qq(
      </TABLE>
      <P>
        <INPUT type=hidden name=modify_flag value=1>
        <INPUT type=submit>
      </FORM>
  );
}

#####################################################################
sub Show_Selection()
{
  my($selection, $name, $descriptions) = @_;
  my(@option, $i, $option_count);
  
  @option = @{$option{$selection}};
  
  print qq(
    <TR>
      <TD>$name</TD>
      <TD><FONT color=GREEN size=2>$descriptions</TD>
      <TD>
        <SELECT name="$selection">
  );
  $option_count = @option;
  for( $i=0; $i<$option_count; $i++ ) {
    if( $i eq $flags{$selection} ) {
      print("<OPTION value=$i SELECTED>$option[$i]\n");
    }else{
      print("<OPTION value=$i        >$option[$i]\n");
    }
  }
  print qq(
        </SELECT>
      </TD>
    </TR>
  );
}


