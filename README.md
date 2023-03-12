# Clipstory - clipboard history for macOS
> *[Download Latest Release](#)*


## About Clipstory
Clipstory is a clipboard history manager for macOS. 
The application lives as a tray icon in the menu bar.

Pressing the hotkey (**^V** / **ctrl+V**) brings up a list of you last clips, simply click on the one you want to paste and it will be pasted. When you paste from Clipstory the clip will also be added to the *"real clipboard"* accessed with (**⌘V**). 

## Settings
To access the settings click on the Clipstory icon in the menu bar.
<!--![](.gh-assets/menu-bar-icon-settings.png)-->
<img src=".gh-assets/menu-bar-icon-settings.png"  width="60%" height="30%">

> ### The settings explained:
> - **Max clipboard history count** –– *the maximum amount of clips saved in in history*
>   - *default*: **20**
>   - *max*: **99**
> - **Save history across sessions** –– *remember clipboard history when you log out*
>   - default: **true**


# Install

First [download the installer](#) and install it.

Once installed you will need to grant the app permission to "control the computer".\
 To do this go to: 
`System Settings > Security and Integrity > Accessability` \
select the `+` sign, navigate to `/Applications` and select **Clipstory**

# Contribute

### prerequisites

1. [install homebrew](https://brew.sh/)
2. *install python:*  `brew install python`
3. *install pipenv:* `python3 -m pip install pipenv`

### setting up
- *clone the repo:* `git clone https://github.com/Pingu1337/Clipstory.git`
- `cd Clipstory`
- *install packages from pipfile:* `pipenv install`
- *run the app:* `pipenv run python tray.py`


## License
Clipstory is licensed under the [**MIT License**](LICENSE)
