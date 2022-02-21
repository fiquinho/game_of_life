# Conway's Game of Life

This is my own implementation of [Conway's Game of Life](https://conwaylife.com/wiki/Conway's_Game_of_Life) 
in Python 3.6, using [PyGame](https://www.pygame.org/wiki/about) to render the application.


![Game of Life](https://s10.gifyu.com/images/app.gif)

## Usage

#### 1. Executable

There is an executable version of the application That doesn't require to install Python 
or any other dependencies. Is ready to use.

Just [download the zipped file](https://we.tl/t-cNfOvRGj8e), extract it's contents, and run the <code>main.exe</code> 
executable file.

#### 2. Using a Python environment

Clone the repository, and activate your Python 3.6 environment. From the project folder 
install the necessary packages with:

<code>pip install -r requirements.txt</code>

Then run the application with:

<code>python main.py</code>

#### 3. Generate executable from source code

Same steps as point 2, but instead of running the application from the <code>main.py</code> file,
generate a standalone executable with [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/).

First we install the package in our environment with:

<code>pip install pyinstaller</code>

And then we generate the executable:

<code>pyinstaller --noconsole --add-data=game/assets/\*;game/assets --add-data=game/boards/\*;game/boards main.py</code>

The file will be in <code>repo/dir/dist/main/main.exe</code>.


## Resources

- https://www.pygame.org/wiki/about
- https://conwaylife.com/wiki/Conway's_Game_of_Life
- https://www.1001fonts.com/
