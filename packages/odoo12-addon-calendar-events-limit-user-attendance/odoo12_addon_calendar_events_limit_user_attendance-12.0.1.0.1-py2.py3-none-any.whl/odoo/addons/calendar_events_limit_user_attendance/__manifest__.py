# Copyright 2023-Coopdevs Treball SCCL (<https://coopdevs.org>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Calendar Events Limit User Attendance",
    "version": "12.0.1.0.1",
    "depends": ["calendar"],
    "author": "Coopdevs Treball SCCL",
    "category": "Auth",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Limit attendance from calendar events to partners belonguing to users instead of any partner.
    """,
    "data": ["views/calendar_event.xml"],
    "installable": True,
}
