# DSCI560_HW5
California Coronavirus Dashboard

## Instructions for executing the dashboard on your computer
1. Install Python 3.7.8
2. Open your terminal and go to the directory you want to download this repository
3. Download this repository in the directory
```
git clone https://github.com/Myunghee13/DSCI560_HW5.git
```
4. Go to the repository folder you downloaded 
```
cd DSCI560_HW5
```
5. Install virtualenv
```
pip install virtualenv
```
6. Create a virtual environment, named visu
```
py -m venv visu
```
7. Activate the virtual environment, visu
```
.\visu\Scripts\activate
```
8. Install the dependencies
```
pip install -r requirements.txt
```
9. Execute app.py
```
bokeh serve --show app.py
```
9. You can see the dashboard on your browser.
```
http://localhost:5006/app
```
10. Deactivate the virtual environment, visu
```
deactivate
```
## Instructions for executing the dashboard through Docker
1. Go to [play with docker](https://labs.play-with-docker.com/).
2. Log in and start.
3. Add new instance

