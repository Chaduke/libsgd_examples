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

REM call the python example 
python %file%.py