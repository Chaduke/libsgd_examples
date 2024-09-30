echo off
REM Set the drive letter just in case we are on a different one
c:

REM Make sure we are in the correct folder
REM Set the following to wherever you cloned libsgd_examples
cd c:\users\chadu\onedrive\projects\libsgd_examples\

REM Set file to equal whatever example you want to run 
REM You can also use this if you make your examples
REM Be careful not to add any spaces here or it will break 
set file=ex001

REM the gcc command line to compile 
REM here you can choose to compile with debug info for use with gdb or not
REM gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -std=c99 -ggdb -o %file% %file%.c -lsgd_dynamic
gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -o %file% %file%.c -lsgd_dynamic

REM If you have Visual Studio 2022 installed and want to use its compiler instead
REM comment out the gcc command above, and uncomment the next 3 lines below 
REM call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
REM cl /I "include" /c "%file%.c"
REM link /LIBPATH:"lib" "%file%.obj" sgd_dynamic.lib /OUT:"%file%.exe"

REM report if there is a compilation Error
if %errorlevel% == 1 echo Error in build!

REM if not run the compiled executable
if %errorlevel% == 0 %file%.exe