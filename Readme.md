## <u>Static Site Generator</u>
This is a static site generator which converts markdown 
files into HTML files. You can also host the generate HTML files on github pages very easily.
Long story short, this will create a static website from your markdown files and host it on GitHub Pages.


### <u>How to use</u>
To use this static site generator, follow these steps:
1. Clone the repository
2. Remove the existing `content` and `static` folders.
3. Create a folder named `content` in the root directory.
4. Add your markdown files to the `content` folder.
5. Add your CSS files to the `static` folder.
6. Add your images in the `images` folder within the `static` folder. When referencing images in your markdown files, use the path `/images/your_image_name.extension`.
7. Execute the `main.sh` script to generate the HTML files. They will be 
created in the `docs` folder.

### <u>How to host on GitHub Pages</u>
1. Create a new `github` repository.
2. Update the `build.sh` script with your repo name as follows:
   ```bash
   python3 src/main.py "/<your repo name>/"
   ```
3. Execute the `build.sh` script.
4. Push the `docs` folder to the github repository.
5. Open your repository's settings on Github and select the `Pages`
section.
    - Set the source to the `main` branch and the `docs` directory.
    - Save the settings.
    - Now the `/docs` directory on your `main` branch will auto 
   deploy to your GitHub Pages URL once something is in it.
   

