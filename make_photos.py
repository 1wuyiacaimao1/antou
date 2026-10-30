import pathlib

ROOT = pathlib.Path(r"D:\hanacoagent\life-site")
(ROOT / "scripts").mkdir(exist_ok=True)

ps = r'''Add-Type -AssemblyName System.Windows.Forms

$dlg = New-Object System.Windows.Forms.FolderBrowserDialog
$dlg.Description = "选一个装着照片的文件夹"
$dlg.SelectedPath = [Environment]::GetFolderPath("MyPictures")
if (-not (Test-Path $dlg.SelectedPath)) {
    $dlg.SelectedPath = [Environment]::GetFolderPath("Desktop")
}

$r = $dlg.ShowDialog()
if ($r -ne [System.Windows.Forms.DialogResult]::OK) { exit 0 }

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host ""
Write-Host "  处理中……" -ForegroundColor DarkGray
Write-Host ""

& python (Join-Path $root "scripts\photos.py") $dlg.SelectedPath
$code = $LASTEXITCODE

if ($code -ne 0) {
    Write-Host ""
    Write-Host "  没有生成内容，检查一下照片格式。" -ForegroundColor DarkYellow
    exit 1
}

$day = (Get-Date).ToString("yyyy-MM-dd")
$md = Join-Path $root "src\content\moments\$day.md"

Write-Host ""
Write-Host "  打开这一篇，写一句话吧。" -ForegroundColor Green

if (Get-Command code -ErrorAction SilentlyContinue) {
    Start-Process -FilePath "code" -ArgumentList "--goto", "`"$md`:4`""
} else {
    Start-Process -FilePath "notepad.exe" -ArgumentList "`"$md`""
}
'''

bat = r'''@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\photos.ps1"
echo.
pause
'''

(ROOT / "scripts" / "photos.ps1").write_text(ps, encoding="utf-8-sig")
(ROOT / "1-整理图片.bat").write_text(bat, encoding="utf-8")
print("written")
