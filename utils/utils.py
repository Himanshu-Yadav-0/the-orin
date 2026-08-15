import psutil
import httpx
from pathlib import Path
from urllib.parse import urlparse
from loguru import logger

def is_wifi_connected() -> bool:
    return psutil.net_if_stats()['Wi-Fi'].isup

def download_file(url: str, directory: str):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path(urlparse(url).path).name
    file_path = directory / filename

    logger.info("Starting download: {}", filename)
    logger.debug("Saving to: {}", file_path)

    try:
        with httpx.stream("GET", url) as response:
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            logger.info(
                "Connected to server: {} {}",
                response.status_code,
                response.reason_phrase,
            )

            if total_size:
                logger.info("File size: {:.2f} MB", total_size / 1024 / 1024)
            else:
                logger.info("File size: unknown")

            downloaded = 0
            last_logged_percent = -1

            with open(file_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    if not chunk:
                        continue

                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size:
                        percent = int(downloaded * 100 / total_size)

                        if percent >= last_logged_percent + 10:
                            logger.info(
                                "Downloading {}: {}% ({:.2f}/{:.2f} MB)",
                                filename,
                                percent,
                                downloaded / 1024 / 1024,
                                total_size / 1024 / 1024,
                            )
                            last_logged_percent = percent
                    else:
                        logger.info(
                            "Downloaded {}: {:.2f} MB",
                            filename,
                            downloaded / 1024 / 1024,
                        )

            logger.success(
                "Download complete: {} ({:.2f} MB)",
                filename,
                downloaded / 1024 / 1024,
            )

    except httpx.HTTPError as e:
        logger.error("HTTP error downloading {}: {}", filename, e)
        raise

    except OSError as e:
        logger.error("File error while saving {}: {}", filename, e)
        raise