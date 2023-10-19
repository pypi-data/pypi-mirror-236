# TVOverlay Notifications

### Python API for TVOverlay Notification

<p align="center">
<picture><img src="https://github.com/gugutab/TvOverlay/blob/main/images/readme_main.png?raw=true" alt="TvOverlay" width="600"></picture>
<br>
<a href="https://play.google.com/store/apps/details?id=com.tabdeveloper.tvoverlay">
<img src="https://github.com/gugutab/TvOverlay/blob/main/images/playstore.png?raw=true" width="300" /></a>
<a href="https://play.google.com/store/apps/details?id=com.tabdeveloper.tvoverlayremote">
<img src="https://github.com/gugutab/TvOverlay/blob/main/images/playstore_remote.png?raw=true" width="300" /></a>	
</p>

Source: https://github.com/gugutab/TvOverlay

## Usage

- Install the application on your TV
- Get the IP of the TV unit

```python
from tvoverlay import Notifications
notify = Notifications("192.168.1.10")

try:
    await notify.async_connect()
expect ConnectError:
    return False
await notify.async_send(
    "message text",
    title="Title text",
)
```

## Optional parameters

```json
{
    "message": "Message",
    "title": "Title",
    "id": "test1",
    "appTitle": "Postman",
    "appIcon": "mdi:unicorn",
    "color": "#FFC107",
    "image": "https://picsum.photos/200/100",
    "smallIcon": "mdi:bell",
    "largeIcon": "mdi:home-assistant",
    "corner": "bottom_end",
    "seconds": 20
}
```
