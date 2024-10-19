echo off
REM "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64

cd c:\users\chadu\onedrive\projects\libsgd_examples\runner_demo
cmake -G "Visual Studio 17 2022" -S . -B c:\dev\runner_demo_build
cmake --build c:\dev\runner_demo_build --config Release
cd ..\

REM report if there is a compilation Error
if %errorlevel% == 1 echo Error in build!

REM if not run the compiled executable
if %errorlevel% == 0 (
copy C:\dev\runner_demo_build\Release .
.\RunnerDemo.exe )