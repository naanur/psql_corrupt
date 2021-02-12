IF FOLLOWING POSTGRESQL ERRORS OCCURS:
"missing chunk number x for toast value xxxxxxx in pg_toast_xxxxxxx"

OR

"unexpected chunk number xxx (expected x) for toast value xxxxxx in pg_toast_xxxxx"


TRY FIRST:
- "select reltoastrelid::regclass from pg_class where relname ='tablename';"
THEN 
- "REINDEX INDEX indexname_idx" of corrupted table.

uncomment this line #87 "# delete_by(id)" to delete corrupted
This script is used when another methods can't help.
!DATA WILL BE LOST!



