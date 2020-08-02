# Manganelo Manga downloader
A python program that will download manga from [manganelo](https://manganelo.com/)

# Prerequisite
All the packages that is required to run Manga ripper can be installed by running 
```bash
pip install -r requirements.txt
```
# Downloading manga
You will need a manganelo manga link and copy the last path (Highlighted in blue) <br>
![example](Capture.png)


and then you need to run
```bash
python mangaRipper.py [insert manga last path here]
```

<h4>Example</h4>
```bash
python mangaRipper.py rokudenashi_blues
```
The program will ask you for a folder to save the manga in.

Once the manga has been downloaded it will convert it into a .cbz
file.

