Sure, here is the contents of the run.bat file:

```bash
@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Running program...
python main.py

echo Program completed.
pause
```

This run.bat file will first install the required dependencies listed in the requirements.txt file using pip. Then, it will execute the main.py file. Finally, it will display a message indicating the program completion and pause the terminal so that the user can see the output before it closes.