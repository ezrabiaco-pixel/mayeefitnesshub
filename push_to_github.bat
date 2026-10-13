@echo off
echo ========================================================
echo MayeeFitness Hub - GitHub Push Helper
echo ========================================================
echo.
git add .
git commit -m "Update MayeeFitness Hub"
git push -u origin main
echo.
echo Done! Render will automatically deploy your latest code.
pause
