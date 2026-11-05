import rio

from ui.journal_page import JournalPage


app = rio.App(
    pages=[
        rio.ComponentPage(
            "Journal",
            "",
            JournalPage,
        ),
    ],
)