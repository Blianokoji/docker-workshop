<#
.SYNOPSIS
    Builds and optionally pushes all Docker Workshop images to Docker Hub.
.PARAMETER Username
    The Docker Hub username/namespace (defaults to 'dracalar').
.PARAMETER NoPush
    Switch to build images locally without pushing to Docker Hub.
.PARAMETER NoCache
    Switch to force rebuilds from scratch without using layer cache.
.EXAMPLE
    .\build-and-push.ps1 -NoPush
    .\build-and-push.ps1 -Username dracalar
#>
param(
    [string]$Username = "dracalar",
    [switch]$NoPush,
    [switch]$NoCache
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🐳 Docker Workshop Image Builder & Publisher" -ForegroundColor Cyan
Write-Host " Docker Hub Namespace: $Username" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# Check Docker CLI
try {
    $dockerVer = docker version --format '{{.Client.Version}}'
    Write-Host "[OK] Docker CLI detected: $dockerVer" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker CLI not found or not in PATH." -ForegroundColor Red
    exit 1
}

# Check Docker Daemon
try {
    docker info > $null 2>&1
    Write-Host "[OK] Docker Daemon is running and responsive." -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker Daemon is NOT running. Please start Docker Desktop first!" -ForegroundColor Red
    exit 1
}

if (-not $NoPush) {
    Write-Host "`n[AUTH] Ensuring Docker Hub authentication..." -ForegroundColor Yellow
    docker login
}

$cacheFlag = if ($NoCache) { "--no-cache" } else { "" }

$images = @(
    @{
        Name = "docker-workshop-explore"
        Path = "01-explore"
        File = "Dockerfile"
    },
    @{
        Name = "docker-workshop-broken"
        Path = "02-fix-the-dockerfile"
        File = "Dockerfile"
    },
    @{
        Name = "docker-workshop-notebook"
        Path = "03-volumes"
        File = "Dockerfile"
    },
    @{
        Name = "docker-workshop-api"
        Path = "04-networking\api"
        File = "Dockerfile"
    },
    @{
        Name = "docker-workshop-frontend"
        Path = "04-networking\frontend"
        File = "Dockerfile"
    },
    @{
        Name = "docker-workshop-vote-api"
        Path = "05-compose-voting-app\vote-api"
        File = "Dockerfile"
    },
    @{
        Name = "docker-workshop-vote-dashboard"
        Path = "05-compose-voting-app\dashboard"
        File = "Dockerfile"
    }
)

$rootDir = $PSScriptRoot
$total = $images.Count
$current = 1

foreach ($img in $images) {
    $tag = "$Username/$($img.Name):latest"
    $contextPath = Join-Path $rootDir $img.Path

    Write-Host "`n----------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "[$current/$total] Building: $tag" -ForegroundColor Cyan
    Write-Host "Context : $contextPath" -ForegroundColor DarkGray

    $cmd = "docker build $cacheFlag -t $tag -f $(Join-Path $contextPath $img.File) $contextPath"
    Invoke-Expression $cmd

    if (-not $NoPush) {
        Write-Host "Pushing $tag to Docker Hub..." -ForegroundColor Yellow
        docker push $tag
        Write-Host "[SUCCESS] Pushed $tag" -ForegroundColor Green
    }

    $current++
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " 🎉 ALL $($images.Count) WORKSHOP IMAGES READY!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
foreach ($img in $images) {
    Write-Host "  ✔ $Username/$($img.Name):latest" -ForegroundColor White
}