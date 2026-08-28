# -*- coding: utf-8 -*-
"""
Content model for digitalautonomous.co.uk.

Everything the site says lives here. Nothing in this file may assert a client
result, a metric, a certification or a founder detail that is not verified —
see the CLAIMS RULE in build.py.
"""

SITE = "https://digitalautonomous.co.uk"
EMAIL = "hello@digitalautonomous.co.uk"
BRAND = "Digital Autonomous"
DESCRIPTOR = "AI Automation Solutions"
TAGLINE = "Intelligence · Automation · Acceleration"
FOUNDER = "Sinmi Omotayo"
LOCATION = ""          # left blank: we do not advertise a base of operations

# Optional real details. Leave empty until verified — the templates simply omit
# any that are blank rather than printing a placeholder.
PHONE = ""            # e.g. "+44 20 7946 0000"
LINKEDIN = ""         # e.g. "https://www.linkedin.com/company/digital-autonomous"
LINKEDIN_FOUNDER = ""
COMPANY_NAME = ""     # registered name, if it differs from the trading name
COMPANY_NUMBER = ""   # Companies House number
REGISTERED_OFFICE = ""

LEGAL_UPDATED = "28 August 2026"

# --------------------------------------------------------------------------
# Form delivery
#
# GitHub Pages serves files only — there is no server here to receive a form
# post. FormSubmit relays a submission straight to EMAIL as an ordinary email.
# Its AJAX endpoint answers with JSON, so the page can confirm success in place
# rather than redirecting the visitor away.
#
# Swapping provider is a one-line change: any endpoint that accepts a JSON POST
# and returns 2xx will work (Formspree, Web3Forms, a webhook of your own).
# --------------------------------------------------------------------------
FORM_ENDPOINT = "https://formsubmit.co/ajax/" + EMAIL

# Google Apps Script web app that appends each submission to the leads
# spreadsheet. Paste the deployment URL here — see _src/sheet-logger.gs for the
# script and DEPLOY.md for the five-minute setup. Left blank, forms still work
# and simply do not log a row.
SHEET_ENDPOINT = ""

# --------------------------------------------------------------------------
# "What type of company is this?" — broad enough that nobody has to think hard.
# --------------------------------------------------------------------------
OTHER_OPTION = "Something else"

COMPANY_TYPES = [
    "Dental practice",
    "Healthcare or aesthetics clinic",
    "Home services or trades",
    "Professional services (legal, accounting, consulting)",
    "Property or real estate",
    "Retail or e-commerce",
    "Hospitality or events",
    "Fitness or wellness",
    "Education or training",
    "Financial services or insurance",
    "Marketing or creative agency",
    "Technology or software",
    "Manufacturing or logistics",
    "Automotive",
    "Recruitment or staffing",
    "Construction",
    "Non-profit or public sector",
    OTHER_OPTION,
]


# --------------------------------------------------------------------------
# Icons — 24x24 stroke paths, drawn by icon() in build.py
# --------------------------------------------------------------------------
ICONS = {
    "phone":     '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "phone_miss":'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/><path d="M23 1l-6 6M17 1l6 6"/>',
    "chat":      '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "send":      '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>',
    "refresh":   '<path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M3 21v-5h5"/>',
    "database":  '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "star":      '<path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/>',
    "calendar":  '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>',
    "cog":       '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    "check":     '<path d="M20 6L9 17l-5-5"/>',
    "shield":    '<path d="M12 2l8 4v6c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "lock":      '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "users":     '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
    "alert":     '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "activity":  '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "bell":      '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
    "beaker":    '<path d="M9 3v6L4 19a2 2 0 0 0 1.8 3h12.4A2 2 0 0 0 20 19l-5-10V3"/><path d="M8 3h8M6.5 14h11"/>',
    "list":      '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "scale":     '<path d="M12 3v18M7 21h10"/><path d="M5 7h14"/><path d="M5 7l-3 6a3 3 0 0 0 6 0z"/><path d="M19 7l3 6a3 3 0 0 1-6 0z"/>',
    "archive":   '<rect x="2" y="4" width="20" height="5" rx="1"/><path d="M4 9v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9"/><path d="M10 13h4"/>',
    "clock":     '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "mail":      '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 7l10 6 10-6"/>',
    "search":    '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "map":       '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "trend":     '<path d="M3 3v18h18"/><path d="M7 15l4-5 3 3 5-7"/>',
    "tooth":     '<path d="M12 2c-2.5 0-3 1.2-5 1.2S4 2.6 4 6c0 3.4 1.2 4.4 1.7 7.4C6.2 16.4 6.4 22 8.4 22c1.8 0 1.7-4.6 3.6-4.6s1.8 4.6 3.6 4.6c2 0 2.2-5.6 2.7-8.6C18.8 10.4 20 9.4 20 6c0-3.4-1-2.8-3-2.8S14.5 2 12 2z"/>',
    "heart":     '<path d="M20.8 5.6a5.2 5.2 0 0 0-7.4 0L12 7l-1.4-1.4a5.2 5.2 0 1 0-7.4 7.4L12 21.4l8.8-8.4a5.2 5.2 0 0 0 0-7.4z"/>',
    "home":      '<path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V20a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9.5"/><path d="M9.5 21v-6h5v6"/>',
    "brief":     '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M2 13h20"/>',
    "doc":       '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>',
    "plug":      '<path d="M9 2v6M15 2v6"/><path d="M6 8h12v3a6 6 0 0 1-12 0z"/><path d="M12 17v5"/>',
    "route":     '<circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M9 6h6a3 3 0 0 1 3 3v6"/>',
    "sparkle":   '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 3v3M20.5 4.5h-3M19 18v3M20.5 19.5h-3"/>',
    "target":    '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
    "hand":      '<path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v7M10 10.5V6.5a2 2 0 0 0-4 0V14"/><path d="M6 14a6 6 0 0 0 6 8h1a7 7 0 0 0 7-7v-4a2 2 0 0 0-4 0"/>',
}

# --------------------------------------------------------------------------
# Integrations — only platforms we can realistically connect to.
# "mark" is the initials tile; "bg" its colour.
# --------------------------------------------------------------------------
INTEGRATIONS = [
    ("Gmail",           "M",  "#ea4335"),
    ("Outlook",         "O",  "#0f6cbd"),
    ("Google Calendar", "GC", "#4285f4"),
    ("Microsoft Teams", "T",  "#5b5fc7"),
    ("WhatsApp",        "WA", "#25d366"),
    ("Slack",           "S",  "#e01e5a"),
    ("Calendly",        "C",  "#006bff"),
    ("HubSpot",         "H",  "#ff7a59"),
]

# --------------------------------------------------------------------------
# The problem
# --------------------------------------------------------------------------
PROBLEMS = [
    ("phone_miss", "Missed calls",
     "The phone rings while you are with a customer. Nobody calls back. That "
     "enquiry rings the next company on the list instead."),
    ("clock", "Slow replies",
     "A web form lands at 7pm and gets answered at 10am. By then the "
     "prospect has already booked with whoever replied first."),
    ("refresh", "Forgotten follow-up",
     "One quote goes out, nobody chases it, and a warm lead quietly goes "
     "cold. Most sales need several touches — most businesses manage one."),
    ("list", "Repetitive admin",
     "Copying details into the CRM, sending confirmations, chasing reviews, "
     "rekeying the same data twice. Hours a week, every week."),
]

# --------------------------------------------------------------------------
# Services — the products. Each becomes a card on the homepage and a page.
# --------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "ai-receptionist",
        "nav": "AI Receptionist",
        "title": "AI Receptionist",
        "icon": "phone",
        "blurb": "Answers your calls, handles the questions people always ask, "
                 "qualifies the caller and books them straight into your diary.",
        "result": "<b>Result:</b> every call answered, including evenings, "
                  "weekends and while your team is already on the phone.",
        "nav_sub": "Answer every call, day or night",
        "meta_title": "AI Receptionist for Business Calls | Digital Autonomous",
        "meta_desc": "An AI receptionist that answers your calls 24/7, answers "
                     "common questions, qualifies callers and books appointments "
                     "straight into your calendar. Built and managed for you.",
        "h1": "An AI receptionist that never puts a caller on hold.",
        "lead": "Most missed calls are not lost because nobody cares. They are "
                "lost because everyone is already busy. A voice agent picks up "
                "on the first ring, every time, and turns the call into a "
                "booked appointment.",
        "problem_h": "What it fixes",
        "problem": "A ringing phone with nobody free to answer it is the most "
                   "expensive thing in a small business. The caller rarely "
                   "leaves a voicemail and almost never calls back — they "
                   "simply move down the list of search results.",
        "build": [
            ("Natural voice conversation",
             "The agent speaks, listens and handles interruptions — not a "
             "phone tree of menu options."),
            ("Answers your actual FAQs",
             "Opening hours, pricing bands, location, parking, what to bring, "
             "how long a treatment takes. Written from your own material."),
            ("Qualifies before it books",
             "Asks the questions that separate a real enquiry from a "
             "time-waster, using criteria you set."),
            ("Books into your live calendar",
             "Checks genuine availability, holds the slot, sends the "
             "confirmation and the reminder."),
            ("Hands over to a human on request",
             "If the caller asks for a person, or the agent hits something it "
             "was not built for, it transfers or takes a message and alerts "
             "your team."),
            ("Full transcript of every call",
             "Logged and searchable, so nothing depends on somebody "
             "remembering what was said."),
        ],
        "outcomes": [
            "Calls answered outside opening hours and during busy periods",
            "Fewer enquiries lost to whoever picked up first",
            "Reception time freed for the people actually in the building",
            "A written record of every conversation",
        ],
        "related": ["missed-call-recovery", "appointment-automation", "crm-automation"],
    },
    {
        "slug": "missed-call-recovery",
        "nav": "Missed-Call Recovery",
        "title": "Missed-Call Recovery",
        "icon": "chat",
        "blurb": "Detects a missed call and sends a personalised text within "
                 "seconds, so the conversation carries on instead of ending.",
        "result": "<b>Result:</b> a missed call becomes a text conversation "
                  "instead of a lost customer.",
        "nav_sub": "Turn a missed call into a text thread",
        "meta_title": "Missed Call Text Back Automation | Digital Autonomous",
        "meta_desc": "Automatically detect missed calls and send a personalised "
                     "SMS within seconds, so the enquiry continues by text "
                     "instead of going to a competitor.",
        "h1": "A missed call does not have to be a lost call.",
        "lead": "The moment a call goes unanswered, the caller gets a text from "
                "your number. Most people reply — and a reply is a conversation "
                "you still have a chance of winning.",
        "problem_h": "What it fixes",
        "problem": "Voicemail is close to dead. When a call goes unanswered the "
                   "caller usually hangs up and rings somebody else, and you "
                   "never learn the enquiry existed.",
        "build": [
            ("Instant detection",
             "The system sees the unanswered call the moment it ends — no "
             "waiting for anyone to check a log."),
            ("A text that sounds like you",
             "Apologises for missing them, says who you are, and asks how you "
             "can help. Written in your tone, not a template."),
            ("Two-way conversation",
             "Replies come back into one shared inbox your team can pick up, "
             "or the automation can handle them."),
            ("Qualify and book by text",
             "Where you want it to, the follow-up can collect the details and "
             "offer appointment slots without anyone stepping in."),
            ("Escalation to a human",
             "Anything complicated, unhappy or unusual is flagged to your team "
             "rather than pushed through a script."),
        ],
        "outcomes": [
            "Missed calls turn into replies instead of silence",
            "Out-of-hours callers get an immediate acknowledgement",
            "The enquiry is captured even when nobody can pick up",
            "Every conversation is logged against the contact",
        ],
        "related": ["ai-receptionist", "lead-follow-up-automation", "crm-automation"],
    },
    {
        "slug": "lead-follow-up-automation",
        "nav": "Lead Follow-Up",
        "title": "Lead Follow-Up System",
        "icon": "send",
        "blurb": "Follows up with every new enquiry by SMS and email, on a "
                 "schedule, until they book or tell you to stop.",
        "result": "<b>Result:</b> no enquiry sits unanswered because the "
                  "person who owned it was busy.",
        "nav_sub": "Chase every enquiry, automatically",
        "meta_title": "Automated Lead Follow-Up by SMS and Email | Digital Autonomous",
        "meta_desc": "Automatically follow up new enquiries by SMS and email on "
                     "a schedule you control, so leads are chased consistently "
                     "instead of whenever somebody remembers.",
        "h1": "Follow-up that happens whether anyone remembers or not.",
        "lead": "New enquiries get an immediate reply, then a planned sequence "
                "of nudges across text and email — stopping the second they "
                "respond or book.",
        "problem_h": "What it fixes",
        "problem": "Almost nobody buys off the first message, and almost nobody "
                   "has time to send the fifth. Follow-up is the first thing "
                   "dropped on a busy day, and it is the thing that closes deals.",
        "build": [
            ("Instant first response",
             "Every enquiry gets a reply in seconds, whatever time it arrives."),
            ("A sequence you control",
             "How many touches, how far apart, which channel, what each one "
             "says. Set once, then it runs."),
            ("Stops when it should",
             "A reply, a booking or an opt-out ends the sequence immediately. "
             "Nobody gets chased after they have said yes."),
            ("Routed to the right person",
             "Enquiries are tagged and assigned by service, location or value, "
             "so the right person sees them."),
            ("Answers the obvious questions",
             "Pricing ranges, availability, next steps — handled in the "
             "follow-up rather than waiting for a callback."),
        ],
        "outcomes": [
            "Every enquiry answered in seconds, not the next morning",
            "Consistent follow-up regardless of who is in that day",
            "Fewer leads lost between the enquiry and the appointment",
            "Sales conversations start warmer",
        ],
        "related": ["lead-reactivation", "appointment-automation", "crm-automation"],
    },
    {
        "slug": "lead-reactivation",
        "nav": "Lead Reactivation",
        "title": "Lead Reactivation",
        "icon": "refresh",
        "blurb": "Reconnects with the old enquiries and past customers already "
                 "sitting in your CRM, so you sell to a list you already own.",
        "result": "<b>Result:</b> revenue from contacts you have already paid "
                  "to acquire.",
        "nav_sub": "Sell to the list you already own",
        "meta_title": "Database Reactivation Campaigns | Digital Autonomous",
        "meta_desc": "Reactivate old leads and past customers sitting in your "
                     "CRM with a compliant, personalised campaign — revenue from "
                     "contacts you have already paid to acquire.",
        "h1": "The cheapest leads you will ever get are already in your CRM.",
        "lead": "Old enquiries that never converted and customers who have not "
                "been back are the least expensive pipeline in the business. A "
                "reactivation campaign works that list properly.",
        "problem_h": "What it fixes",
        "problem": "Most businesses spend heavily to generate enquiries, work "
                   "them for a fortnight, then leave them in the CRM for good. "
                   "That list is already paid for and mostly untouched.",
        "build": [
            ("Segment the database",
             "Split by service, value, how long ago and how far they got, so "
             "the message is relevant rather than a blast."),
            ("Personalised outreach",
             "References what they originally enquired about — not a generic "
             "marketing email."),
            ("Consent handled properly",
             "Suppression lists, opt-outs and lawful basis are checked before "
             "anything sends. Unsubscribes are honoured immediately."),
            ("Replies handled automatically",
             "Interested responses are qualified and booked; the rest are "
             "tagged and set aside."),
            ("Measured per segment",
             "You see which segments responded, so the next campaign is aimed "
             "at what worked."),
        ],
        "outcomes": [
            "Dormant contacts turned back into conversations",
            "Pipeline that costs nothing extra in ad spend",
            "A cleaner, correctly segmented database afterwards",
            "A repeatable campaign you can run again",
        ],
        "related": ["lead-follow-up-automation", "crm-automation", "review-automation"],
    },
    {
        "slug": "crm-automation",
        "nav": "CRM Automation",
        "title": "CRM Automation",
        "icon": "database",
        "blurb": "Creates contacts, moves pipeline stages, logs conversations "
                 "and fires the next action — without anyone typing it in.",
        "result": "<b>Result:</b> a CRM that is actually accurate, without "
                  "anyone maintaining it.",
        "nav_sub": "A CRM that updates itself",
        "meta_title": "CRM Automation and Integration | Digital Autonomous",
        "meta_desc": "Automatically create contacts, update pipeline stages, log "
                     "conversations and trigger the next action in your CRM — "
                     "HubSpot, Salesforce, GoHighLevel and more.",
        "h1": "Your CRM should update itself.",
        "lead": "Every call, form, text and booking writes itself to the right "
                "record, moves the deal to the right stage and triggers "
                "whatever comes next.",
        "problem_h": "What it fixes",
        "problem": "A CRM nobody updates is worse than no CRM: it produces "
                   "confident reports built on stale data. Manual entry is the "
                   "first thing to slip when the day gets busy.",
        "build": [
            ("Contacts created from any source",
             "Web forms, phone calls, WhatsApp, email and chat all land as "
             "properly formed records."),
            ("Deduplication",
             "Matches on phone and email before creating, so one person does "
             "not become four records."),
            ("Pipeline kept current",
             "Stages move on real events — booked, attended, quoted, won — "
             "not on somebody remembering to drag a card."),
            ("Every conversation logged",
             "Call transcripts, texts and emails attached to the contact."),
            ("Actions triggered automatically",
             "Tasks assigned, notifications sent, documents generated, the "
             "next sequence started."),
            ("Reporting you can trust",
             "Because the underlying data is written by the system rather "
             "than typed in later."),
        ],
        "outcomes": [
            "Admin time returned to the team",
            "Records accurate enough to make decisions on",
            "Nothing sitting in an inbox instead of the pipeline",
            "Handovers that do not depend on one person's memory",
        ],
        "related": ["lead-follow-up-automation", "operations-automation", "appointment-automation"],
    },
    {
        "slug": "review-automation",
        "nav": "Review Automation",
        "title": "Review Automation",
        "icon": "star",
        "blurb": "Asks happy customers for a review at the right moment, and "
                 "routes unhappy ones to you first.",
        "result": "<b>Result:</b> steadier review flow without anyone having "
                  "to ask face to face.",
        "nav_sub": "Ask at the right moment, every time",
        "meta_title": "Automated Review Requests | Digital Autonomous",
        "meta_desc": "Automatically request reviews from satisfied customers at "
                     "the right moment, with unhappy feedback routed to you "
                     "privately first.",
        "h1": "Reviews, asked for consistently instead of occasionally.",
        "lead": "The request goes out when the customer is most likely to say "
                "yes — just after the job is finished or the appointment "
                "attended — through the channel they actually read.",
        "problem_h": "What it fixes",
        "problem": "Everyone knows reviews matter and almost nobody asks "
                   "consistently. Asking is awkward in person and forgotten "
                   "afterwards, so review counts stall.",
        "build": [
            ("Triggered by the real event",
             "Fires on job completed, appointment attended or invoice paid — "
             "not on a date guess."),
            ("Sensible timing and limits",
             "Waits an appropriate interval, never asks the same person twice, "
             "respects quiet hours."),
            ("Feedback gate first",
             "Unhappy customers are routed to you privately so the problem "
             "gets fixed rather than posted."),
            ("Direct link to the platform",
             "One tap to Google or wherever you want reviews, with no hunting "
             "for the page."),
            ("Polite single reminder",
             "One nudge if there is no response, then it stops."),
        ],
        "outcomes": [
            "Requests actually get sent, every time",
            "Problems surface to you before they surface publicly",
            "No awkward in-person asking",
            "A record of who was asked and when",
        ],
        "related": ["appointment-automation", "crm-automation", "lead-reactivation"],
    },
    {
        "slug": "appointment-automation",
        "nav": "Appointment Automation",
        "title": "Appointment Automation",
        "icon": "calendar",
        "blurb": "Books appointments against real availability, confirms them "
                 "and handles reminders, rescheduling and cancellations.",
        "result": "<b>Result:</b> a fuller diary with less back-and-forth and "
                  "fewer no-shows.",
        "nav_sub": "Booking, confirmations and reminders",
        "meta_title": "Appointment Booking Automation | Digital Autonomous",
        "meta_desc": "Automated appointment booking against live calendar "
                     "availability, with confirmations, reminders, rescheduling "
                     "and cancellation handling.",
        "h1": "Booking, confirming and reminding — handled end to end.",
        "lead": "From the first enquiry to the reminder the night before, the "
                "whole booking loop runs itself against your real calendar.",
        "problem_h": "What it fixes",
        "problem": "Booking by phone tag wastes a remarkable amount of time, "
                   "and appointments nobody reminded turn into empty slots that "
                   "cannot be resold.",
        "build": [
            ("Real availability, not a guess",
             "Reads your live calendar, honours buffers, working hours, "
             "resource and staff rules."),
            ("Booked in the conversation",
             "The slot is offered and taken during the call or the text thread, "
             "while intent is highest."),
            ("Confirmations immediately",
             "Sent by the channel the customer used, with everything they need "
             "to turn up in the right place."),
            ("Reminders on a schedule",
             "Timed to your service — the day before, the morning of, whatever "
             "reduces no-shows for you."),
            ("Self-service reschedule and cancel",
             "One link. Cancellations free the slot automatically so it can be "
             "filled again."),
        ],
        "outcomes": [
            "Less phone tag to arrange a single appointment",
            "Fewer forgotten appointments",
            "Cancelled slots released instead of sitting empty",
            "Bookings taken outside office hours",
        ],
        "related": ["ai-receptionist", "crm-automation", "review-automation"],
    },
    {
        "slug": "operations-automation",
        "nav": "Custom Operations",
        "title": "Custom Operations Automation",
        "icon": "cog",
        "blurb": "Automates the repetitive internal work — reporting, "
                 "notifications, data entry and handoffs between systems.",
        "result": "<b>Result:</b> hours returned to your team every week, "
                  "reliably.",
        "nav_sub": "Automate the internal grind",
        "meta_title": "Custom Business Process Automation | Digital Autonomous",
        "meta_desc": "Automate repetitive internal processes: reporting, "
                     "notifications, data entry, document generation and handoffs "
                     "between the systems you already use.",
        "h1": "If it is repetitive and rules-based, it can run itself.",
        "lead": "The work that eats the week and appears on nobody's job "
                "description: rekeying data, assembling the same report, "
                "chasing the same approvals, moving records between systems "
                "that do not talk.",
        "problem_h": "What it fixes",
        "problem": "Every business runs on a handful of manual processes that "
                   "exist only because two systems never got connected. They "
                   "are invisible on the org chart and expensive in practice.",
        "build": [
            ("Process mapped first",
             "We watch how the job is actually done, including the exceptions, "
             "before automating anything."),
            ("Systems connected",
             "Whatever you run — CRM, spreadsheets, accounting, forms, email, "
             "storage — joined so data moves once."),
            ("Documents generated",
             "Quotes, contracts, invoices, onboarding packs produced from real "
             "record data."),
            ("Reports built and delivered",
             "Assembled on a schedule and sent to whoever needs them, without "
             "the spreadsheet ritual."),
            ("Alerts that matter",
             "The team is notified when something needs a human, and not "
             "otherwise."),
            ("Monitored in production",
             "Failures raise an alert to us, not a silence that lasts a "
             "fortnight."),
        ],
        "outcomes": [
            "Repetitive tasks removed rather than reassigned",
            "The same data entered once instead of three times",
            "Reporting that arrives without being chased",
            "Processes that survive somebody being on holiday",
        ],
        "related": ["crm-automation", "ai-receptionist", "lead-follow-up-automation"],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# --------------------------------------------------------------------------
# Industries
# --------------------------------------------------------------------------
INDUSTRIES = [
    {
        "slug": "dentists",
        "icon": "tooth",
        "nav": "Private Dental Clinics",
        "title": "Private Dental Clinics",
        "blurb": "High-value enquiries arrive while reception is with a patient. "
                 "Implant and Invisalign leads need answering the same day, and "
                 "consultations need chasing until they are in the diary.",
        "chips": ["Missed calls", "Implant enquiries", "Invisalign leads",
                  "Consultation booking", "Recall &amp; follow-up"],
        "meta_title": "Automation for Private Dental Clinics | Digital Autonomous",
        "meta_desc": "AI call answering, missed-call recovery and consultation "
                     "follow-up for private dental practices — so implant and "
                     "Invisalign enquiries are not lost at reception.",
        "h1": "Automation for private dental clinics.",
        "lead": "A single implant or Invisalign enquiry is worth thousands. It "
                "usually arrives by phone, during clinic hours, when reception "
                "is already with a patient.",
        "pains": [
            ("Calls missed during clinic",
             "Reception is checking a patient in and the phone rings out. A "
             "high-value enquiry rings the practice down the road instead."),
            ("Treatment enquiries that go cold",
             "Someone asks about implants, gets a price, and is never "
             "contacted again. The decision takes weeks — the follow-up lasts "
             "one email."),
            ("Consultations that no-show",
             "Free consultation slots are easy to book and easy to forget, and "
             "an empty chair cannot be resold at short notice."),
            ("Recall lists nobody works",
             "Patients overdue a check-up or a hygiene visit sit in the system "
             "while the practice buys new patients instead."),
        ],
        "stack": ["ai-receptionist", "missed-call-recovery",
                  "lead-follow-up-automation", "appointment-automation",
                  "lead-reactivation", "review-automation"],
    },
    {
        "slug": "aesthetics",
        "icon": "heart",
        "nav": "Healthcare & Aesthetics",
        "title": "Healthcare &amp; Aesthetics",
        "blurb": "Clinics, aesthetics and private healthcare where enquiries "
                 "come in at all hours, consultations need qualifying, and "
                 "patient communication has to be handled carefully.",
        "chips": ["Out-of-hours enquiries", "Consultation qualifying",
                  "Treatment follow-up", "Rebooking", "Reminders"],
        "meta_title": "Automation for Aesthetics Clinics | Digital Autonomous",
        "meta_desc": "Enquiry handling, consultation booking and follow-up "
                     "automation for aesthetics and private healthcare clinics, "
                     "built with confidentiality in mind.",
        "h1": "Automation for healthcare and aesthetics clinics.",
        "lead": "Enquiries arrive in the evening, on Instagram, and from people "
                "comparing three clinics at once. Whoever replies first and "
                "answers properly usually gets the consultation.",
        "pains": [
            ("Evening and weekend enquiries",
             "Most people research treatments outside working hours. A reply "
             "the next morning arrives after they have booked elsewhere."),
            ("Consultations that are not qualified",
             "Diary time goes to people who were never suitable or never "
             "intended to proceed."),
            ("Treatment courses that lapse",
             "Multi-session treatments need rebooking, and the rebooking is "
             "what gets forgotten."),
            ("Sensitive information handled ad hoc",
             "Patient details end up in personal inboxes and message threads "
             "with no record and no control."),
        ],
        "stack": ["ai-receptionist", "lead-follow-up-automation",
                  "appointment-automation", "crm-automation", "review-automation"],
    },
    {
        "slug": "home-services",
        "icon": "home",
        "nav": "Home Services",
        "title": "Home Services",
        "blurb": "Trades and home services where the team is on site all day, "
                 "the phone rings constantly, and quotes go out and never get "
                 "chased.",
        "chips": ["On-site missed calls", "Emergency enquiries", "Quote follow-up",
                  "Job scheduling", "Review requests"],
        "meta_title": "Automation for Home Service Businesses | Digital Autonomous",
        "meta_desc": "Missed-call text back, quote follow-up and job scheduling "
                     "automation for trades and home service businesses whose "
                     "team is on site all day.",
        "h1": "Automation for trades and home services.",
        "lead": "You cannot answer the phone from under a sink or up a ladder. "
                "Every unanswered ring is a job going to whoever picked up.",
        "pains": [
            ("The phone rings while you are working",
             "Hands are full, the call goes unanswered, and the customer "
             "rings the next number on the search results."),
            ("Emergency jobs go to the fastest responder",
             "For a leak or a breakdown nobody waits. The first firm to answer "
             "wins the job at the price they quote."),
            ("Quotes sent and never chased",
             "The quote goes out, and that is the last contact. A single "
             "follow-up would win a share of them."),
            ("Admin at the end of a long day",
             "Invoicing, scheduling and review requests happen at 9pm, badly, "
             "or not at all."),
        ],
        "stack": ["missed-call-recovery", "lead-follow-up-automation",
                  "appointment-automation", "review-automation", "operations-automation"],
    },
    {
        "slug": "professional-services",
        "icon": "brief",
        "nav": "Professional Services",
        "title": "Professional Services",
        "blurb": "Firms where fee earners are the bottleneck: enquiries need "
                 "qualifying before they reach a partner, and onboarding is a "
                 "pile of repetitive admin.",
        "chips": ["Enquiry qualifying", "Intake forms", "Client onboarding",
                  "Document generation", "Deadline reminders"],
        "meta_title": "Automation for Professional Services Firms | Digital Autonomous",
        "meta_desc": "Enquiry qualification, client intake and onboarding "
                     "automation for accountants, solicitors, consultants and "
                     "other professional services firms.",
        "h1": "Automation for professional services firms.",
        "lead": "The scarcest resource is fee-earner time, and a surprising "
                "amount of it goes on qualifying enquiries and re-entering "
                "information the client already gave you.",
        "pains": [
            ("Unqualified enquiries reaching senior people",
             "Partners spend chargeable time on calls that were never going to "
             "become instructions."),
            ("Intake collected by email tennis",
             "Details arrive across a dozen messages and get rekeyed into the "
             "practice system by hand."),
            ("Onboarding that takes a week",
             "Engagement letters, ID checks and welcome packs assembled "
             "manually every single time."),
            ("Deadlines tracked in someone's head",
             "Filing dates and review points depend on one person remembering "
             "to look."),
        ],
        "stack": ["lead-follow-up-automation", "crm-automation",
                  "operations-automation", "appointment-automation"],
    },
]

INDUSTRY_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}

# --------------------------------------------------------------------------
# How it works
# --------------------------------------------------------------------------
PROCESS = [
    ("Audit", "We map where enquiries are lost and where time goes, then show "
              "you what is worth automating first and what is not."),
    ("Design", "We agree exactly what the system will do, what it will never "
               "do, and where it hands over to a person."),
    ("Build", "We build it around the tools you already pay for. No migration, "
              "no new platform for your team to learn."),
    ("Deploy", "We test against your real workflows and edge cases before a "
               "single customer touches it, then launch."),
    ("Optimise", "We monitor it in production, fix what breaks and refine what "
                 "works, as an ongoing service."),
]

# --------------------------------------------------------------------------
# Security and reliability
# --------------------------------------------------------------------------
SECURITY = [
    ("lock", "Secure credential handling",
     "API keys and passwords live in an encrypted credential store or a "
     "password manager. They are never pasted into documents, code or chat."),
    ("users", "Access controls",
     "Least-privilege access to your systems. Each integration gets only the "
     "permissions it genuinely needs, and access is revocable at any time."),
    ("hand", "Human escalation",
     "Every automation has a defined point where it stops and hands over to a "
     "person — on request, on uncertainty, or on anything sensitive."),
    ("alert", "Error handling",
     "Failures are caught and handled explicitly. A step that cannot complete "
     "raises an error rather than silently doing nothing."),
    ("activity", "Automation monitoring",
     "Runs are monitored in production. We see failure rates rather than "
     "waiting to hear that something stopped working."),
    ("bell", "Failure notifications",
     "When something breaks, an alert reaches us and, where you want it, you. "
     "Nothing fails quietly."),
    ("beaker", "Tested before deployment",
     "Every workflow is tested against real scenarios and edge cases before it "
     "is allowed near a customer."),
    ("doc", "Conversation and activity logging",
     "Calls, messages and automated actions are logged so there is always a "
     "record of what the system did and why."),
    ("shield", "GDPR-conscious implementation",
     "Data minimisation, defined retention, honoured opt-outs and lawful basis "
     "considered when we design the flow — not bolted on afterwards."),
    ("scale", "Your data stays yours",
     "Accounts, data and customer relationships remain in your name. You can "
     "export your data at any time."),
    ("archive", "Backups and recovery",
     "Workflow configurations are version controlled, so a broken change can "
     "be rolled back rather than rebuilt."),
]

# --------------------------------------------------------------------------
# Free automation audit
# --------------------------------------------------------------------------
AUDIT_STEPS = [
    "Where leads are currently being lost",
    "Which repetitive processes can be automated",
    "Which of your existing systems should be connected",
    "Where staff time is being wasted",
    "Which automation should be implemented first",
]

# --------------------------------------------------------------------------
# FAQ
# --------------------------------------------------------------------------
FAQ = [
    ("What can Digital Autonomous automate?",
     "Anything repetitive and rules-based that touches your enquiries, your "
     "customers or your admin: answering calls, replying to enquiries, "
     "qualifying leads, booking appointments, following up, updating your CRM, "
     "requesting reviews, generating documents and moving data between "
     "systems. If a person does it the same way every time, it is a candidate."),
    ("How long does implementation take?",
     "It depends on how much is being built and how many systems are involved. "
     "A single automation goes live quickly; a larger build takes longer, "
     "because it is tested properly before it speaks to your customers. You get "
     "a realistic timeline for your specific build during the audit."),
    ("Do I need to replace my current software?",
     "No. We build around what you already use. Replacing working systems is "
     "expensive, slow and usually unnecessary — the problem is almost always "
     "that your tools are not connected, not that they are the wrong tools."),
]

# --------------------------------------------------------------------------
# Dialling codes. Common destinations first, then alphabetical.
# --------------------------------------------------------------------------
DIAL_CODES = [
    ("United Kingdom", "+44"),
    ("United States", "+1"),
    ("Ireland", "+353"),
    ("Canada", "+1"),
    ("Australia", "+61"),
    ("United Arab Emirates", "+971"),
    ("Germany", "+49"),
    ("France", "+33"),
    ("Netherlands", "+31"),
    ("Spain", "+34"),
    ("Afghanistan", "+93"),
    ("Albania", "+355"),
    ("Algeria", "+213"),
    ("Andorra", "+376"),
    ("Angola", "+244"),
    ("Antigua and Barbuda", "+1268"),
    ("Argentina", "+54"),
    ("Armenia", "+374"),
    ("Aruba", "+297"),
    ("Austria", "+43"),
    ("Azerbaijan", "+994"),
    ("Bahamas", "+1242"),
    ("Bahrain", "+973"),
    ("Bangladesh", "+880"),
    ("Barbados", "+1246"),
    ("Belarus", "+375"),
    ("Belgium", "+32"),
    ("Belize", "+501"),
    ("Benin", "+229"),
    ("Bermuda", "+1441"),
    ("Bhutan", "+975"),
    ("Bolivia", "+591"),
    ("Bosnia and Herzegovina", "+387"),
    ("Botswana", "+267"),
    ("Brazil", "+55"),
    ("Brunei", "+673"),
    ("Bulgaria", "+359"),
    ("Burkina Faso", "+226"),
    ("Burundi", "+257"),
    ("Cambodia", "+855"),
    ("Cameroon", "+237"),
    ("Cape Verde", "+238"),
    ("Cayman Islands", "+1345"),
    ("Central African Republic", "+236"),
    ("Chad", "+235"),
    ("Chile", "+56"),
    ("China", "+86"),
    ("Colombia", "+57"),
    ("Comoros", "+269"),
    ("Congo", "+242"),
    ("Congo (DRC)", "+243"),
    ("Costa Rica", "+506"),
    ("Croatia", "+385"),
    ("Cuba", "+53"),
    ("Cyprus", "+357"),
    ("Czechia", "+420"),
    ("Denmark", "+45"),
    ("Djibouti", "+253"),
    ("Dominica", "+1767"),
    ("Dominican Republic", "+1809"),
    ("Ecuador", "+593"),
    ("Egypt", "+20"),
    ("El Salvador", "+503"),
    ("Equatorial Guinea", "+240"),
    ("Eritrea", "+291"),
    ("Estonia", "+372"),
    ("Eswatini", "+268"),
    ("Ethiopia", "+251"),
    ("Fiji", "+679"),
    ("Finland", "+358"),
    ("Gabon", "+241"),
    ("Gambia", "+220"),
    ("Georgia", "+995"),
    ("Ghana", "+233"),
    ("Gibraltar", "+350"),
    ("Greece", "+30"),
    ("Greenland", "+299"),
    ("Grenada", "+1473"),
    ("Guatemala", "+502"),
    ("Guinea", "+224"),
    ("Guyana", "+592"),
    ("Haiti", "+509"),
    ("Honduras", "+504"),
    ("Hong Kong", "+852"),
    ("Hungary", "+36"),
    ("Iceland", "+354"),
    ("India", "+91"),
    ("Indonesia", "+62"),
    ("Iran", "+98"),
    ("Iraq", "+964"),
    ("Israel", "+972"),
    ("Italy", "+39"),
    ("Ivory Coast", "+225"),
    ("Jamaica", "+1876"),
    ("Japan", "+81"),
    ("Jordan", "+962"),
    ("Kazakhstan", "+7"),
    ("Kenya", "+254"),
    ("Kuwait", "+965"),
    ("Kyrgyzstan", "+996"),
    ("Laos", "+856"),
    ("Latvia", "+371"),
    ("Lebanon", "+961"),
    ("Lesotho", "+266"),
    ("Liberia", "+231"),
    ("Libya", "+218"),
    ("Liechtenstein", "+423"),
    ("Lithuania", "+370"),
    ("Luxembourg", "+352"),
    ("Macau", "+853"),
    ("Madagascar", "+261"),
    ("Malawi", "+265"),
    ("Malaysia", "+60"),
    ("Maldives", "+960"),
    ("Mali", "+223"),
    ("Malta", "+356"),
    ("Mauritania", "+222"),
    ("Mauritius", "+230"),
    ("Mexico", "+52"),
    ("Moldova", "+373"),
    ("Monaco", "+377"),
    ("Mongolia", "+976"),
    ("Montenegro", "+382"),
    ("Morocco", "+212"),
    ("Mozambique", "+258"),
    ("Myanmar", "+95"),
    ("Namibia", "+264"),
    ("Nepal", "+977"),
    ("New Zealand", "+64"),
    ("Nicaragua", "+505"),
    ("Niger", "+227"),
    ("Nigeria", "+234"),
    ("North Macedonia", "+389"),
    ("Norway", "+47"),
    ("Oman", "+968"),
    ("Pakistan", "+92"),
    ("Palestine", "+970"),
    ("Panama", "+507"),
    ("Papua New Guinea", "+675"),
    ("Paraguay", "+595"),
    ("Peru", "+51"),
    ("Philippines", "+63"),
    ("Poland", "+48"),
    ("Portugal", "+351"),
    ("Puerto Rico", "+1787"),
    ("Qatar", "+974"),
    ("Romania", "+40"),
    ("Russia", "+7"),
    ("Rwanda", "+250"),
    ("Saint Lucia", "+1758"),
    ("Samoa", "+685"),
    ("San Marino", "+378"),
    ("Saudi Arabia", "+966"),
    ("Senegal", "+221"),
    ("Serbia", "+381"),
    ("Seychelles", "+248"),
    ("Sierra Leone", "+232"),
    ("Singapore", "+65"),
    ("Slovakia", "+421"),
    ("Slovenia", "+386"),
    ("Somalia", "+252"),
    ("South Africa", "+27"),
    ("South Korea", "+82"),
    ("South Sudan", "+211"),
    ("Sri Lanka", "+94"),
    ("Sudan", "+249"),
    ("Suriname", "+597"),
    ("Sweden", "+46"),
    ("Switzerland", "+41"),
    ("Syria", "+963"),
    ("Taiwan", "+886"),
    ("Tajikistan", "+992"),
    ("Tanzania", "+255"),
    ("Thailand", "+66"),
    ("Togo", "+228"),
    ("Trinidad and Tobago", "+1868"),
    ("Tunisia", "+216"),
    ("Turkey", "+90"),
    ("Turkmenistan", "+993"),
    ("Uganda", "+256"),
    ("Ukraine", "+380"),
    ("Uruguay", "+598"),
    ("Uzbekistan", "+998"),
    ("Venezuela", "+58"),
    ("Vietnam", "+84"),
    ("Yemen", "+967"),
    ("Zambia", "+260"),
    ("Zimbabwe", "+263"),
]
DIAL_DIVIDER = 10   # entries before the alphabetical run
