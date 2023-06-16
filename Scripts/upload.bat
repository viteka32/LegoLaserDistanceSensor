@ECHO OFF 
set comPort=%1
set volumeLabel=%2
set pathSW="..\SW\"
set pathFirmware="..\Firmware\"
set TMP_DIR="tempSW"

xcopy /e /i /s "%pathSW%" "%TMP_DIR%"

copy %pathFirmware%lego_vl53l1x_firmware.uf2 %volumeLabel%:
rshell -p %comPort% --buffer-size 512 cp tempSW/main.py tempSW/VL53L1X.py tempSW/LPF2.py /pyboard

IF EXIST %TMP_DIR% DEL /Q %TMP_DIR%\*
IF EXIST %TMP_DIR% RMDIR  %TMP_DIR%