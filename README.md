# aidoru

a qt music player in python

![music player in playing album mode](img/main.png)

## Installation

You must install Qt5 library and python3. After that, do:

```
pip3 install --user -r requirements.txt
```

*Linux users*, if this issue:

```
defaultServiceProvider::requestService(): no service found for - "org.qt-project.qt.mediaplayer"
```

upon running, then:

 1. install your distro's equivalent to `libqt5multimedia5-plugins`
 2. remove `~/.local/lib/python3*/dist-packages/PyQt5/Qt/plugins/mediaservice/libgstmediaplayer.so`
 3. `ln -s /usr/lib/x86_64-linux-gnu/qt5/plugins/mediaservice/libgstmediaplayer.so ~/.local/lib/python3*/dist-packages/PyQt5/Qt/plugins/mediaservice/libgstmediaplayer.so`

## Credits

- Breeze/Paper icons
