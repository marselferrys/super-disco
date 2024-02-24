@echo off
setlocal enabledelayedexpansion
for %%F in (*.*) do (
    if "%%~xF" neq "" (
        set "filename=%%~nF"
        set "extension=%%~xF"
        magick convert "%%F" -flop "!filename!-f!extension!"
    )
)
