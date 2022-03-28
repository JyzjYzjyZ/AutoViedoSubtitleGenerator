set /p venv_name=venv_name:
echo Configuration:%venv_name%
conda create -n %venv_name% python=3.9
call activate %venv_name% --no-stack
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r "D:\setup\requirements_AudioFormatConversion_goodjin5.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install D:\setup\pyannote-audio-develop.zip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install "D:\setup\torch-cp39-cu111-1.9\torch-1.9.0+cu111-cp39-cp39-win_amd64.whl"
pip install "D:\setup\torch-cp39-cu111-1.9\torchaudio-0.9.0-cp39-cp39-win_amd64.whl"
pip install "D:\setup\torch-cp39-cu111-1.9\torchvision-0.10.0+cu111-cp39-cp39-win_amd64.whl"
pip install transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install vosk  -i https://pypi.tuna.tsinghua.edu.cn/simple
pip list
echo Your virtual environment has been successfully created
pause