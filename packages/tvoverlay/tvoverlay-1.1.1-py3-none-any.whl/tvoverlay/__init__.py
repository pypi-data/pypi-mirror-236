"""Library for sending notifications to TVOverlay."""

from __future__ import annotations

import uuid
import base64
import logging
from typing import Any

import httpx

from .const import (
    DEFAULT_APP_ICON,
    DEFAULT_APP_NAME,
    COLOR_GREEN,
    DEFAULT_DURATION,
    # DEFAULT_LARGE_ICON,
    DEFAULT_SMALL_ICON,
    DEFAULT_TITLE,
    DEFAULT_SOURCE_NAME,
    Positions,
    Shapes,
)

from .exceptions import ConnectError, InvalidResponse, InvalidImage

_LOGGER = logging.getLogger(__name__)

# _ALLOWED_IMAGES = ["image/gif", "image/jpeg", "image/png"]

class Notifications:
    """Notifications class for TVOverlay."""

    def __init__(
        self,
        host: str,
        port: int = 5001,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize notifier."""
        self.url = f"http://{host}:{port}"
        self.httpx_client = httpx_client
        _LOGGER.debug("TVOverlay initialized")

    async def async_connect(self) -> str:
        """Test connecting to server."""
        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )
        try:
            async with httpx_client as client:
                response = await client.get(self.url + "/get", timeout=5)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Connection to host: {self.url} failed!") from err
        if response.status_code == httpx.codes.OK:
            _LOGGER.debug("TVOverlay Connect response: %s", response.json())
            return response.json()
        else:
            raise InvalidResponse(f"Error connecting host: {self.url}")

    async def async_send(
        self,
        message: str,
        id: str | None = str(uuid.uuid1()),
        title: str | None = DEFAULT_TITLE,
        deviceSourceName: str | None = DEFAULT_SOURCE_NAME,
        appTitle: str | None = DEFAULT_APP_NAME,
        appIcon: str | ImageUrlSource | None = None,
        image: str | ImageUrlSource | None = None,
        smallIcon: str | None = DEFAULT_SMALL_ICON,
        smallIconColor: str | None = COLOR_GREEN,
        corner: str = Positions.TOP_RIGHT.value,
        seconds: int | None = DEFAULT_DURATION,
    ) -> str:
        """Send notification with parameters.

        :param message: The notification message.
        :param title: (Optional) The notification title.
        :param id: (Optional) ID - Ff a notification is being displayed and the tvoverlay receives a notification with the same id, the notification displayed is updated instantly
        :param appTitle: (Optional) App Title text field.
        :param appIcon: (Optional) Accepts mdi icons, image urls and Bitmap encoded to Base64.
        :param color: (Optional) appIcon color accepts 6 or 8 digit color hex. the '#' is optional.
        :param image: (Optional) Accepts mdi icons, image urls.
        :param smallIcon: (Optional) Accepts mdi icons, image urls and Bitmap encoded to Base64.
        :param largeIcon: (Optional) Accepts mdi icons, image urls and Bitmap encoded to Base64.
        :param corner: (Optional) Notification Position values: bottom_start, bottom_end, top_start, top_end.
        :param seconds: (Optional) Display the notification for the specified period in seconds.
        Usage:
        >>> from tvoverlay import Notifications
        >>> notifier = Notifications("192.168.1.100")
        >>> notifier.async_send(
                "message to be sent",
                "title"="Notification title",
                "id": 0,
                "appTitle": "MyApp",
                "appIcon": "mdi:unicorn",
                "color": "#FF0000",
                "image": "https://picsum.photos/200/100",
                "smallIcon": "mdi:bell",
                "largeIcon": "mdi:home-assistant",
                "corner": "bottom_left",
                "seconds": 20
            )
        """
        if appIcon:
            appIcon_b64 = await self._async_get_b64_image(appIcon)
        else:
            appIcon_b64 = DEFAULT_APP_ICON

        if image:
            image_b64 = await self._async_get_b64_image(image)
        else:
            image_b64 = None

        data: dict[str, Any] = {
            "id": id,
            "title": title,
            "message": message,
            "deviceSourceName": deviceSourceName,
            "appIcon": appIcon_b64,
            "appTitle": appTitle,
            "smallIcon": smallIcon,
            "color": smallIconColor,
            "image": image_b64,
            "corner": corner.replace("left", "start").replace("right", "end"),
            "seconds": seconds,
        }

        headers = {"Content-Type": "application/json"}

        _LOGGER.debug("data: %s", data)

        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )
        try:
            async with httpx_client as client:
                response = await client.post(
                    self.url + "/notify", json=data, headers=headers, timeout=5
                )
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(
                f"Error sending notification to {self.url}: {err}"
            ) from err
        if response.status_code == httpx.codes.OK:
            _LOGGER.debug("TVOverlay send notification response: %s", response.json())
            return response.json()
        else:
            raise InvalidResponse(f"Error sending notification: {response}")

    async def async_send_fixed(
        self,
        message: str,
        id: str | None = str(uuid.uuid1()),
        icon: str | None = None, # DEFAULT_APP_ICON,
        textColor: str | None = None, # "#FFFFFF",
        iconColor: str | None = None, # "#FFFFFF",
        borderColor: str | None = None, # "#FFFFFF",
        backgroundColor: str | None = None, # "#000000",
        shape: str = Shapes.CIRCLE.value,
        expiration: str | None = "5",
        visible: bool | None = True,
    ) -> str:
        """Send Fixed notification.

        :param message: "Sample" # REQUIRED: this is a required field for home assistant, but it can be 'null' if not needed
        :param id: "fixed_notification_sample" # optional id string - if a fixed notification with this id exist, it will be updated
        :param icon: mdi:unicorn  # optional - accepts mdi icons, image urls and Bitmap encoded to Base64
        :param textColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param iconColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param borderColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param backgroundColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param shape: "circle" # optional - values: circle, rounded, rectangular
        :param expiration: "7m"  # optional - valid formats: 1695693410 (Epoch time), 1y2w3d4h5m6s (duration format) or 123 (for seconds)
        :param visible: true  # optional - if false it deletes the fixed notification with matching id

        Usage:
        >>> from tvoverlay import Notifications
        >>> notifier = Notifications("192.168.1.100")
        >>> notifier.async_send_fixed(
                message: "Sample"
                id: "fixed_notification_sample"
                icon: "mdi:bell"
                textColor: "#FFF000"
                iconColor: "#FFF000"
                borderColor: "#FFF000"
                backgroundColor: "#FFF000"
                shape: "circle"
                expiration: "7m"
                visible: true
            )
        """
        if icon:
            appIcon_b64 = await self._async_get_b64_image(icon)
        else:
            appIcon_b64 = None

        data: dict[str, Any] = {
            "id": id,
            "message": message,
            "textColor": textColor,
            "icon": appIcon_b64,
            "iconColor": iconColor,
            "borderColor": borderColor,
            "backgroundColor": backgroundColor,
            "shape": shape,
            "expiration": expiration,
            "visible": visible,
        }

        headers = {"Content-Type": "application/json"}

        _LOGGER.debug("data: %s", data)

        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )
        try:
            async with httpx_client as client:
                response = await client.post(
                    self.url + "/notify_fixed", json=data, headers=headers, timeout=5
                )
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(
                f"Error sending fixed notification to {self.url}: {err}"
            ) from err
        if response.status_code == httpx.codes.OK:
            _LOGGER.debug("TVOverlay send fixed notification response: %s", response.json())
            return response.json()
        else:
            raise InvalidResponse(f"Error sending fixed notification: {response}")

    async def _async_get_b64_image(self, image_source: ImageUrlSource | str) -> Any | bytes | None:
        """Load file from path or url."""
        if isinstance(image_source, ImageUrlSource):
            httpx_client: httpx.AsyncClient = (
                self.httpx_client if self.httpx_client else httpx.AsyncClient()
            )
            try:
                async with httpx_client as client:
                    response = await client.get(
                        image_source.url, auth=image_source.auth, timeout=10, follow_redirects=True
                    )
            except (httpx.ConnectError, httpx.TimeoutException) as err:
                raise InvalidImage(
                    f"Error fetching image from {image_source.url}: {err}"
                ) from err
            if response.status_code != httpx.codes.OK:
                raise InvalidImage(
                    f"Error fetching image from {image_source.url}: {response}"
                )
            if "image" not in response.headers["content-type"]:
                raise InvalidImage(
                    f"Response content type is not an image: {response.headers['content-type']}"
                )
            return await self._get_base64(response.content)
        elif (image_source.startswith("mdi:") or image_source.startswith("http://") or image_source.startswith("https://")):
            return image_source
        else:
            try:
                if image_source.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    with open(image_source, "rb") as file:
                        image = file.read()
                    return await self._get_base64(image)
                else:
                    raise InvalidImage("Invalid Image: %s", image_source)
            except FileNotFoundError as err:
                raise InvalidImage(err) from err

    async def _get_base64(self, filebyte: bytes) -> str | None:
        """Convert the image to the expected base64 string."""
        base64_image = base64.b64encode(filebyte).decode("utf8")
        return base64_image


class ImageUrlSource:
    """Image source from url or local path."""

    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        auth: str | None = None,
    ) -> None:
        """Initiate image source class."""
        self.url = url
        self.auth: httpx.BasicAuth | httpx.DigestAuth | None = None

        if auth:
            if auth not in ["basic", "disgest"]:
                raise ValueError("authentication must be 'basic' or 'digest'")
            if username is None or password is None:
                raise ValueError("username and password must be specified")
            if auth == "basic":
                self.auth = httpx.BasicAuth(username, password)
            else:
                self.auth = httpx.DigestAuth(username, password)
