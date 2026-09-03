$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:gitBusy = $false

function Invoke-GitAutoPush {
    if ($script:gitBusy) { return }
    $script:gitBusy = $true

    try {
        Set-Location $repoPath

        $status = git status --porcelain
        if ([string]::IsNullOrWhiteSpace($status)) {
            return
        }

        git add .
        $branch = git branch --show-current
        if ([string]::IsNullOrWhiteSpace($branch)) {
            $branch = "main"
        }

        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "Auto-save $timestamp" | Out-Null

        git push origin $branch
    }
    catch {
        Write-Host "Auto push failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        $script:gitBusy = $false
    }
}

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $repoPath
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true
$watcher.Filter = "*.*"

$eventAction = {
    param($sender, $eventArgs)

    $fullPath = $eventArgs.FullPath
    if ($fullPath -match '\\.git\\') {
        return
    }

    Start-Sleep -Milliseconds 500
    Invoke-GitAutoPush
}

Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $eventAction | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Created -Action $eventAction | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Deleted -Action $eventAction | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $eventAction | Out-Null

Write-Host "Auto Git push is running. Watching: $repoPath"
Write-Host "Press Ctrl+C to stop."

while ($true) {
    Start-Sleep -Seconds 5
}
