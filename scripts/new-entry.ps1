param(
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
    $form.ClientSize = New-Object System.Drawing.Size(330, 250)
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
        @{ key = "journal"; label = "随  记" },
        @{ key = "notes";   label = "笔  记" },
        @{ key = "lists";   label = "清  单" }
    )

    $top = 54
    foreach ($it in $items) {
        $b = New-Object System.Windows.Forms.Button
        $b.Text = $it.label
        $b.Tag = $it.key
        $b.Size = New-Object System.Drawing.Size(278, 48)
        $b.Location = New-Object System.Drawing.Point(26, $top)
        $b.FlatStyle = "Flat"
        $b.FlatAppearance.BorderColor = [System.Drawing.Color]::FromArgb(214, 206, 190)
        $b.BackColor = [System.Drawing.Color]::FromArgb(255, 253, 248)
        $b.TextAlign = "MiddleLeft"
        $b.Padding = New-Object System.Windows.Forms.Padding(20, 0, 0, 0)
        $b.ForeColor = [System.Drawing.Color]::FromArgb(40, 36, 30)
        $b.Add_Click({ $script:choice = $this.Tag; $form.Close() })
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
    "notes"   { "src/content/notes" }
    "lists"   { "src/content/lists" }
    default   { "src/content/journal" }
}

New-Item -ItemType Directory -Force -Path (Join-Path $root $dir) | Out-Null

# 同一天第二条自动加 -b/-c
$file = "$date.md"
$n = 1
while (Test-Path (Join-Path $root (Join-Path $dir $file))) {
    $n++
    $letter = [char](96 + $n)
    $file = "$date-$letter.md"
}

switch ($choice) {
    "lists" {
        $text = @"
---
date: $date
name: 
note: 
draft: false
---

<!-- 一行一项：- [ ] 想做的事 ／ 做完了改成 - [x] ／ 后面加 @2026 会显示年份 -->

- [ ] 
- [ ] 
- [ ] 
"@
    }
    default {
        $text = @"
---
date: $stamp
title: 
tags: []
draft: false
---

"@
    }
}

$path = Join-Path $root (Join-Path $dir $file)
[System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))

Write-Host ""
Write-Host "  已建好：$dir\$file" -ForegroundColor DarkGray

if ($NoUI) { exit 0 }

$code = Get-Command code -ErrorAction SilentlyContinue
if ($code) {
    Start-Process -FilePath "code" -ArgumentList "--goto", "`"$path`:8`""
} else {
    Start-Process -FilePath "notepad.exe" -ArgumentList "`"$path`""
}
