[CmdletBinding()]
param()

$runtime = Join-Path $PSScriptRoot "ai_runtime.py"

function Invoke-Runtime {
    param([string[]]$Arguments)

    & python $runtime @Arguments
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nDer Runtime-Befehl ist fehlgeschlagen (Exitcode $LASTEXITCODE)." -ForegroundColor Red
    }
}

while ($true) {
    Clear-Host
    Write-Host "AI Runtime Control" -ForegroundColor Cyan
    Write-Host "==================" -ForegroundColor Cyan
    Invoke-Runtime @("status")
    Write-Host ""
    Write-Host "[1] Lokale AI pausieren (Gaming)"
    Write-Host "[2] Lokale AI fortsetzen"
    Write-Host "[3] Status aktualisieren"
    Write-Host "[0] Schliessen"
    $choice = Read-Host "Auswahl"
    if ($null -eq $choice) {
        exit 0
    }

    switch ($choice) {
        "1" {
            Invoke-Runtime @("block", "--reason", "gaming")
            Read-Host "Enter zum Fortfahren" | Out-Null
        }
        "2" {
            Invoke-Runtime @("unblock", "--reason", "gaming")
            Read-Host "Enter zum Fortfahren" | Out-Null
        }
        "3" {
            Read-Host "Enter zum Aktualisieren" | Out-Null
        }
        "0" {
            exit 0
        }
        default {
            Write-Host "Bitte 0, 1, 2 oder 3 waehlen." -ForegroundColor Yellow
            Start-Sleep -Seconds 1
        }
    }
}
