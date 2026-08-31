import { useEffect, useRef, useState } from 'react';
import { motion, useScroll, useSpring } from 'motion/react';

import Aurora from './reactbits/Aurora';
import SplitText from './reactbits/SplitText';
import CountUp from './reactbits/CountUp';
import SpotlightCard from './reactbits/SpotlightCard';
import TiltedCard from './reactbits/TiltedCard';
import ScrollReveal from './reactbits/ScrollReveal';
import GradientText from './reactbits/GradientText';

const SECTIONS = [
  ['hero', 'Diya'],
  ['brief', 'The brief'],
  ['scope', 'Scope'],
  ['problem', 'The problem'],
  ['attempts', 'Three attempts'],
  ['inversion', 'The inversion'],
  ['flow', 'The flow'],
  ['wireframes', 'Wireframes'],
  ['gallery', 'Screens'],
  ['stack', 'Architecture'],
  ['testing', 'Testing'],
  ['shipping', 'Shipping'],
  ['roadmap', 'Handover'],
];

/* generic scroll-in wrapper */
function Reveal({ children, delay = 0, y = 34 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.25 }}
      transition={{ duration: 0.72, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}

function Card({ n, title, children, mono, hi, delay = 0 }) {
  return (
    <Reveal delay={delay}>
      <SpotlightCard
        className={hi ? 'hi' : ''}
        spotlightColor={hi ? 'rgba(233,184,114,.22)' : 'rgba(180,169,214,.13)'}
      >
        {n && <div className="cardnum">{n}</div>}
        <h3>{title}</h3>
        <p>{children}</p>
        {mono && <span className="mono">{mono}</span>}
      </SpotlightCard>
    </Reveal>
  );
}

export default function App() {
  const [active, setActive] = useState('hero');
  const { scrollYProgress } = useScroll();
  const width = useSpring(scrollYProgress, { stiffness: 120, damping: 28, restDelta: 0.001 });
  const refs = useRef({});

  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => e.isIntersecting && setActive(e.target.id));
      },
      { rootMargin: '-45% 0px -45% 0px' }
    );
    SECTIONS.forEach(([id]) => {
      const el = document.getElementById(id);
      if (el) obs.observe(el);
    });
    return () => obs.disconnect();
  }, []);

  const go = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });

  return (
    <>
      <motion.div className="bar" style={{ scaleX: width, width: '100%' }} />

      <nav className="dots">
        {SECTIONS.map(([id, label]) => (
          <button
            key={id}
            title={label}
            aria-label={label}
            className={`dot ${active === id ? 'on' : ''}`}
            onClick={() => go(id)}
          />
        ))}
      </nav>

      {/* ================= HERO ================= */}
      <header className="hero" id="hero">
        <div className="hero-aurora">
          <Aurora colorStops={['#6D28D9', '#E9B872', '#3B1F6B']} amplitude={1.15} blend={0.62} />
        </div>
        <div className="hero-fade" />
        <div className="hero-in">
          <div className="kick">Internship Project Report</div>
          <SplitText
            text="Diya"
            tag="h1"
            textAlign="left"
            delay={62}
            duration={1.15}
            splitType="chars"
            from={{ opacity: 0, y: 78, rotateX: -75 }}
            to={{ opacity: 1, y: 0, rotateX: 0 }}
          />
          <motion.div
            initial={{ opacity: 0, y: 26 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.72, ease: [0.22, 1, 0.36, 1] }}
          >
            <h2 style={{ fontWeight: 600, color: 'var(--lilac)', marginTop: 16 }}>
              An unattended<br />
              <GradientText colors={['#E9B872', '#F5D9A8', '#B4A9D6', '#E9B872']} animationSpeed={7}>
                meditation kiosk
              </GradientText>
            </h2>
            <div className="rule" />
            <p className="lede" style={{ maxWidth: '52ch' }}>
              A visitor is identified by their own phone, guided through a camera-observed session,
              and handed a report. Then the machine resets itself.
            </p>
            <div className="hero-meta">
              <div><b>[Your Name]</b> · [Institution]</div>
              <div>[Month Year – Month Year]</div>
              <div>Guide: [Mentor Name]</div>
            </div>
          </motion.div>
        </div>
        <div className="scrollcue">scroll<span /></div>
      </header>

      {/* ================= BRIEF ================= */}
      <section className="sec" id="brief">
        <Reveal><div className="kick">The brief</div></Reveal>
        <Reveal delay={0.05}>
          <h2>A visitor walks up.<br />Nobody is there to help them.</h2>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="lede" style={{ marginTop: 30 }}>
            A museum kiosk has to identify a stranger, run a camera-guided meditation session,
            hand them a personal report, and reset itself — unattended, all day.
          </p>
        </Reveal>
        <div className="grid g4" style={{ marginTop: 58 }}>
          <Card n="01" title="No staff" delay={0.04}>
            Nobody is present to check anyone in, or to restart anything that stops.
          </Card>
          <Card n="02" title="No keyboard" delay={0.1}>
            A shared touchscreen that strangers type on needs cleaning between visitors.
          </Card>
          <Card n="03" title="No scanner" delay={0.16}>
            Dedicated reader hardware is cost, procurement and one more thing that breaks.
          </Card>
          <Card n="04" title="Never closed" delay={0.22}>
            An unattended machine that crashes and stays down is worth nothing at all.
          </Card>
        </div>
      </section>

      {/* ================= SCOPE ================= */}
      <section className="sec" id="scope">
        <Reveal><div className="kick">Scope</div></Reveal>
        <Reveal delay={0.05}><h2>Two teams, one thin seam</h2></Reveal>
        <div className="grid g2" style={{ marginTop: 56 }}>
          <Card n="HARDWARE TEAM · IITH" title="Cameras, servos, CV" delay={0.04}>
            Depth and thermal capture, posture and gaze analysis, and the external
            meditation-app that produces the report PDF.
          </Card>
          <Card n="MINE" title="Everything around it" hi delay={0.12}>
            The kiosk application, the identification system, the backend and web pages,
            packaging and deployment — and the contract between the two sides.
          </Card>
        </div>
        <Reveal delay={0.18}>
          <div className="callout">
            <p>
              <b>The seam is two primitives, not a protocol.</b> I launch one shell script and
              read one PDF off disk. They changed their internals all summer without ever
              breaking my app.
            </p>
          </div>
        </Reveal>
      </section>

      {/* ================= PROBLEM ================= */}
      <section className="sec" id="problem">
        <Reveal><div className="kick">The hard part</div></Reveal>
        <div style={{ maxWidth: '20ch' }}>
          <ScrollReveal baseOpacity={0.08} enableBlur blurStrength={5} baseRotation={4}>
            How do you identify someone with no scanner?
          </ScrollReveal>
        </div>
        <Reveal delay={0.1}>
          <p className="lede" style={{ marginTop: 26 }}>
            Every obvious answer costs hardware — a QR reader, a card reader, or a keyboard
            that strangers share.
          </p>
        </Reveal>
      </section>

      {/* ================= ATTEMPTS ================= */}
      <section className="sec" id="attempts">
        <Reveal><div className="kick">Design evolution</div></Reveal>
        <Reveal delay={0.05}><h2>Three attempts</h2></Reveal>
        <div className="grid g3" style={{ marginTop: 58 }}>
          <Card n="01" title="Data in the QR" delay={0.04}
            mono="DIYA1:<base64 json>">
            The printed code carried the visitor's details. Fully offline — but it still needs a
            reader, and it puts personal data on paper.
          </Card>
          <Card n="02" title="QR holds an id" delay={0.11}
            mono="GET /api/visitors/:id">
            The code became a lookup key and the kiosk fetched details over the API.
            Better privacy; the scanner problem remained.
          </Card>
          <Card n="03 · SHIPPED" title="Invert it" hi delay={0.18}
            mono="POST /api/sessions">
            The kiosk shows the QR and the visitor's phone scans it. The phone is the scanner,
            the camera and the keyboard. Zero hardware.
          </Card>
        </div>
      </section>

      {/* ================= INVERSION ================= */}
      <section className="sec" id="inversion">
        <div className="split">
          <div>
            <Reveal><div className="kick">The decision that mattered</div></Reveal>
            <Reveal delay={0.05}><h2>The phone is the scanner</h2></Reveal>
            <Reveal delay={0.1}>
              <p className="lede" style={{ marginTop: 26 }}>
                The kiosk asks the backend for a session, renders the token as a QR, and polls.
                The visitor's own phone does the reading.
              </p>
            </Reveal>
            <Reveal delay={0.15}>
              <div className="chips">
                <div className="chip m">POST /api/sessions</div>
                <div className="chip m">GET /api/sessions/:token</div>
                <div className="chip m">POST /api/claim</div>
              </div>
            </Reveal>
            <Reveal delay={0.2}>
              <div className="callout">
                <p>A constraint produced a simpler design than a budget would have.</p>
              </div>
            </Reveal>
          </div>
          <Reveal delay={0.12} y={50}>
            <TiltedCard
              imageSrc="shots/app-01-idle-qr.png"
              altText="The kiosk displaying its own session QR code"
              captionText="The kiosk shows the code — the phone reads it"
              containerHeight="430px"
              containerWidth="100%"
              imageHeight="430px"
              imageWidth="100%"
              rotateAmplitude={11}
              scaleOnHover={1.04}
              showMobileWarning={false}
              showTooltip
            />
          </Reveal>
        </div>
      </section>

      {/* ================= FLOW ================= */}
      <section className="sec" id="flow">
        <Reveal><div className="kick">End to end</div></Reveal>
        <Reveal delay={0.05}><h2>Four stages, one API</h2></Reveal>
        <div className="grid g4" style={{ marginTop: 54 }}>
          <Card n="STAGE 01" title="Identify" delay={0.04}
            mono={'GET /api/people/:token'}>
            An admin roster gives each person a private link. They open it on their phone and
            scan the kiosk.
          </Card>
          <Card n="STAGE 02" title="Claim" delay={0.1}
            mono={'POST /api/claim'}>
            The backend links that identity to the kiosk's open session. The polling kiosk
            advances by itself.
          </Card>
          <Card n="STAGE 03" title="Session" hi delay={0.16}
            mono={'bash scripts/run1.sh'}>
            The kiosk launches the CV pipeline and blocks. This boundary is deliberately
            not an API.
          </Card>
          <Card n="STAGE 04" title="Report" delay={0.22}
            mono={'PDFium -> images'}>
            The newest PDF written after the session began is rendered in-app, then the
            kiosk resets.
          </Card>
        </div>
        <Reveal delay={0.16}>
          <figure style={{ marginTop: 52 }}>
            <img className="wide" src="shots/diagram-timeline-slide.png"
              alt="Timeline of the interaction between phone, kiosk, backend and meditation-app" />
            <figcaption className="cap">
              <b>Kiosk to Backend</b> is the only network boundary — plain REST over HTTPS.
              <b> Kiosk to meditation-app</b> is a local process and a file on disk, so there is
              no protocol to break.
            </figcaption>
          </figure>
        </Reveal>
      </section>

      {/* ================= WIREFRAMES ================= */}
      <section className="sec" id="wireframes">
        <Reveal><div className="kick">Design process</div></Reveal>
        <Reveal delay={0.05}><h2>Wireframes, and what they got wrong</h2></Reveal>
        <Reveal delay={0.1}>
          <p className="lede" style={{ marginTop: 26 }}>
            Annotated before building. Two of the notes are flaws I only saw once it was
            running — they are marked as such rather than quietly fixed in the drawing.
          </p>
        </Reveal>
        <div className="grid g2" style={{ marginTop: 50 }}>
          {[
            ['wf-01', 'Idle. The QR owns the screen; everything else is deliberately quiet.'],
            ['wf-02', 'Identified. Notes 5 and 6 are real defects — stale controls and split status.'],
            ['wf-03', 'Report overlay, full-bleed so the desktop never shows between visitors.'],
            ['wf-04', 'The phone side: three taps, no app install, no typing.'],
          ].map(([f, cap], i) => (
            <Reveal key={f} delay={0.05 * i} y={40}>
              <figure>
                <img className="wide" src={`wf/${f}.png`} alt={cap} />
                <figcaption className="cap">{cap}</figcaption>
              </figure>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ================= GALLERY ================= */}
      <section className="sec" id="gallery">
        <Reveal><div className="kick">Running system</div></Reveal>
        <Reveal delay={0.05}><h2>Every screen, for real</h2></Reveal>
        <Reveal delay={0.1}>
          <p className="lede" style={{ marginTop: 26 }}>
            Captured from the running application and the live web pages — not mockups.
          </p>
        </Reveal>

        <div className="grid g2" style={{ marginTop: 50 }}>
          <Reveal y={40}>
            <figure>
              <img className="shot" src="shots/app-02-authenticated.png" alt="Kiosk showing the identified visitor" />
              <figcaption className="cap">
                <b>Identified.</b> Name, email and roster photo arrive from the claim; the session
                starts with no button press.
              </figcaption>
            </figure>
          </Reveal>
          <Reveal delay={0.08} y={40}>
            <figure>
              <img className="shot" src="shots/app-03-session-running.png" alt="Kiosk during the session" />
              <figcaption className="cap">
                <b>Session running.</b> The live status line is the pipeline's own stdout, stripped
                of colour codes.
              </figcaption>
            </figure>
          </Reveal>
        </div>

        <Reveal delay={0.06} y={40}>
          <figure style={{ marginTop: 34 }}>
            <img className="shot" src="shots/app-04-report.png" alt="Report rendered inside the kiosk" />
            <figcaption className="cap">
              <b>Report.</b> The PDF is decoded by PDFium and rendered inside the app — no external
              viewer, and the desktop is never exposed.
            </figcaption>
          </figure>
        </Reveal>

        <Reveal delay={0.05}>
          <h3 style={{ marginTop: 78, marginBottom: 30 }}>The web side</h3>
        </Reveal>
        <div className="grid g3">
          <Reveal y={36}>
            <figure>
              <img className="phoneshot" src="shots/web-02-login.png" alt="Per-person login page on a phone" />
              <figcaption className="cap"><b>Private link.</b> Greets the person by name. Returns name and role only — never Aadhaar or email.</figcaption>
            </figure>
          </Reveal>
          <Reveal delay={0.08} y={36}>
            <figure>
              <img className="phoneshot" src="shots/web-01-register.png" alt="Visitor self-registration on a phone" />
              <figcaption className="cap"><b>Self-registration.</b> The session-aware fallback when someone is not on the roster.</figcaption>
            </figure>
          </Reveal>
          <Reveal delay={0.16} y={36}>
            <figure>
              <img className="phoneshot" style={{ maxWidth: '100%' }} src="shots/web-03-admin.png" alt="Admin roster upload with parsed preview" />
              <figcaption className="cap"><b>Admin roster.</b> XLSX parsed in the browser, Aadhaar masked in the preview.</figcaption>
            </figure>
          </Reveal>
        </div>
      </section>

      {/* ================= STACK ================= */}
      <section className="sec" id="stack">
        <Reveal><div className="kick">Under the hood</div></Reveal>
        <Reveal delay={0.05}><h2>Three parts I built</h2></Reveal>
        <div className="grid g3" style={{ marginTop: 54 }}>
          <Card n="KIOSK APP" title="C# · .NET 8 · Avalonia" delay={0.04}>
            The only .NET UI framework that officially supports Linux. Ships as a
            self-contained single-file .deb for two architectures.
          </Card>
          <Card n="BACKEND" title="Node · Express · Postgres" delay={0.11}>
            Sessions, visitors and the admin roster, serving the web pages from the same
            origin so the phone camera gets HTTPS.
          </Card>
          <Card n="WEB" title="Three static pages" delay={0.18}>
            Phone registration, admin roster upload with in-browser XLSX parsing, and the
            per-person login scanner.
          </Card>
        </div>
        <Reveal delay={0.1}>
          <div className="chips">
            {['QRCoder', 'PDFtoImage / PDFium', 'SkiaSharp', 'SheetJS', 'html5-qrcode', 'systemd', 'Render', 'QuestPDF-free'].map((c) => (
              <div className="chip m" key={c}>{c}</div>
            ))}
          </div>
        </Reveal>
        <div className="stats">
          {[
            [8, 'source files in the kiosk app', ''],
            [9, 'API endpoints', ''],
            [3, 'Postgres tables', ''],
            [2, 'architectures packaged', ''],
          ].map(([n, l], i) => (
            <Reveal key={l} delay={0.06 * i}>
              <div className="stat">
                <div className="statn"><CountUp to={n} duration={1.6} /></div>
                <div className="statl">{l}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ================= TESTING ================= */}
      <section className="sec" id="testing">
        <div className="split">
          <div>
            <Reveal><div className="kick">Testing</div></Reveal>
            <Reveal delay={0.05}><h2>Building it without the hardware</h2></Reveal>
            <Reveal delay={0.1}>
              <p className="lede" style={{ marginTop: 26 }}>
                For most of the internship there were no cameras and no meditation-app. The flow
                still had to be testable end to end.
              </p>
            </Reveal>
            <Reveal delay={0.15}>
              <div className="callout">
                <p>
                  Two environment variables swap the pipeline for a mock. <b>No test code inside
                  the app</b>, nothing extra in the shipped package — and those same variables are
                  the real production override.
                </p>
              </div>
            </Reveal>
            <Reveal delay={0.2}>
              <p className="small" style={{ marginTop: 26 }}>
                It also surfaced a real bug: “show the newest PDF” would quietly hand a visitor
                their predecessor’s report. Now only a file newer than the session start is accepted.
              </p>
            </Reveal>
          </div>
          <Reveal delay={0.12} y={44}>
            <div className="term">
              <div className="termbar">
                <i style={{ background: '#FF5F57' }} /><i style={{ background: '#FEBC2E' }} /><i style={{ background: '#28C840' }} />
              </div>
              <div className="termbody">
                <div><span className="p">$</span> export DIYA_PIPELINE_SCRIPT=<span className="k">…/run1.mock.sh</span></div>
                <div><span className="p">$</span> export DIYA_REPORT_DIR=<span className="k">/tmp/diya-reports</span></div>
                <div><span className="p">$</span> diya-meditation</div>
                <div style={{ height: 18 }} />
                <div className="ok">Calibrating cameras…</div>
                <div className="ok">Running meditation session…</div>
                <div className="ok">Running t3 (PDF report)…</div>
                <div className="ok">All tasks completed successfully.</div>
                <div style={{ height: 12 }} />
                <div className="c"># login → session → report → thank-you</div>
                <div className="c"># on any Linux desktop, no cameras</div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ================= SHIPPING ================= */}
      <section className="sec" id="shipping">
        <Reveal><div className="kick">Shipping</div></Reveal>
        <Reveal delay={0.05}><h2>One command each</h2></Reveal>
        <div className="grid g3" style={{ marginTop: 54 }}>
          <Card n="BUILD" title="A single package" delay={0.04}
            mono="./deploy/build-deb.sh 1.6.0 amd64">
            Self-contained .deb for amd64 and arm64. The museum machine needs nothing
            pre-installed — not even .NET.
          </Card>
          <Card n="LOCK DOWN" title="A kiosk, not an app" delay={0.11}
            mono="Restart=always">
            A systemd user service restarts it on crash, autologin brings it up on boot, and the
            GNOME escape shortcuts are disabled.
          </Card>
          <Card n="DEPLOY" title="Backend in one file" delay={0.18}
            mono="render.yaml">
            A blueprint provisions the web service and Postgres together, then tracks main
            on every merge.
          </Card>
        </div>
        <Reveal delay={0.16}>
          <div className="callout">
            <p>
              Plus documentation written for whoever comes next: an overview, a full command
              reference, an FAQ, and a handoff note that records the <b>dead ends</b> so nobody
              repeats them.
            </p>
          </div>
        </Reveal>
      </section>

      {/* ================= ROADMAP ================= */}
      <section className="sec" id="roadmap">
        <Reveal><div className="kick">What comes next</div></Reveal>
        <Reveal delay={0.05}><h2>Where I handed it over</h2></Reveal>
        <Reveal delay={0.1}>
          <p className="lede" style={{ marginTop: 26 }}>
            The full path works today: roster upload, phone login, automatic session, report on
            screen, reset. Four things are queued for whoever continues.
          </p>
        </Reveal>
        <div className="grid g4" style={{ marginTop: 54 }}>
          <Card n="01" title="Personalise the report" delay={0.04}>
            Pass the visitor into the pipeline so the PDF is theirs rather than generic.
          </Card>
          <Card n="02" title="Bound the pipeline" delay={0.1}>
            A timeout and a failure screen, so a dead camera cannot strand the kiosk.
          </Card>
          <Card n="03" title="Consent screen" delay={0.16}>
            Cameras observe visitors and identity data is stored. It needs asking first.
          </Card>
          <Card n="04" title="Real CV hardware" delay={0.22}>
            The interfaces are in place; the devices arrive after my internship ends.
          </Card>
        </div>
      </section>

      {/* ================= CLOSE ================= */}
      <section className="sec" id="close" style={{ minHeight: '86vh' }}>
        <Reveal>
          <h2 style={{ maxWidth: '24ch' }}>
            Someone can walk up, log in with their phone, and leave with their report.
          </h2>
        </Reveal>
        <Reveal delay={0.08}><div className="rule" /></Reveal>
        <Reveal delay={0.12}>
          <p className="lede">
            The vision hardware is the remaining milestone. Everything I could not finish is
            written down.
          </p>
        </Reveal>
        <Reveal delay={0.2}>
          <h3 style={{ marginTop: 56, color: 'var(--gold)' }}>Thank you — questions?</h3>
        </Reveal>
      </section>

      <footer className="footer">
        Diya Meditation Kiosk · internship report<br />
        Screenshots are captured from the running application. The report PDF shown is
        representative — the real one is produced by the hardware team’s meditation-app.<br />
        Animated components from <a href="https://reactbits.dev" style={{ color: 'var(--gold)' }}>React Bits</a>.
      </footer>
    </>
  );
}
