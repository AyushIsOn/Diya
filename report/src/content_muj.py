"""Report text, arranged in the chapter structure of the MUJ industrial-training template."""

META = {
    "report_type": "An Industrial Training Report",
    "title": "DIYA: DESIGN AND DEVELOPMENT OF AN UNATTENDED MEDITATION KIOSK",
    "subject": "[[Subject Code]]",
    "student": "Ayush Gupta",
    "regno": "23FE10CDS00349",
    "department": "Department of Data Science and Engineering",
    "month": "October 2026",
}


class B:
    """Collects content blocks in order."""

    def __init__(self):
        self.blocks = []
        self.ch = 0
        self.sec = 0
        self.first_in_chapter = False

    def add(self, kind, **kw):
        kw["kind"] = kind
        self.blocks.append(kw)

    # structure
    def front(self, title, key):
        self.add("front", title=title, key=key)

    def chapter(self, title):
        self.ch += 1
        self.sec = 0
        self.first_in_chapter = True
        self.add("chapter", title=title, num=self.ch)

    def section(self, title, toc_title=None):
        self.sec += 1
        num = f"{self.ch}.{self.sec}"
        self.add("section", num=num, title=title, toc_title=toc_title or title,
                 newpage=not self.first_in_chapter)
        self.first_in_chapter = False

    def unnumbered(self, title):
        self.add("unnumbered", title=title)

    # content
    def sub(self, t):
        self.add("sub", text=t)

    def p(self, t):
        self.add("para", text=" ".join(t.split()))

    def bullets(self, items, level=0):
        self.add("bullets", items=[" ".join(i.split()) for i in items], level=level)

    def numbered(self, items):
        self.add("numbered", items=[" ".join(i.split()) for i in items])

    def fig(self, path, caption, width=6.3):
        self.add("figure", path=path, caption=caption, width=width)

    def figrow(self, items, caption, height=3.4):
        self.add("figrow", items=items, caption=caption, height=height)

    def placeholder(self, caption, hint, height=3.2):
        self.add("placeholder", caption=caption, hint=hint, height=height)

    def table(self, caption, header, rows, widths):
        self.add("table", caption=caption, header=header, rows=rows, widths=widths)

    def code(self, t):
        self.add("code", text=t.strip("\n"))

    def raw(self, kind, **kw):
        self.add(kind, **kw)


def build():
    r = B()

    r.raw("cover", meta=META)
    r.raw("certificate", path="images/iith-certificate.jpg")

    # ------------------------------------------------------------ front matter
    r.front("ACKNOWLEDGMENTS", "ack")
    r.p("""I would like to express my heartfelt gratitude to **Dr. Prasad S. Onkar**, Associate Professor,
    Department of Design, Indian Institute of Technology Hyderabad, for giving me the opportunity to work
    at the INDReA Lab and for his supervision and encouragement throughout my internship from 1 June 2026
    to 31 July 2026.""")
    r.p("""I am deeply thankful to **Mr. Eshwar Teja**, under whose day-to-day guidance this project was carried
    out. His design discussions, his testing of every build on the real kiosk and his patience while the
    system was taking shape were instrumental in the successful completion of my work. I also thank
    **Kalyan Sir** for his support and valuable feedback, and the members of the hardware and
    computer-vision team for their cooperation in defining clear interfaces between our parts of the
    system.""")
    r.p("""I sincerely thank my faculty guide, **[[Faculty guide name]]**, and the Department of Data Science and
    Engineering, School of Computer Science and Engineering, **Manipal University Jaipur**, for their
    guidance and for providing me with the opportunity to undertake this industrial training.""")
    r.p("""Finally, I am grateful to my family and friends for their constant encouragement and support
    throughout the internship.""")

    r.front("ABSTRACT", "abstract")
    r.p("""*Diya* is an unattended meditation kiosk developed at the INDReA Lab, Department of Design, IIT
    Hyderabad, and named after the traditional Indian oil lamp. A visitor walks up to the kiosk, is
    identified, is aligned to a set of cameras by a motorised rig, sits through a guided meditation while
    thermal, depth, gaze and posture data are captured, and receives a personalised report on screen. The
    machine then resets itself for the next person without any operator.""")
    r.p("""During this eight-week internship I designed and built the software side of the kiosk: a full-screen
    desktop application in C# on .NET 8 with the Avalonia UI framework for Ubuntu (GNOME on Wayland); a
    Node.js/Express and PostgreSQL backend hosted on Render; phone-facing web pages for registration,
    roster administration and login; an integration layer that runs the hardware team’s calibration and
    meditation pipeline and displays the PDF report it produces; and packaging that ships the kiosk as a
    self-contained Debian package that starts on boot and restarts after a crash.""")
    r.p("""The key design decision was to **invert the usual QR-code flow**. The kiosk had no scanner, so the
    kiosk displays a short-lived session QR code and the visitor’s own phone scans it through a private,
    per-person login link. This removed a hardware dependency, needed no app installation and made the
    scan a proof of who arrived. A second decision was to integrate with the hardware team through a
    process and a file on disk rather than an API, which let both teams work independently.""")
    r.p("""The system went through seven released versions (v1.0 to v1.6) and was demonstrated end to end with a
    real phone scanning the kiosk. The report also discusses the problems faced, in particular the window
    restrictions of Wayland, and the remaining work: a consent screen, an inactivity reset, continuous
    integration and replacing the placeholder calibration scripts with the hardware team’s real stages.""")

    r.raw("lof")
    r.raw("lot")
    r.raw("contents")

    r.front("List of Abbreviations", "abbr")
    r.table(None, ["Abbreviation", "Full Form"], [
        ["API", "Application Programming Interface"], ["CI", "Continuous Integration"],
        ["CV", "Computer Vision"], [".deb", "Debian software package"],
        ["GNOME", "GNU Network Object Model Environment (Linux desktop)"],
        ["HTTPS", "Hypertext Transfer Protocol Secure"], ["IITH", "Indian Institute of Technology Hyderabad"],
        ["INDReA", "Interaction Design Research Lab (IITH Department of Design)"],
        ["JSON", "JavaScript Object Notation"], ["LTS", "Long-Term Support"],
        ["PDF", "Portable Document Format"], ["PR", "Pull Request"],
        ["QR", "Quick Response code"], ["REST", "Representational State Transfer"],
        ["SQL", "Structured Query Language"], ["UI / UX", "User Interface / User Experience"],
        ["V4L2", "Video4Linux version 2"], ["XLSX", "Office Open XML spreadsheet (Excel)"],
    ], [1.8, 5.0])

    # ------------------------------------------------------------ chapter 1
    r.chapter("INTRODUCTION")
    r.section("Introduction to work done/ Motivation (*Overview, Applications & Advantages*)",
              "Introduction to work done/ Motivation (Overview, Applications & Advantages)")
    r.p("""The internship was carried out at the **INDReA Lab, Department of Design, Indian Institute of
    Technology Hyderabad**, under the supervision of Dr. Prasad S. Onkar, from 1 June 2026 to 31 July 2026.
    The lab was developing *Diya*, a meditation kiosk inspired by the traditional Indian lamp, and I joined
    the project to build its software.""")
    r.p("""**Overview:** The Diya kiosk is an installation meant for a public, museum-like space. A visitor walks
    up, is identified, and is guided through a short meditation. During the session several cameras observe
    the person (a webcam for face and gaze, a depth camera, a posture camera and a thermal camera), and a
    motorised rig first aligns these sensors to the visitor’s chest and eyes. At the end, a report of the
    session is shown on screen and the kiosk returns to its welcome screen, ready for the next visitor,
    with no attendant.""")
    r.p("""My work covered the complete software path that a visitor experiences: the full-screen kiosk
    application, the visitor identification system (backend, database and phone web pages), the layer that
    launches the hardware team’s pipeline and shows its report, and the packaging and deployment of the
    kiosk. The camera and motor control scripts and the meditation application were built by a collaborating
    hardware and computer-vision team (Table 1).""")
    r.table("Division of responsibilities", ["Party", "Owns", "Interface to the kiosk app"], [
        ["Me (this internship)", "Kiosk desktop app, backend API and database, web pages for registration, "
         "admin and login, pipeline launcher, report display, packaging", "—"],
        ["Hardware / CV team", "Camera calibration and motor scripts (HOME, SHOOT, CHEST, EYE) and the "
         "`meditation-app` that runs the session and writes the PDF report",
         "Script `run1.sh` and the folder `/opt/meditation-app/data`"],
        ["Lab / supervisors", "Concept, experience design, hardware rig, testing on the real kiosk",
         "Requirements and review"],
    ], [1.5, 3.5, 2.0])
    r.p("""**Motivation:** An unattended kiosk has to do on its own what an attendant would normally do: greet
    the visitor, find out who they are, start the right process, recover when something fails and get ready
    for the next person. For Diya this had to work on a Linux machine with several cameras attached,
    alongside software written by another team, and without a QR scanner or keyboard for the visitor.""")
    r.p("""**Applications:** The same software pattern applies to museum and exhibition installations, wellness
    and meditation booths, self-service health check-up kiosks, and any setting where a person must be
    identified at a shared screen and a local hardware process must then run for them.""")
    r.p("""**Advantages:** Identification needs nothing but the visitor’s own phone; the kiosk recovers from
    crashes by itself and installs on a fresh machine with one command; and the clean boundary with the
    hardware software allows the two teams to change their internals independently.""")

    r.section("Project Statement / Objectives of the Project")
    r.p("""**Project statement:** *To design and build reliable, self-recovering kiosk software that identifies a
    visitor without dedicated hardware, runs the hardware team’s calibration and meditation pipeline, shows
    the resulting report and resets automatically for the next visitor, while remaining easy to install and
    update on the kiosk machine.*""")
    r.p("The objectives of the project were:")
    r.numbered([
        "**Kiosk application:** a full-screen application for Ubuntu (GNOME on Wayland) that starts on boot "
        "and restarts itself after a crash.",
        "**Visitor identification:** a method that needs no scanner or keyboard at the kiosk.",
        "**Backend and web pages:** visitor registration, roster upload by an administrator and phone-based "
        "login.",
        "**Pipeline integration:** run the hardware team’s calibration scripts and meditation application "
        "without depending on their internal code.",
        "**Report display:** show the generated PDF report inside the kiosk and reset for the next visitor.",
        "**Packaging and documentation:** install on a fresh machine with a single command, with documented "
        "installation, operation and troubleshooting.",
    ])
    r.p("""Building the camera and motor control logic and the meditation content was outside the scope of this
    internship; these were provided by the hardware team and are described only where the kiosk software
    had to be designed around them.""")

    r.section("Organization of Report")
    r.p("""This report has been structured to give a systematic account of the work done during the
    internship at the INDReA Lab, IIT Hyderabad. The chapters are organised as follows:""")
    r.numbered([
        "**Introduction:** the project, its motivation, the problem statement and the objectives.",
        "**Background Material:** the concepts behind an unattended kiosk and the technologies used, with "
        "the reasons for choosing them.",
        "**Methodology:** the step-by-step approach followed, and the block diagrams of the system, the "
        "hardware, the visitor flow, the database and the pipeline.",
        "**Implementation:** the software modules and the prototype, including the kiosk apparatus and the "
        "screens of the final application.",
        "**Results and Analysis:** the outcomes, the testing carried out, the evolution of the design, and the "
        "challenges faced and lessons learned.",
        "**Conclusions & Future Scope:** a summary of the achievements and realistic extensions of the work.",
        "**References and Annexures:** sources used, the weekly work log, code snippets, wireframes and setup "
        "commands.",
    ])

    # ------------------------------------------------------------ chapter 2
    r.chapter("BACKGROUND MATERIAL")
    r.section("Conceptual Overview (*Concepts/Theory Used*)", "Conceptual Overview (Concepts/Theory used)")
    r.p("""Several concepts from human–computer interaction, distributed systems and operating systems were
    applied in this project. They are summarised below.""")
    r.sub("1. Unattended kiosk systems")
    r.p("""Kiosk software differs from an ordinary desktop application mainly in what happens when nobody is
    watching. It must start without a login prompt, occupy the whole screen, survive crashes and power
    cuts, keep a visitor from reaching the desktop and return to a known state after every visitor. Every
    failure must either be recovered automatically or be shown clearly enough for staff to act on it.""")
    r.sub("2. Visitor identification and QR codes")
    r.p("""A QR code is a two-dimensional barcode that can carry a short text such as a URL, and every modern
    phone camera can read it. Several ways of identifying a visitor were compared (Table 2). Because the kiosk
    had no scanner and its cameras were reserved for the meditation pipeline, the chosen approach was for the
    **kiosk to show** a QR code and the **phone to scan** it.""")
    r.table("Comparison of visitor identification approaches",
            ["Approach", "Hardware at kiosk", "Visitor effort", "Remarks"], [
        ["Printed pass + USB scanner", "QR scanner", "Carry and present a pass",
         "Extra hardware and printing; explored as an offline variant"],
        ["Typing details at the kiosk", "Keyboard", "High", "Kept only as a staff/testing fallback"],
        ["Phone shows QR to kiosk camera", "Camera facing visitor", "Medium",
         "Kiosk cameras are needed by the CV pipeline"],
        ["**Kiosk shows QR, phone scans**", "None", "Low: open link, tap, scan", "**Chosen**"],
        ["Face recognition", "Camera", "None", "Future option; needs enrolment and privacy care"],
    ], [1.9, 1.4, 1.6, 2.1])
    r.sub("3. Client–server communication and polling")
    r.p("""The kiosk and the phone never talk directly. Both talk to a REST API over HTTPS. The kiosk creates a
    *session* and then **polls** the server every two seconds to learn whether a phone has claimed it.
    Polling is simpler than a push channel, works through any network and is cheap at this scale.""")
    r.sub("4. Display servers and the Wayland security model")
    r.p("""Ubuntu’s GNOME desktop uses **Wayland**. Unlike the older X11 system, the compositor decides where
    windows go, and an application may not move, raise or hide another application’s windows, or even raise
    itself. This improves security but limits what kiosk software can do, and several design decisions
    followed from it.""")
    r.sub("5. Process-based integration")
    r.p("""Instead of an API between the kiosk and the hardware software, the integration uses two operating-system
    primitives: a **child process** (the kiosk runs a shell script and waits for it to exit) and a **file
    on disk** (the meditation application writes a PDF that the kiosk reads). This loose coupling lets each
    team change its internals without breaking the other.""")
    r.sub("6. Packaging, services and fault recovery")
    r.p("""A self-contained Debian package bundles the application with its runtime, so nothing has to be
    installed first. A **systemd user service** starts the kiosk with the desktop session and restarts it
    automatically if it exits, which provides crash recovery without custom code.""")
    r.sub("7. Privacy and security")
    r.p("""The roster contains names, photographs and Aadhaar numbers, so the design follows data minimisation:
    links use long random tokens that cannot be guessed, public endpoints return only what is needed to greet
    a person, and the administrator’s upload is protected by a secret key.""")

    r.section("Technologies Involved")
    r.p("""The following tools and technologies were used to build, deploy and test the system:""")
    r.sub("1. Kiosk desktop application")
    r.bullets([
        "**C# and .NET 8 (LTS):** garbage-collected memory removes a whole class of crashes for a machine that "
        "runs all day; publishing produces one self-contained binary.",
        "**Avalonia 11.2.3:** a cross-platform .NET UI framework that officially supports Linux and draws its "
        "own controls with Skia, so the UI looks identical on the laptop and the kiosk.",
        "**QRCoder 1.6.0:** generates the session QR code without System.Drawing.",
        "**PDFtoImage 4.1.1 (PDFium + SkiaSharp):** renders the report pages inside the application.",
    ])
    r.sub("2. Backend and database")
    r.bullets([
        "**Node.js 18+ and Express 4:** a small REST API that also serves the web pages.",
        "**PostgreSQL with the pg driver:** stores visitors, sessions and the roster.",
        "**Render:** hosts the web service and database from a blueprint file, with HTTPS.",
    ])
    r.sub("3. Web pages")
    r.bullets([
        "**HTML and JavaScript:** registration, admin and login pages.",
        "**SheetJS:** parses the uploaded Excel roster inside the browser.",
        "**html5-qrcode:** turns the phone camera into a QR scanner.",
    ])
    r.sub("4. Pipeline, packaging and tools")
    r.bullets([
        "**Bash and Python 3.10:** the pipeline script and the hardware team’s calibration scripts.",
        "**dotnet publish, dpkg-deb and systemd:** the Debian package, auto-start and restart.",
        "**Git and GitHub:** one branch and pull request per change.",
        "**Docker, Xvfb and noVNC:** preview of the UI in a browser during development.",
    ])
    r.p("Table 3 compares the UI frameworks that were considered for the kiosk.")
    r.table("Comparison of desktop UI frameworks", ["Option", "Linux support", "Native access", "Verdict"], [
        ["**C# / .NET 8 + Avalonia**", "Official (X11 and Wayland)", "Full", "**Chosen**"],
        [".NET MAUI", "No Linux target", "Full", "Rejected"],
        ["Electron", "Good", "Needs a native helper", "Heavier; two processes"],
        ["Web app in a browser", "Good", "None (sandbox)", "Cannot launch the pipeline"],
        ["C++ with Qt", "Good", "Full", "No benefit for this UI; manual memory"],
    ], [2.0, 1.7, 1.6, 1.7])

    # ------------------------------------------------------------ chapter 3
    r.chapter("METHODOLOGY")
    r.section("Detailed methodology that will be adopted")
    r.sub("1. Requirement Analysis")
    r.bullets([
        "**Discussions with the lab:** understood the visitor experience, the hardware rig and what the hardware "
        "team would provide.",
        "**Constraints identified:** no QR scanner or keyboard at the kiosk; cameras reserved for the pipeline; "
        "Ubuntu with GNOME on Wayland; unattended operation.",
        "**Requirements written down:** functional requirements (Table 4) and non-functional requirements "
        "(Table 5).",
    ])
    r.table("Functional requirements", ["ID", "Requirement"], [
        ["FR1", "On start-up the kiosk opens fullscreen and shows a welcome screen with a QR code."],
        ["FR2", "Each QR code carries a fresh, hard-to-guess session token created by the backend."],
        ["FR3", "An administrator uploads an Excel roster and gets one private login link per person."],
        ["FR4", "A visitor opens their link on a phone, scans the kiosk QR and is identified."],
        ["FR5", "Visitors not on the roster can register themselves on the phone."],
        ["FR6", "The kiosk shows the visitor’s name and photo within a few seconds of the scan."],
        ["FR7", "The kiosk then runs the calibration and meditation pipeline automatically, with a live status."],
        ["FR8", "When the pipeline ends, the kiosk shows the new report and a thank-you message."],
        ["FR9", "A Return button resets the kiosk and creates a new session."],
        ["FR10", "A manual name entry lets staff start a session without a phone or server."],
    ], [0.8, 6.2])
    r.table("Non-functional requirements", ["Category", "Requirement"], [
        ["Reliability", "Auto-start on boot; restart within seconds after a crash; no state between visitors."],
        ["Recoverability", "Network failures show a clear message and a retry action."],
        ["Portability", "Installs on any recent Ubuntu (amd64 or arm64) with nothing pre-installed."],
        ["Privacy", "Aadhaar never returned by public endpoints; unguessable tokens."],
        ["Usability", "At most three taps on the phone; nothing to type at the kiosk."],
        ["Maintainability", "Editable pipeline script; paths overridable by environment variables."],
    ], [1.6, 5.4])
    r.sub("2. System Design")
    r.bullets([
        "Designed the architecture, the visitor flow as a state machine, the database schema and the REST API "
        "(Section 3.2).",
        "Designed the screens as wireframes before coding them (Annexure C).",
        "Agreed the integration contract with the hardware team: one script to run and one folder to read the "
        "report from.",
    ])
    r.sub("3. Iterative Development")
    r.bullets([
        "Built the system in small increments; every change on its own Git branch and merged through a pull "
        "request (28 pull requests during the internship).",
        "Released a new Debian package whenever the kiosk needed an update, and updated the setup guide with "
        "every merge.",
        "Explored alternatives on separate branches (an offline people-list mode and an in-app meditation flow) "
        "before choosing the final direction.",
    ])
    r.sub("4. Integration with the Hardware Pipeline")
    r.bullets([
        "Wrapped the hardware team’s stages in an editable script with retry rules.",
        "Displayed only reports written after the session started, so a previous visitor’s report can never be "
        "shown.",
    ])
    r.sub("5. Testing and Validation")
    r.bullets([
        "Automated end-to-end tests of the backend session flow and the kiosk’s HTTP client.",
        "Headless rendering of every screen; a no-camera test kit that replaces the pipeline with a mock.",
        "Installation and live runs on the real kiosk, including a recorded demonstration with a phone.",
    ])
    r.sub("6. Deployment and Documentation")
    r.bullets([
        "Packaged the kiosk as a self-contained .deb with a systemd service and kiosk setup script.",
        "Deployed the backend on Render from a blueprint file.",
        "Wrote the setup guide, a handoff document and a codebase overview for the lab.",
    ])

    r.section("Circuit Layouts / block diagrams")
    r.sub("1. Overall System Architecture")
    r.p("""**Block diagram elements:** the administrator’s PC and the visitor’s phone (browsers); the backend API
    and PostgreSQL database on Render; and, on the kiosk machine, the Diya application, the pipeline script
    and the hardware team’s stack (Figure 1).""")
    r.p("""**Flow:** Admin PC → Backend (roster) · Kiosk → Backend (create session, poll) · Phone camera reads
    kiosk QR → Backend (claim) · Kiosk → run1.sh → hardware stack → report PDF → Kiosk.""")
    r.fig("figures/fig_architecture.png", "Overall system architecture of the Diya kiosk")
    r.p("""The kiosk and the hardware stack never call each other over an API; the only contract is a script to
    run and a folder to watch.""")
    r.sub("2. Hardware Block Diagram")
    r.p("""**Block diagram elements:** four USB cameras (Logitech C920, Intel RealSense D435, Arducam 8MP and a
    thermal camera), the display, an Arduino controller driving motors M1 (chest axis) and M2 (eye axis), the
    limit switches and proximity sensors, and an LD2410 radar that detects a seated person (Figure 2).""")
    r.p("""**Flow:** Cameras → Kiosk PC (V4L2) · Kiosk PC ⇄ Arduino (USB serial, 115200 baud) → Motors ·
    Safety inputs → Arduino · Radar → Kiosk PC (USB serial, 256000 baud) · Kiosk PC → Display (HDMI).""")
    r.fig("figures/fig_hardware_block.png", "Hardware block diagram of the kiosk")
    r.sub("3. Visitor Flow")
    r.p("""**Flow:** Idle (QR on screen) → Claimed (name and photo) → Session (pipeline running) → Report
    (PDF and thank-you) → Return → Idle. A manual name entry skips straight to Claimed (Figure 3).""")
    r.fig("figures/fig_visitor_flow.png", "Visitor flow of the kiosk as a state machine")
    r.sub("4. Interaction Sequence")
    r.p("""Figure 4 shows every message for one visitor. Solid arrows are HTTP requests, dashed arrows are
    responses, and dotted arrows do not use the API at all: the link shared with the visitor, the phone camera
    reading the screen, and the local pipeline with its PDF output.""")
    r.fig("images/diagram-timeline.png", "Sequence of interactions between admin, phone, kiosk, backend and "
          "meditation-app", 6.5)
    r.sub("5. Database Design")
    r.p("""**people** holds the uploaded roster; each row has an unguessable token that forms the private link
    `/p/<token>`. **sessions** holds one row per QR code shown on the kiosk, with status pending or claimed.
    **visitors** holds the identity linked to a session; on a claim the roster details are copied into a visitor
    row (Figure 5).""")
    r.fig("figures/fig_er_diagram.png", "Database schema (entity–relationship view)")
    r.sub("6. Pipeline Flowchart")
    r.p("""**Flow:** HOME1 (home the axes) → SHOOT1 (deploy actuators) → CHEST1 (align chest camera) → EYE1
    (align eye camera) → meditation-app (session and PDF report). Homing and deployment retry themselves;
    a failure in chest or eye alignment restarts the whole sequence from homing (Figure 6).""")
    r.fig("figures/fig_pipeline.png", "Retry logic of the pipeline script run1.sh")
    r.sub("7. Build and Deployment")
    r.fig("figures/fig_deployment.png", "Build and deployment of the kiosk and the backend")

    # ------------------------------------------------------------ chapter 4
    r.chapter("IMPLEMENTATION")
    r.section("Modules")
    r.p("The implementation was divided into the following modules:")
    r.sub("1. Kiosk Shell Module (fullscreen on Wayland)")
    r.bullets([
        "**Resizable window:** marking the window non-resizable sets fixed size hints, and the compositor then "
        "refuses to make it fullscreen.",
        "**Fullscreen applied in code and re-asserted:** applied when the window opens and re-applied six times "
        "at 250 ms intervals, because the compositor first maps the window in its normal state.",
        "**Portable build:** invariant globalisation removes the libicu dependency, and a self-contained "
        "single-file publish bundles the .NET runtime.",
        "**Delayed auto-start:** launching before the Wayland session is ready fails silently, so start-up "
        "waits a few seconds.",
    ])
    r.sub("2. Home Screen, Session QR and Polling Module")
    r.bullets([
        "Requests a new session; because the free server sleeps when idle, the status reads “Waking up the "
        "server…” and the HTTP client allows 60 seconds.",
        "Encodes `<site>/?session=<token>` as a QR image and polls `GET /api/sessions/:token` every 2 seconds.",
        "On a claim, shows the visitor’s name, email, age and roster photo; the photo fails open and never "
        "blocks the session.",
        "Offers **New code** to retry after a network error, and a manual name entry for staff.",
    ])
    r.sub("3. Backend API Module")
    r.bullets([
        "**Unguessable tokens:** session tokens of 9 random bytes and personal link tokens of 16 random bytes.",
        "**Claim only once:** a session is linked to a visitor only while its status is still pending.",
        "**Minimal disclosure:** the greeting endpoint returns only name and role.",
        "**Admin protection:** roster upload requires the ADMIN_KEY secret; without it the feature is off.",
    ])
    r.table("REST endpoints of the backend", ["Method", "Endpoint", "Used by", "Purpose"], [
        ["GET", "/api/health", "Operators", "Liveness check"],
        ["POST", "/api/sessions", "Kiosk", "Create a session; returns a token"],
        ["GET", "/api/sessions/:token", "Kiosk", "Poll: pending, or claimed with the visitor"],
        ["POST", "/api/visitors", "Phone", "Self-registration"],
        ["POST", "/api/admin/upload", "Admin page", "Create people from the roster (needs key)"],
        ["GET", "/api/people/:token", "Phone", "Greeting: name and role only"],
        ["POST", "/api/claim", "Phone", "Link the person to the session"],
    ], [0.8, 2.0, 1.1, 3.1])
    r.sub("4. Web Pages Module")
    r.bullets([
        "**admin.html:** parses the Excel roster in the browser, matches column headers loosely, previews rows "
        "with Aadhaar masked, and returns one personal link per person with Copy all and CSV download.",
        "**scan.html (/p/<token>):** greets the person, opens the phone camera, reads the kiosk QR and claims "
        "the session.",
        "**index.html:** self-registration for visitors who are not on a roster.",
    ])
    r.figrow([("images/web-03-admin.png", "(a) Admin roster upload"),
              ("images/web-02-login.png", "(b) Personal login link"),
              ("images/web-01-register.png", "(c) Self-registration")],
             "Web pages of the system (sample data)", 3.4)
    r.sub("5. Pipeline Integration and Report Display Module")
    r.bullets([
        "Runs `bash scripts/run1.sh` without a terminal window and shows each line it prints as the live "
        "status; there is deliberately no timeout because the meditation takes several minutes.",
        "Picks the newest PDF in `/opt/meditation-app/data` written **after the session started**, so a "
        "previous visitor’s report is never shown.",
        "Renders the pages as images inside the app, so no external viewer can take focus, and adds a "
        "thank-you line and a single Return button.",
    ])
    r.sub("6. Packaging and Deployment Module")
    r.bullets([
        "`build-deb.sh` builds a self-contained .deb for amd64 or arm64 with the scripts, desktop entry and "
        "systemd unit.",
        "The systemd user service restarts the app 2 seconds after any exit; `setup-kiosk.sh` enables auto-login "
        "and disables escape shortcuts.",
        "The backend is deployed from `render.yaml`, which creates the web service and database.",
    ])
    r.table("Configuration through environment variables", ["Variable", "Where", "Meaning"], [
        ["DIYA_API_BASE", "Kiosk", "Backend URL"],
        ["DIYA_PIPELINE_SCRIPT", "Kiosk", "Script to run on login"],
        ["DIYA_REPORT_DIR", "Kiosk", "Folder to read the report from"],
        ["DATABASE_URL", "Server", "PostgreSQL connection string"],
        ["ADMIN_KEY", "Server", "Secret that enables and protects roster upload"],
    ], [2.3, 1.0, 3.7])

    r.section("Prototype")
    r.sub("1. Kiosk Apparatus")
    r.p("""The prototype is a physical installation: a seat, a display, and a sensor assembly carrying the cameras,
    moved by two motorised axes and guarded by limit switches, proximity sensors and a radar. The apparatus
    and its control scripts were built by the hardware team; Table 8 lists the components.""")
    r.table("Hardware components of the kiosk", ["Component", "Role", "Interface"], [
        ["Kiosk PC (Ubuntu)", "Runs the kiosk app, CV scripts and meditation-app", "—"],
        ["Display", "Kiosk UI, meditation video, report", "HDMI"],
        ["Logitech C920 webcam", "Face and gaze", "USB (V4L2)"],
        ["Intel RealSense D435", "Depth", "USB"],
        ["Arducam 8MP", "Front view and posture", "USB (V4L2)"],
        ["USB thermal camera", "Thermal capture", "USB (V4L2)"],
        ["Arduino controller", "Drives motors; reads switches and sensors", "USB serial, 115200 baud"],
        ["Motors M1 and M2", "Chest axis and eye axis; homing and actuator", "Via Arduino"],
        ["Limit switches, proximity sensors", "Home position, collision detection", "Via Arduino"],
        ["LD2410 mmWave radar", "Seated person, 650–1050 mm", "USB serial, 256000 baud"],
    ], [2.2, 2.9, 1.9])
    r.placeholder("Front view of the Diya meditation kiosk",
                  "Insert photograph: the complete kiosk as a visitor sees it.")
    r.placeholder("Side view showing the seat and sensor arm",
                  "Insert photograph: seating position relative to the cameras.")
    r.placeholder("Camera assembly", "Insert photograph: close-up of the camera mounts.")
    r.placeholder("Motorised chest and eye axes", "Insert photograph: motors, axes and limit switches.")
    r.placeholder("Arduino controller and wiring", "Insert photograph: controller board and wiring.")
    r.placeholder("LD2410 radar sensor and mounting", "Insert photograph: radar module and its position.")
    r.sub("2. Screens of the Final Application")
    r.p("""Figures 15 to 18 are genuine frames of the kiosk application rendered with the same layout, fonts and
    QR encoder as on the kiosk. The visitor is fictional and the report is a representative sample, since the
    real report comes from the hardware team’s software.""")
    r.fig("images/app-01-idle-qr.png", "Kiosk idle: session created and QR code displayed", 5.6)
    r.fig("images/app-02-authenticated.png", "Kiosk after the phone has claimed the session", 5.6)
    r.fig("images/app-03-session-running.png", "Pipeline running with the live status line", 5.6)
    r.fig("images/app-04-report.png", "Report displayed with the thank-you message and Return", 5.6)
    r.sub("3. Live Demonstration")
    r.p("""Figures 19 and 20 are frames from a recorded run with the deployed backend: the personal link greets the
    visitor, the phone scans the kiosk QR, and the kiosk advances by itself. The recording used an earlier build,
    so some labels differ slightly from the final version.""")
    r.figrow([("images/real-greeting.png", "(a) Personal link greets the visitor"),
              ("images/real-scan.png", "(b) Phone scanning the kiosk QR")],
             "Live demonstration: the visitor’s phone", 3.8)
    r.fig("images/real-kiosk.png", "Live demonstration: the kiosk after the claim (email blurred)", 5.6)

    # ------------------------------------------------------------ chapter 5
    r.chapter("RESULTS AND ANALYSIS")
    r.section("Results")
    r.sub("1. Visitor Identification Without Extra Hardware")
    r.p("**Results:**")
    r.bullets([
        "Visitors are identified with only their own phone: open the link, tap, scan.",
        "Each scan proves who arrived, because the link is private and unguessable.",
        "The kiosk shows the visitor’s details within one polling interval (2 s) of the claim.",
    ])
    r.p("""**Analysis:** The missing scanner turned out to simplify the design. No app, no typing at the kiosk and
    no extra hardware were needed, and the kiosk cameras stayed free for the meditation pipeline.""")
    r.sub("2. Reliable Unattended Operation")
    r.p("**Results:**")
    r.bullets([
        "The kiosk opens fullscreen on GNOME/Wayland and installs from one package on amd64 and arm64.",
        "systemd restarts the application after any crash; network errors show a clear retry option.",
    ])
    r.p("""**Analysis:** Building on the platform’s own mechanisms (systemd, self-contained publishing) gave
    reliability with very little custom code, which suits a machine that runs without supervision.""")
    r.sub("3. Integration with the Hardware Team")
    r.p("**Results:**")
    r.bullets([
        "The complete journey (identify, claim, pipeline, report, reset) works end to end.",
        "A previous visitor’s report is never shown, and no terminal or viewer window appears from the kiosk.",
    ])
    r.p("""**Analysis:** A contract of one script and one folder was enough, and it let both teams develop and
    test independently.""")
    r.sub("4. Evolution of the Design")
    r.p("""The design changed most in how visitors are identified (Figure 21, Table 9). The first version put the
    visitor’s data inside the QR; this was readable by anyone and could not be revoked, so version 1.2 stored the
    data online and kept only an ID in the code. Version 1.3 reversed the flow so the kiosk shows the QR, and the
    admin roster added in July made each scan prove identity. In late July the kiosk was made to minimise itself
    during the session, but Wayland does not let an application restore itself, so the change was rolled back to
    the last stable baseline and the useful parts were re-implemented in version 1.6.0.""")
    r.fig("figures/fig_evolution.png", "Timeline of the main versions")
    r.table("Version history", ["Version", "Date", "Change"], [
        ["1.0.x", "11–13 Jun", "Fullscreen kiosk shell, Wayland fixes, .deb for amd64 and arm64"],
        ["1.1.0", "17 Jun", "Offline QR pass: visitor details inside the QR"],
        ["1.2.0", "19 Jun", "Online lookup: QR carries only an ID"],
        ["1.3.0", "26 Jun", "Reverse flow: kiosk shows the QR, phone registers"],
        ["1.4.0", "26 Jun – 9 Jul", "Calibration launch, admin roster, phone login, visitor photo"],
        ["1.5.0", "11 Jul", "Login runs the pipeline and shows the PDF report"],
        ["1.6.0", "31 Jul", "Report-ready flow, live status, thank-you, no-camera test kit"],
    ], [1.0, 1.5, 4.5])

    r.section("Testing and Validation")
    r.table("Summary of test cases", ["#", "Scenario", "Expected result", "Outcome"], [
        ["T1", "Create session, register, poll", "Poll returns claimed", "Passed (automated)"],
        ["T2", "Kiosk client: claim and unknown token", "Claimed; unknown is NotFound", "Passed (automated)"],
        ["T3", "Render every screen headlessly", "Screens build", "Passed"],
        ["T4", "Install .deb on several Ubuntu releases", "No dependency errors", "Passed after removing libicu"],
        ["T5", "Start on GNOME/Wayland", "Window covers the screen", "Passed after fullscreen fixes"],
        ["T6", "First request to a sleeping server", "Kiosk waits, then shows QR", "Passed (60 s timeout)"],
        ["T7", "Network unavailable", "Clear error and retry", "Passed"],
        ["T8", "Broken roster photo URL", "Session continues", "Passed"],
        ["T9", "Full flow with the mock pipeline", "Status, sample report, thank-you", "Passed"],
        ["T10", "Phone scans kiosk QR (live)", "Kiosk advances itself", "Passed (recorded demo)"],
        ["T11", "Kiosk minimises itself during session", "Kiosk returns afterwards",
         "**Failed on Wayland**; rolled back"],
        ["T12", "Kiosk clock set in the past", "HTTPS works", "Failed; fixed by enabling NTP"],
    ], [0.5, 2.3, 2.1, 2.1])
    r.p("""Because the real pipeline needs the cameras, motors and meditation application, a small test kit was
    written that replaces it with a mock script. Two environment variables point the kiosk at the mock and a
    temporary report folder; no test code is included in the package, so the tested kiosk is exactly the one that
    ships.""")

    r.section("Challenges Faced and Learnings")
    r.table("Main challenges and how they were addressed", ["Challenge", "Resolution"], [
        ["Fullscreen did not stick on Wayland", "Resizable window, fullscreen applied in code and re-asserted"],
        ["Package failed on some Ubuntu versions", "Bundle the runtime; drop the ICU dependency"],
        ["No QR scanner at the kiosk", "Kiosk shows the QR; the phone scans it"],
        ["Integrating another team’s software", "Script plus report folder; only PDFs newer than the session"],
        ["Free server sleeps when idle", "Long client timeout and a “waking up” message"],
        ["Phone camera blocked on plain HTTP", "Serve all pages over HTTPS"],
        ["Kiosk could not restore itself", "Roll back; avoid self-managing windows on Wayland"],
    ], [3.0, 4.0])
    r.p("**Learnings:**")
    r.bullets([
        "**Constraints can simplify a design:** the missing scanner led to an easier flow for visitors.",
        "**Integrate through the narrowest contract:** a script and a folder let two teams move independently.",
        "**Know the platform’s rules first:** fighting Wayland’s window policy cost two releases.",
        "**Rolling back is a valid decision:** returning to a known-good baseline was faster than patching.",
        "**Write things down:** keeping the setup guide updated let the lab install each build without me.",
    ])

    # ------------------------------------------------------------ chapter 6
    r.chapter("CONCLUSIONS & FUTURE SCOPE")
    r.section("Conclusions")
    r.p("""The internship at the INDReA Lab, IIT Hyderabad, produced the complete software side of the Diya
    meditation kiosk. The key conclusions are:""")
    r.sub("1. Hardware-free visitor identification")
    r.bullets([
        "**Outcomes:** visitors are identified with nothing but their own phone, in three taps.",
        "**Significance:** removing a scanner reduced cost and points of failure while improving the experience.",
    ])
    r.sub("2. Reliable unattended kiosk")
    r.bullets([
        "**Outcomes:** a fullscreen application that installs with one command, starts on boot and recovers "
        "from crashes.",
        "**Significance:** the kiosk can run all day in a public space without an attendant.",
    ])
    r.sub("3. Clean integration across teams")
    r.bullets([
        "**Outcomes:** the hardware team’s pipeline runs from the kiosk and its report is shown in the app.",
        "**Significance:** a minimal contract let both teams evolve their parts without breaking each other.",
    ])
    r.sub("4. Documented, maintainable system")
    r.bullets([
        "**Outcomes:** seven versions delivered, each with an updated setup guide, plus a handoff document.",
        "**Significance:** the lab can operate, update and extend the kiosk after the internship.",
    ])

    r.section("Future Scope of Work", "Future Scope of Work (at least 3 points)")
    r.sub("1. Consent and Privacy Screen")
    r.bullets([
        "**Objective:** show what is captured and stored, and obtain consent, before any camera starts.",
        "**Significance:** the kiosk records people and the roster contains ID numbers, so this is needed before "
        "public deployment.",
    ])
    r.sub("2. Inactivity Reset and Pipeline Timeouts")
    r.bullets([
        "**Objective:** return to the welcome screen if a visitor leaves mid-session, and add an overall timeout "
        "with an error screen to the pipeline and to the alignment loops.",
        "**Significance:** a stage that never succeeds can then no longer hang the kiosk.",
    ])
    r.sub("3. Real Calibration Stages")
    r.bullets([
        "**Objective:** replace the placeholder scripts called by run1.sh with the hardware team’s motor-control "
        "and radar stages.",
        "**Significance:** the visitor will be physically aligned to the sensors, improving data quality.",
    ])
    r.sub("4. Face Recognition and Report Delivery")
    r.bullets([
        "**Objective:** identify enrolled visitors by face and send the report to them by email.",
        "**Significance:** removes even the phone step and lets visitors keep their results.",
    ])
    r.sub("5. Continuous Integration and Persistent Database")
    r.bullets([
        "**Objective:** build packages automatically as releases with a single version number, and move the "
        "database off the free tier, which deletes data after 30 days.",
        "**Significance:** safer updates and no loss of visitor data.",
    ])

    # ------------------------------------------------------------ references
    r.unnumbered("References")
    r.raw("refs", items=[
        "A. Troelsen and P. Japikse, *Pro C# 10 with .NET 6: Foundational Principles and Practices in "
        "Programming*, 11th ed. Berkeley, CA, USA: Apress, 2022.",
        "R. T. Fielding, “Architectural styles and the design of network-based software architectures,” "
        "Ph.D. dissertation, Univ. of California, Irvine, CA, USA, 2000.",
        "M. Kleppmann, *Designing Data-Intensive Applications*. Sebastopol, CA, USA: O’Reilly Media, 2017.",
        "M. T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 2nd ed. Raleigh, NC, USA: "
        "Pragmatic Bookshelf, 2018.",
        "J. Humble and D. Farley, *Continuous Delivery: Reliable Software Releases through Build, Test, and "
        "Deployment Automation*. Boston, MA, USA: Addison-Wesley, 2010.",
        "D. A. Norman, *The Design of Everyday Things*, revised ed. New York, NY, USA: Basic Books, 2013.",
        "B. Shneiderman, C. Plaisant, M. Cohen, S. Jacobs, N. Elmqvist and N. Diakopoulos, *Designing the User "
        "Interface: Strategies for Effective Human-Computer Interaction*, 6th ed. Boston, MA, USA: Pearson, 2016.",
        "H. Brignull and Y. Rogers, “Enticing people to interact with large public displays in public spaces,” "
        "in *Proc. IFIP INTERACT*, Zurich, Switzerland, 2003, pp. 17–24.",
        "P. Peltonen *et al.*, “It’s Mine, Don’t Touch!: Interactions at a large multi-touch display in a city "
        "centre,” in *Proc. ACM CHI Conf. Human Factors in Computing Systems*, Florence, Italy, 2008, "
        "pp. 1285–1294.",
        "J. Kabat-Zinn, *Full Catastrophe Living: Using the Wisdom of Your Body and Mind to Face Stress, Pain, "
        "and Illness*. New York, NY, USA: Delacorte Press, 1990.",
        "*Information technology — Automatic identification and data capture techniques — QR Code bar code "
        "symbology specification*, ISO/IEC 18004:2015, 2015.",
        "Avalonia UI, “Avalonia documentation,” 2026. [Online]. Available: https://docs.avaloniaui.net/",
        "Microsoft, “.NET application publishing overview,” 2026. [Online]. Available: "
        "https://learn.microsoft.com/dotnet/core/deploying/",
        "The PostgreSQL Global Development Group, *PostgreSQL 16 Documentation*, 2026. [Online]. Available: "
        "https://www.postgresql.org/docs/",
        "freedesktop.org, “systemd.service — Service unit configuration,” 2026. [Online]. Available: "
        "https://www.freedesktop.org/software/systemd/man/systemd.service.html",
        "K. Høgsberg *et al.*, “The Wayland protocol,” 2026. [Online]. Available: "
        "https://wayland.freedesktop.org/docs/html/",
        "Intel Corporation, *Intel RealSense Product Family D400 Series Datasheet*, rev. 016, 2023.",
        "Hi-Link Electronic, *HLK-LD2410 Human Presence Sensing Module: User Manual and Serial Protocol*, 2022.",
    ])

    # ------------------------------------------------------------ annexures
    r.unnumbered("Annexures")
    r.sub("Annexure A: Weekly Work Log")
    r.fig("figures/fig_gantt.png", "Gantt chart of the internship (1 June – 31 July 2026)")
    r.table("Weekly work log", ["Week", "Dates", "Work done"], [
        ["1", "1–7 Jun", "Orientation at the lab; study of the kiosk concept; requirements; choice of .NET 8 and Avalonia"],
        ["2", "8–14 Jun", "First kiosk app; two-panel home screen; Wayland fullscreen fixes; .deb builder; setup guide"],
        ["3", "15–21 Jun", "Offline install; QR visitor pass (v1.1.0); hosted API with lookup by ID (v1.2.0)"],
        ["4", "22–28 Jun", "Reverse QR flow with phone registration (v1.3.0); calibration launch (v1.4.0)"],
        ["5", "29 Jun – 5 Jul", "Alternative branches; project overview and FAQ; admin roster and reverse-scan login"],
        ["6", "6–12 Jul", "Visitor photo; setup docs; login runs the pipeline and shows the PDF (v1.5.0)"],
        ["7", "13–19 Jul", "Window behaviour changes requested by the lab; testing on the kiosk"],
        ["8", "20–26 Jul", "Codebase overview; window hand-off experiment; no-camera test kit"],
        ["9", "27–31 Jul", "Rollback to the stable baseline; report-ready flow and thank-you (v1.6.0); handoff"],
    ], [0.7, 1.4, 4.9])
    r.sub("Annexure B: Code Snippets")
    r.p("**B.1 Choosing the report for the current visitor (ReportRenderer.cs):**")
    r.code("""
var newest = new DirectoryInfo(ReportDir)
    .EnumerateFiles("*.pdf")
    .Where(f => f.LastWriteTimeUtc >= sinceUtc)   // only this session's report
    .OrderByDescending(f => f.LastWriteTimeUtc)
    .FirstOrDefault();
""")
    r.p("**B.2 Claiming a session only once (server.js):**")
    r.code("""
UPDATE sessions
   SET status = 'claimed', visitor_id = $1, claimed_at = now()
 WHERE token = $2 AND status = 'pending';
""")
    r.p("**B.3 Retry rules of the pipeline (run1.sh):**")
    r.code("""
while true; do
  until run_step HOME1.py  python3.10 HOME1.py;  do sleep 1; done  # retry
  until run_step SHOOT1.py python3.10 SHOOT1.py; do sleep 1; done  # retry
  run_step CHEST1.py python3.10 CHEST1.py || continue  # from HOME1
  run_step EYE1.py   python3.10 EYE1.py   || continue  # from HOME1
  meditation-app; break
done
""")
    r.p("**B.4 Auto-restart service (diya-meditation.service):**")
    r.code("""
[Service]
ExecStart=/opt/diya-meditation/DiyaMeditation
Restart=always
RestartSec=2
Environment=DIYA_API_BASE=https://diya-registration.onrender.com
""")
    r.sub("Annexure C: Screen Wireframes")
    r.fig("images/wf-01.png", "Wireframe WF-01: kiosk idle, waiting to be scanned", 6.0)
    r.fig("images/wf-02.png", "Wireframe WF-02: visitor identified, session starting", 6.0)
    r.fig("images/wf-03.png", "Wireframe WF-03: report overlay", 6.0)
    r.fig("images/wf-04.png", "Wireframe WF-04: the visitor’s three taps on the phone", 6.0)
    r.sub("Annexure D: Installation Commands")
    r.code("""
systemctl --user stop diya-meditation 2>/dev/null; pkill -f DiyaMeditation
sudo dpkg -i ./diya-meditation_1.6.0_amd64.deb
diya-meditation
curl https://diya-registration.onrender.com/api/health
cd DiyaMeditation && ./deploy/build-deb.sh 1.6.0 amd64
""")
    return r
