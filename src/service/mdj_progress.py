import data.mdj_progress as data

from data.mdj_progress import Progress

def webhook(progress: Progress) -> None:
    data.update(progress)