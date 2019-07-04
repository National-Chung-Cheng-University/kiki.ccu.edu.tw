#!/bin/sh

cd /ultra2/project/ccmisp06/WWW/cgi-bin/superuser/Update/
/usr/local/bin/php Update_teacher_edu.php
/usr/local/bin/php Update_deduct.php 
/usr/local/bin/php Update_a14teng_gen_class.php
/usr/local/bin/php Update_a14tapply_eng_class.php
/usr/local/bin/php Update_a14tapply_eng_deduct_c.php
/usr/local/bin/php Update_early_warning_21_list.php
/usr/local/bin/php Update_change_school_student.php
