<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_teacher01.php
  /////  ��s�}�ҥN�X�� teacher.txt
  /////  query_string �ӦۤH��, �|�p���t�ΤW���H�Ƹ��. (���Ѫ�:�f��)
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2009/02/05  created
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Sybase.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "teacher.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>��s�Юv�����</H1><HR>");            
  db_connect_personneldb();

  $query_string = "
SELECT accdb_run..h0btcomm_proj.department_cd,
                accdb_run..p0btproj_dt_staff.id,
                accdb_run..h0btcomm_proj.name
FROM accdb_run..p0btproj_dt_staff,
             accdb_run..h0btcomm_proj
WHERE ( accdb_run..p0btproj_dt_staff.id *= accdb_run..h0btcomm_proj.id) and
                ( ( accdb_run..p0btproj_dt_staff.staff_type = 'A' ) )


UNION

SELECT personneldb..h0etnew_prof.unit_cd,
                personneldb..h0etnew_prof.staff_cd,
                personneldb..h0etnew_prof.c_name
FROM personneldb..h0etnew_prof
WHERE 
convert(char(4),convert(numeric(3),substring(personneldb..h0etnew_prof.d_end,1,3))+1911)+substring(personneldb..h0etnew_prof.d_end,4,2)+substring(personneldb..h0etnew_prof.d_end,6,2) 
>= convert(char(10),getdate(),112)

UNION

SELECT personneldb..h0etoffer.unit_cd,
                personneldb..h0btbasic_per.staff_cd,
                personneldb..h0btbasic_per.c_name
FROM personneldb..h0btbasic_per,
             personneldb..h0etoffer
WHERE ( personneldb..h0etoffer.staff_cd = 
personneldb..h0btbasic_per.staff_cd ) and
               ( ( personneldb..h0btbasic_per.is_current = '1' ) AND
               ( personneldb..h0etoffer.is_current in ('y','Y') ) AND
               ( personneldb..h0etoffer.off_continue in ('y','Y') ) )

UNION

select personneldb..h0etchange.unit_cd,
       personneldb..h0btbasic_per.staff_cd,
       personneldb..h0btbasic_per.c_name
from  personneldb..h0btbasic_per,
      personneldb..h0etchange
where personneldb..h0btbasic_per.staff_cd = 
personneldb..h0etchange.staff_cd and
      personneldb..h0btbasic_per.dist_cd='TEA' and
      personneldb..h0btbasic_per.is_current='1' and
      personneldb..h0etchange.is_current in('y','Y') and
      personneldb..h0btbasic_per.staff_cd not in (  SELECT 
personneldb..h0etnew_prof.staff_cd
                                                  FROM 
personneldb..h0etnew_prof ) 

  ";
    
  $result_id	= sybase_query($query_string, $link);
  print("result_id = $result_id<BR>\n");
  $last_msg = sybase_get_last_message();
  print("��Ʈw�Ǧ^�T���G$last_msg<BR>\n");
  $rowcount	= sybase_num_rows($result_id);
//  $columncount	= sybase_num_fields($result_id);
  
  $save_succeed = Save_Update_File($outputfile, $result_id, $rowcount);
  
  $time = time() - $time_start;
  if( $rowcount == 0 ) {
    echo("��Ƨ�����ѡI �줣������ơA�i��O sql �y�k�����D�I<BR>\n");
    echo("�H�U�O SQL script, �ΨӰ������ϥ�:<BR></CENTER><PRE>");
    echo $query_string;
  }else if( $save_succeed == 0 ) {
    echo("�s�ɥ���! �i��O�ɮ��v�����D<BR>\n");
    echo("<FONT color=RED>���{���i��u��b�����t�� ccmisp06 �W����</FONT><BR>\n");
  }else{
    echo("��s $filename		: $rowcount �����, �Ӯ� $time ��<P>\n");
    echo("���~�����<BR><A href=Update_teacher02.cgi>��s��ƲĤG�B</A>");    
  }
  
  echo("�H�U�O SQL script, �ΨӰ������ϥ�:<BR></CENTER><PRE>");
  echo $query_string;
  
  Update_Log($filename, $rowcount, $time);
    
?>
