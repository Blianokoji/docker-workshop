#!/bin/sh
clear
if command -v figlet >/dev/null 2>&1; then
    figlet -f standard "DOCKER 101"
else
    echo "========================================"
    echo "            DOCKER 101                 "
    echo "========================================"
fi

echo "🐳 Welcome to your isolated Linux container sandbox!"
echo "--------------------------------------------------------"
echo "  Container Hostname : $(hostname)"
echo "  Operating System   : $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"')"
echo "  Container IP       : $(hostname -i 2>/dev/null || ip route get 1 2>/dev/null | awk '{print $NF;exit}')"
echo "  Current User       : $(whoami) (UID: $(id -u))"
echo "  Running Processes  : $(ps -e | wc -l) process(es)"
echo "--------------------------------------------------------"
echo ""
echo "🚀 Try running these commands inside this container:"
echo "   1. figlet 'Hello World'               # Generate ASCII banners"
echo "   2. curl -s https://icanhazip.com      # Check external network egress"
echo "   3. ps aux                             # Look at isolated processes"
echo "   4. touch /test.txt && ls -l /test.txt # Create a test file"
echo "   5. exit                               # Leave the container"
echo ""
exec bash