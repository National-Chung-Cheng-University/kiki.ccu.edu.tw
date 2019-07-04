<?PHP
  ////////////////////////////////////////////////////////////////////////////
  /////  Update_teacher01.php
  /////  更新開課代碼檔 teacher.txt
  /////  query_string 來自人事, 會計等系統上的人事資料. (提供者:惠萍)
  /////  Coder: Nidalap :D~
  /////  Updates:
  /////    2009/02/05  created
  /////    2012/10/30  改採 PDO 連資料庫 by Nidalap :D~
  /////    2015/03/23  赫然發現以前新增英文姓名欄位的程式不見了，重新加入！ by Nidalap :D~
  ////////////////////////////////////////////////////////////////////////////
  
  include "../../php_lib/Reference.php";
  include $LIBRARY_PATH . "Database.php";
  include $LIBRARY_PATH . "Error_Message.php";

  $filename   = "teacher.txt";  
  $outputfile = $REFERENCE_PATH . $filename;
  $time_start = time();

  echo $EXPIRE_META_TAG;
  echo("<BODY background=\"../../../Graph/manager.jpg\">");
  echo("<CENTER><H1>更新教師資料檔</H1><HR>");            
  $DBH = PDO_connect($PERSONNELDB_DB_NAME);

  $query_string = "
select unit_cd,staff_cd,c_name,e_name
from dblink('dbname=accdb_run host=localhost port=5432 user=ccumis password=!misdbadmin@ccu',$$
SELECT h0btcomm_proj.department_cd,
      p0btproj_dt_staff.id,
      h0btcomm_proj.name,
	  h0btcomm_proj.e_name
FROM p0btproj_dt_staff LEFT OUTER JOIN h0btcomm_proj ON(p0btproj_dt_staff.id = h0btcomm_proj.id)
     
WHERE  p0btproj_dt_staff.staff_type = 'A' 
$$)
as t1(unit_cd char(4),staff_cd char(10),c_name varchar(40), e_name varchar(40))

--提聘人員檔(尚未完成聘任手續)

union

select unit_cd,staff_cd,c_name,e_name
from dblink('dbname=personneldb host=localhost port=5432 user=ccumis password=!misdbadmin@ccu',$$
      SELECT h0etnew_prof.unit_cd,
             h0etnew_prof.staff_cd,
             h0etnew_prof.c_name,
			 h0etnew_prof.e_name
       FROM h0etnew_prof
        where h0etnew_prof.d_end >= ltrim((to_char(extract('year' from current_date)-1911,'000'))|| ltrim(to_char(extract('month' from current_date),'00'))|| ltrim(to_char(extract('day' from current_date),'00')))
$$)
AS t1(unit_cd char(4),staff_cd char(10),c_name varchar(40), e_name varchar(40))

--教師聘期檔
union

select unit_cd,staff_cd,c_name,e_name
from dblink('dbname=personneldb host=localhost port=5432 user=ccumis password=!misdbadmin@ccu',$$
     SELECT h0etoffer.unit_cd,
            h0btbasic_per.staff_cd,
            h0btbasic_per.c_name,
			h0btbasic_per.e_name
     FROM h0btbasic_per,
          h0etoffer
WHERE ( h0etoffer.staff_cd = h0btbasic_per.staff_cd ) and
      ( ( h0btbasic_per.is_current = '1' ) AND
        ( h0etoffer.is_current in ('y','Y') ) AND
        ( h0etoffer.off_continue in ('y','Y') ) 
       )
$$)
AS t1(unit_cd char(4),staff_cd char(10),c_name varchar(40), e_name varchar(40))

--現職異動檔
union

select unit_cd,staff_cd,c_name,e_name
from dblink('dbname=personneldb host=localhost port=5432 user=ccumis password=!misdbadmin@ccu',$$

    select h0etchange.unit_cd,
           h0btbasic_per.staff_cd,
           h0btbasic_per.c_name,
		   h0btbasic_per.e_name
      from  h0btbasic_per,
            h0etchange
      where h0btbasic_per.staff_cd = h0etchange.staff_cd and
            h0btbasic_per.dist_cd='TEA' and
            h0btbasic_per.is_current='1' and
            h0etchange.is_current in('y','Y') and
            h0btbasic_per.staff_cd not in 
            ( SELECT h0etnew_prof.staff_cd
                FROM h0etnew_prof ) 
$$)
AS t1(unit_cd char(4),staff_cd char(10),c_name varchar(40), e_name varchar(40));
  
  ";
 
  $STH = $DBH->prepare($query_string);
  $STH->execute();
  list($save_succeed, $rowcount) = Save_Update_File_PDO($outputfile);
  
  $time = time() - $time_start;
  if( $rowcount == 0 ) {
    echo("資料抓取失敗！ 抓不到任何資料，可能是 sql 語法有問題！<BR>\n");
    echo("以下是 SQL script, 用來做偵錯使用:<BR></CENTER><PRE>");
    echo $query_string;
  }else if( $save_succeed == 0 ) {
    echo("存檔失敗! 可能是檔案權限問題<BR>\n");
    echo("<FONT color=RED>本程式可能只能在正式系統 ccmisp06 上執行</FONT><BR>\n");
  }else{
    echo("更新 $filename		: $rowcount 筆資料, 耗時 $time 秒<P>\n");
    echo("請繼續執行<BR><A href=Update_teacher02.cgi>更新資料第二步</A>");    
  }
  
  echo("以下是 SQL script, 用來做偵錯使用:<BR></CENTER><PRE>");
  echo $query_string;
  
  Update_Log($filename, $rowcount, $time);
    
?>
