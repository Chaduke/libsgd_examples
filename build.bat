REM echo off
set file=ex002
c:
cd c:\users\chadu\onedrive\projects\c\libsgd_examples\
gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -o %file% %file%.c -lsgd_dynamic
if %errorlevel% == 1 echo Error in build!
if %errorlevel% == 0 %file%.exe