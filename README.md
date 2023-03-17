# *Patpat-viewer*
A viewer for *[Patpat](https://github.com/henry-leo/Patpat)*

## Installation
Install Patpat-viewer by PyPI
```commandline
pip install patpat-viewer
```
## Usage
After installation, running the FLASK server will enter **the sample environment**.
As different systems have different methods for setting environment variables, operations may vary:

**Windows:**
```cmd
> set FLASK_APP=patpat_viewer
> set FLASK_ENV=production
> flask run
```

**Linux:**
```CIL
$ export FLASK_APP=patpat_viewer
$ export FLASK_ENV=production
$ flask run
```

Before starting the server, specify the **answers of [Patpat](https://github.com/henry-leo/Patpat)** `patpat_env`
by changing the environment variables:

**Windows:**
```cmd
...
> set PATPAT_ENV=<Absolute path of patpat_env>
> flask run
```

**Linux:**
```CIL
...
$ export PATPAT_ENV=<Absolute path of patpat_env>
$ flask run
```

### Example in Windows
We recommend using conda to manage environments. A clean environment makes me feel comfortable 
and can also prevent hair loss.

```cmd
(base)> conda create --name=patpat python=3.10
...
(base)> conda activate patpat
(patpat)> pip install patpat-viewer
...
(patpat)> set FLASK_APP=patpat_viewer
(patpat)> set FLASK_ENV=production
(patpat)> set PATPAT_ENV=D:\patpat_env
(patpat)> flask run
```

