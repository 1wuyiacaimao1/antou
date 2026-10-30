# 上传：先自检构建，通过了才提交、推送
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$siteUrl = "https://1wuyiacaimao1.github.io/antou/"
$logDir = Join-Path $root "_log"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logPath = Join-Path $logDir "upload.log"

try { Start-Transcript -Path $logPath -Force | Out-Null } catch { }

try {
    $now = Get-Date
    $stamp = $now.ToString("yyyy-MM-dd HH:mm")

    Write-Host ""
    Write-Host "  整理文件里的 frontmatter……" -ForegroundColor DarkGray
    if (Get-Command python -ErrorAction SilentlyContinue) {
        & python (Join-Path $root "fix_frontmatter.py")
    } else {
        Write-Host "  没找到 python，跳过这一步。" -ForegroundColor DarkYellow
    }

    Write-Host ""
    Write-Host "  在本机构建一次，写错了会在这里拦住。" -ForegroundColor DarkGray
    Write-Host ""

    $build = & npm run build 2>&1
    $code = $LASTEXITCODE

    if ($code -ne 0) {
        Write-Host ""
        Write-Host "  构建失败，没有推上去。" -ForegroundColor Red
        Write-Host "  下面是报错，把这段截图发给我：" -ForegroundColor DarkGray
        Write-Host ""
        $build | Select-Object -Last 30 | ForEach-Object { Write-Host "  $_" }
        Write-Host ""
        Write-Host "  详细记录在 _log\upload.log" -ForegroundColor DarkGray
        exit 1
    }

    Write-Host "  构建通过。" -ForegroundColor Green
    Write-Host ""

    & git add -A | Out-Null
    $changed = & git diff --cached --name-only

    if (-not $changed) {
        Write-Host "  没有改动，不用上传。" -ForegroundColor DarkGray
        exit 0
    }

    $msg = "记录 $stamp"
    & git -c user.name="wuyi" -c user.email="wuyi@example.com" commit -m $msg | Out-Null

    if ($LASTEXITCODE -ne 0) {
        Write-Host "  提交失败。" -ForegroundColor Red
        exit 1
    }

    Write-Host "  推送中……" -ForegroundColor DarkGray
    & git push
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "  推送失败，可能是没登录 GitHub。" -ForegroundColor Red
        Write-Host "  在终端里跑一次 git push，会弹出登录窗口，登完再试。" -ForegroundColor DarkGray
        exit 1
    }

    Write-Host ""
    Write-Host "  推上去了。GitHub 大约一分钟构建完：" -ForegroundColor Green
    Write-Host "  $siteUrl"
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "  出错了：$_" -ForegroundColor Red
    Write-Host "  详细记录在 _log\upload.log" -ForegroundColor DarkGray
    exit 1
}
finally {
    try { Stop-Transcript | Out-Null } catch { }
}
