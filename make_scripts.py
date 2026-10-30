import pathlib

ROOT = pathlib.Path(r"D:\hanacoagent\life-site")
(ROOT / "scripts").mkdir(exist_ok=True)

new_entry = r'''param(
    [string]$Type = "",
    [switch]$NoUI
)

# 写一条：选类型、生成模板、打开编辑器
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

function Show-Chooser {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "写一条"
    $form.ClientSize = New-Object System.Drawing.Size(320, 250)
    $form.StartPosition = "CenterScreen"
    $form.TopMost = $true
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.BackColor = [System.Drawing.Color]::FromArgb(251, 250, 247)
    $form.Font = New-Object System.Drawing.Font("Microsoft YaHei", 11)

    $title = New-Object System.Windows.Forms.Label
    $title.Text = "今天想记点什么"
    $title.AutoSize = $true
    $title.Location = New-Object System.Drawing.Point(26, 20)
    $title.ForeColor = [System.Drawing.Color]::FromArgb(60, 56, 50)
    $form.Controls.Add($title)

    $script:choice = $null
    $items = @(
        @{ key = "journal"; label = "随  记"; hint = "可以写" },
        @{ key = "moments"; label = "瞬  间 · 用 1-整理图片"; hint = "还没接" },
        @{ key = "notes";   label = "笔  记 · 还没接"; hint = "还没接" }
    )

    $top = 54
    foreach ($it in $items) {
        $b = New-Object System.Windows.Forms.Button
        $b.Text = $it.label
        $b.Tag = $it.key
        $b.Size = New-Object System.Drawing.Size(268, 48)
        $b.Location = New-Object System.Drawing.Point(26, $top)
        $b.FlatStyle = "Flat"
        $b.FlatAppearance.BorderColor = [System.Drawing.Color]::FromArgb(214, 206, 190)
        $b.BackColor = [System.Drawing.Color]::FromArgb(255, 253, 248)
        $b.TextAlign = "MiddleLeft"
        $b.Padding = New-Object System.Windows.Forms.Padding(20, 0, 0, 0)
        if ($it.hint -eq "还没接") {
            $b.Enabled = $false
            $b.ForeColor = [System.Drawing.Color]::FromArgb(190, 182, 170)
        } else {
            $b.ForeColor = [System.Drawing.Color]::FromArgb(40, 36, 30)
            $b.Add_Click({ $script:choice = $this.Tag; $form.Close() })
        }
        $form.Controls.Add($b)
        $top += 58
    }

    [void]$form.ShowDialog()
    $form.Dispose()
    return $script:choice
}

if ($NoUI) {
    if (-not $Type) { Write-Host "NoUI 模式需要 -Type"; exit 1 }
    $choice = $Type
} else {
    $choice = Show-Chooser
}

if (-not $choice) { exit 0 }

$now = Get-Date
$date = $now.ToString("yyyy-MM-dd")
$stamp = $now.ToString("yyyy-MM-dd HH:mm")

$dir = switch ($choice) {
    "journal" { "src/content/journal" }
    "moments" { "src/content/moments" }
    "notes"   { "src/content/notes" }
    default   { "src/content/journal" }
}

New-Item -ItemType Directory -Force -Path (Join-Path $root $dir) | Out-Null

# 同一天第二条自动加 -b/-c
$base = $date
$file = "$base.md"
$n = 1
while (Test-Path (Join-Path $root (Join-Path $dir $file))) {
    $n++
    $letter = [char](96 + $n)
    $file = "$base-$letter.md"
}

$head = @"
---
date: $stamp
title: 
tags: []
draft: false
---

"@

$body = @"
"@

switch ($choice) {
    "journal" {
        $body = "`r`n"
    }
    "moments" {
        $inbox = Join-Path $root (Join-Path "_inbox" $date)
        $lines = @()
        if (Test-Path $inbox) {
            Get-ChildItem $inbox -Filter *.webp | Sort-Object Name | ForEach-Object {
                $lines += "![](./$($_.Name))"
            }
        }
        $body = ($lines -join "`r`n`r`n") + "`r`n`r`n"
    }
    "notes" {
        $body = "`r`n" + '```' + "`r`n" + '```' + "`r`n"
    }
}

$path = Join-Path $root (Join-Path $dir $file)
$text = $head + $body
[System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))

Write-Host ""
Write-Host "  已建好：$dir\$file" -ForegroundColor DarkGray

if ($NoUI) { exit 0 }

$code = Get-Command code -ErrorAction SilentlyContinue
if ($code) {
    Start-Process -FilePath "code" -ArgumentList "--goto", "`"$path`:8`"
} else {
    Start-Process -FilePath "notepad.exe" -ArgumentList "`"$path`""
}
'''

publish = r'''# 上传：先自检构建，通过了才提交、推送
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$siteUrl = "https://1wuyiacaimao1.github.io/antou/"
$now = Get-Date
$stamp = $now.ToString("yyyy-MM-dd HH:mm")

Write-Host ""
Write-Host "  先整理一下文件里的 frontmatter。" -ForegroundColor DarkGray
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python (Join-Path $root "fix_frontmatter.py")
}

Write-Host ""
Write-Host "  先在本机构建一次，写错了会在这里拦住。" -ForegroundColor DarkGray
Write-Host ""

$build = & npm run build 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  构建失败，没有推上去。" -ForegroundColor Red
    Write-Host "  下面是报错，把这段截图发给我就行：" -ForegroundColor DarkGray
    Write-Host ""
    $build | Select-Object -Last 30 | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
    Read-Host "  按回车关闭"
    exit 1
}

Write-Host "  构建通过。" -ForegroundColor Green
Write-Host ""

& git add -A | Out-Null
$changed = & git diff --cached --name-only
if (-not $changed) {
    Write-Host "  没有改动，不用上传。" -ForegroundColor DarkGray
    Start-Sleep -Seconds 2
    exit 0
}

$msg = "记录 $stamp"
& git -c user.name="wuyi" -c user.email="wuyi@example.com" commit -m $msg | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  提交失败。" -ForegroundColor Red
    Read-Host "  按回车关闭"
    exit 1
}

Write-Host "  推送中……" -ForegroundColor DarkGray
& git push
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  推送失败，可能是没登录 GitHub。" -ForegroundColor Red
    Write-Host "  在终端里跑一次 git push，会弹出登录窗口，登完再试。" -ForegroundColor DarkGray
    Read-Host "  按回车关闭"
    exit 1
}

Write-Host ""
Write-Host "  推上去了。GitHub 大约一分钟构建完：" -ForegroundColor Green
Write-Host "  $siteUrl"
Write-Host ""
Start-Sleep -Seconds 3
'''

(ROOT / "scripts" / "new-entry.ps1").write_text(new_entry, encoding="utf-8-sig")
(ROOT / "scripts" / "publish.ps1").write_text(publish, encoding="utf-8-sig")

bat_new = r'''@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\new-entry.ps1"
if errorlevel 1 pause
'''

bat_pub = r'''@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\publish.ps1"
'''

(ROOT / "2-写一条.bat").write_text(bat_new, encoding="utf-8")
(ROOT / "3-上传.bat").write_text(bat_pub, encoding="utf-8")

print("written")
for f in ["scripts/new-entry.ps1", "scripts/publish.ps1", "2-写一条.bat", "3-上传.bat"]:
    p = ROOT / f
    print(f, p.stat().st_size, "bytes")
