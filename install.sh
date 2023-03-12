#!/bin/zsh
brew install python 
python3 -m pip install pipenv 

echo "#!/bin/zsh \npython3 -m pipenv run python $(pwd)/tray.py &"  > Clipstory.sh
sudo chmod +x Clipstory.sh
echo "Done!"