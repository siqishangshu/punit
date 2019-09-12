
@echo off
rem This is the logistics product component .
rem All copyright belongs to logistics.  
rem     https://www.siqishangshu.com/punit/download
rem     Author:siqishangshu@foxmail.com
rem Through the above link, you can get the latest software version and technical support.
rem If you have any questions in use, please consult yourdo.com.

rem ---------------------------------------------------------------------------
rem UnInstall script for the punit Server
rem ---------------------------------------------------------------------------
echo Start remove punit in your computer
set DIR="C:\punit"
set PRO=punit.exe

tasklist.exe -v | findstr %PRO% >NUL
if %ErrorLevel% == 0 (
	echo Stop the old Program
	taskkill.exe /F /IM %PRO% >NUL
)

if exist %DIR% (
	echo Clean old Verson Files
	rd /s /q %DIR% >NUL
)


ver|findstr /r /i "5.1.*" > NUL && goto WindowsXP
ver|findstr /r /i "6.1.*" > NUL && goto Windows7
ver|findstr /r /i "10.0.*" > NUL && goto Windows10
goto OtherVersion

:WindowsXP
msg "Sorry WindowsXP Not Support"
goto TheEnd

:Windows7
echo Windows7

if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\punit.exe.lnk" (
	echo Clean old link 
	del /F "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\punit.exe.lnk" >NUL
)

if exist "%USERPROFILE%\Desktop\punit.exe.lnk" (
	del /F "%USERPROFILE%\Desktop\punit.exe.lnk" >NUL
)
 
if exist "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\punit" (
    	rd /s /q "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\punit"
) 

goto TheEnd

:Windows10
echo Windows10

if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\punit.exe.lnk" (
	echo Clean old link
	del /F "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\punit.exe.lnk" >NUL
)

if exist "%USERPROFILE%\Desktop\punit.exe.lnk" (
	del /F "%USERPROFILE%\Desktop\punit.exe.lnk" >NUL
)

if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\punit" (
    	rd /s /q "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\punit"
)

goto TheEnd

:OtherVersion
echo OtherVersion 
if exist   (
	echo Clean old link 
	del /F "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\punit.exe.lnk" >NUL
)

if exist "%USERPROFILE%\Desktop\punit.exe.lnk" (
	del /F "%USERPROFILE%\Desktop\punit.exe.lnk" >NUL
)
 
if exist "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\punit"(
    	rd /s /q "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\punit"
)  
goto TheEnd

:TheEnd
msg %username% /time:7  "The punit uninstall successfully"
pause