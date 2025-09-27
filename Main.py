from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import HTTPException
from datetime import datetime
from bs4 import BeautifulSoup

import playsound
import requests
import json
import time
import re
import os

AUDIO = os.path.abspath("resources/athan.mp3")

# Change Masjid_id to your nearest masjid. For example: "al-haram-makkah-saudi-arabia".
MASJID_ID = "your-masjid-id-here"

def fetch_prayer_times_from_mawaqit(masjid_id:str):
    """
    Fetches prayer times from the Mawaqit website for a given masjid ID.
    Original implementation @ 
    https://github.com/mrsofiane/mawaqit-api/blob/main/scraping/script.py#L13
    with a few modifications and readability improvements.
    Parameters:
        masjid_id (str): The unique identifier of the masjid.
    Returns:
        dict: A dictionary containing the prayer times.
    Raises:
        HTTPException: If the masjid is not found or the prayer times cannot be extracted.
    """
    url = f"https://mawaqit.net/fr/{masjid_id}"

    try:
        r = requests.get(url, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch {url}: {e}")

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail=f"{masjid_id} not found")
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error fetching data for {masjid_id}")

    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script", string=re.compile(r"var confData ="))

    if not script:
        raise HTTPException(status_code=500, detail=f"Script containing confData not found for {masjid_id}")

    
    match = re.search(r"var confData = (.*?);", script.string, re.DOTALL)
    if not match:
        raise HTTPException(status_code=500, detail=f"Failed to extract confData JSON for {masjid_id}")

    try:
        conf_data = json.loads(match.group(1))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in confData for {masjid_id}")

    try:
        times = [datetime.strptime(t, "%H:%M").time() for t in conf_data["times"]]
    except (KeyError, ValueError):
        raise HTTPException(status_code=500, detail=f"Invalid times data for {masjid_id}")

    return times


def play_athan() -> None:
    """plays athan from the audio file."""
    playsound.playsound(AUDIO)
    return

def schedule_tasks(scheduler) -> None:
    """Fetch new times and schedule tasks for today."""

    times = fetch_prayer_times_from_mawaqit(MASJID_ID)
    today = datetime.today()

    for t in times:
        run_at = datetime.combine(today, t)
        if run_at > datetime.now():
            scheduler.add_job(play_athan, "date", run_date=run_at)
            print("Scheduled task for", run_at)
    return

def main() -> None:
    """Gonna blame chatgpt if this breaks"""

    scheduler = BackgroundScheduler()
    scheduler.start()

    # Fetch & schedule once at startup
    schedule_tasks(scheduler)
    # Refresh schedule daily at midnight
    scheduler.add_job(schedule_tasks, "cron", hour=0, minute=1, args=[scheduler])

    # keeps the main thread alive,
    # otherwise the script will exit after executing the jobs.
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
    return

if __name__ == "__main__":
    main()


