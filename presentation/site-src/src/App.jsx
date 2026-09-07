import { useCallback, useEffect, useState } from 'react';

import Grainient from './reactbits/Grainient';

/* Seven slides. White and black, like the kiosk app itself, over a blue
   Grainient background. Arrow keys / space move between slides. */
const SLIDES = [
  ['title', 'Title'],
  ['intro', 'What I did'],
  ['qr', 'QR system'],
  ['flow', 'The flow'],
  ['issues', 'Problems'],
  ['demo', 'Full demo'],
  ['thanks', 'Thank you'],
];

function Slide({ id, n, children, className = '' }) {
  return (
    <section id={id} className={`slide ${className}`}>
      <div className="slide-body">{children}</div>
      <div className="slide-foot">
        <span className="slide-brand">Diya · Meditation Kiosk</span>
        <span className="slide-num">{n} / 7</span>
      </div>
    </section>
  );
}

/* An image that prefers `primary` and silently falls back to `fallback`.
   Used for the report shot: drop a file in at shots/real-report.png and it is
   picked up automatically, with no code change and no rebuild needed. */
function Shot({ primary, fallback, alt, className = '' }) {
  const [src, setSrc] = useState(primary);
  return (
    <img
      className={className}
      src={src}
      alt={alt}
      onError={() => setSrc(current => (current === fallback ? current : fallback))}
    />
  );
}

/* A video that falls back to a still image, and always prints as the still. */
function Clip({ src, still, alt, className = '', ...rest }) {
  const [failed, setFailed] = useState(false);
  return (
    <div className={`clip ${className}`}>
      {failed ? (
        <img src={still} alt={alt} />
      ) : (
        <video src={src} poster={still} onError={() => setFailed(true)} {...rest} />
      )}
      <img className="print-still" src={still} alt={alt} />
    </div>
  );
}

export default function App() {
  const [active, setActive] = useState(0);

  const go = useCallback(i => {
    const next = Math.max(0, Math.min(i, SLIDES.length - 1));
    document.getElementById(SLIDES[next][0])?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = SLIDES.findIndex(([id]) => id === e.target.id);
        if (i >= 0) setActive(i);
      }),
      { threshold: 0.55 },
    );
    SLIDES.forEach(([id]) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const onKey = e => {
      if (['ArrowDown', 'ArrowRight', 'PageDown', ' '].includes(e.key)) {
        e.preventDefault();
        go(active + 1);
      } else if (['ArrowUp', 'ArrowLeft', 'PageUp'].includes(e.key)) {
        e.preventDefault();
        go(active - 1);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [active, go]);

  return (
    <>
      <div className="backdrop" aria-hidden="true">
        <Grainient
          color1="#FF9FFC"
          color2="#5227FF"
          color3="#B497CF"
          timeSpeed={0.25}
          colorBalance={0}
          warpStrength={1}
          warpFrequency={5}
          warpSpeed={2}
          warpAmplitude={50}
          blendAngle={0}
          blendSoftness={0.05}
          rotationAmount={500}
          noiseScale={2}
          grainAmount={0.32}
          grainScale={2}
          grainAnimated={false}
          contrast={1.15}
          gamma={2.4}
          saturation={0.62}
          centerX={0}
          centerY={0}
          zoom={0.9}
        />
      </div>

      <nav className="rail" aria-label="Slides">
        {SLIDES.map(([id, label], i) => (
          <button
            key={id}
            className={i === active ? 'on' : ''}
            onClick={() => go(i)}
            title={label}
            aria-label={label}
          />
        ))}
      </nav>

      <main>
        {/* 1 — TITLE */}
        <Slide id="title" n={1} className="title-slide">
          <p className="kicker">Internship Project Report</p>
          <h1>Diya</h1>
          <p className="sub">An unattended meditation kiosk</p>
          <div className="line" />
          <div className="who">
            <div>
              <span>Presented by</span>
              <b>Ayush Gupta</b>
            </div>
            <div>
              <span>Under the guidance of</span>
              <b>Eshwar Teja</b>
              <small>Mentor</small>
            </div>
          </div>
        </Slide>

        {/* 2 — WHAT I DID */}
        <Slide id="intro" n={2}>
          <p className="kicker">Introduction</p>
          <h2>What I worked on</h2>
          <p className="lede">
            A visitor walks up to a kiosk with nobody there to help them. My work was everything
            around the experience: identifying the visitor, running their session, and handing back
            a report — then resetting for the next person.
          </p>
          <div className="cards">
            <div className="card">
              <span className="tag">01</span>
              <h3>The kiosk application</h3>
              <p>A fullscreen desktop app in C# and .NET with Avalonia, running on Linux.</p>
            </div>
            <div className="card">
              <span className="tag">02</span>
              <h3>Phone-based identification</h3>
              <p>A backend and web pages so a visitor is identified using only their own phone.</p>
            </div>
            <div className="card">
              <span className="tag">03</span>
              <h3>Hardware integration</h3>
              <p>Connecting to the other team's application without touching their code.</p>
            </div>
            <div className="card">
              <span className="tag">04</span>
              <h3>Packaging and deployment</h3>
              <p>A single installable package that boots straight into the kiosk and restarts itself.</p>
            </div>
          </div>
        </Slide>

        {/* 3 — QR SYSTEM (big video) */}
        <Slide id="qr" n={3} className="qr-slide">
          <div className="qr-grid">
            <div className="qr-copy">
              <p className="kicker">The QR code system</p>
              <h2>The kiosk shows the code. The phone reads it.</h2>
              <p className="lede">
                There was no scanner hardware, so I inverted it. The kiosk asks the backend for a
                session and displays it as a QR code. The visitor's phone scans that code, and the
                kiosk — which is polling the backend — moves ahead on its own.
              </p>
              <ul className="ticks">
                <li>No scanner, no app install, no typing</li>
                <li>The phone is the camera and the keyboard</li>
                <li>Phone and kiosk never talk directly — only through the backend</li>
              </ul>
            </div>
            <div className="qr-media">
              <figure className="phone-frame">
                <Clip
                  className="phone"
                  src="clips/scan-phone.mp4"
                  still="shots/real-scan.png"
                  alt="A phone scanning the QR code shown on the kiosk"
                  autoPlay
                  muted
                  loop
                  controls
                  playsInline
                  preload="auto"
                />
                <figcaption>The scan itself, on the real setup</figcaption>
              </figure>
              <figure className="phone-frame">
                <img className="web-shot" src="shots/real-greeting.png" alt="The website open on the visitor's phone during the live run, greeting them by name before they scan" />
                <figcaption>The site greets them, then opens the camera</figcaption>
              </figure>
            </div>
          </div>
        </Slide>

        {/* 4 — THE FLOW */}
        <Slide id="flow" n={4}>
          <p className="kicker">End to end</p>
          <h2>The whole flow</h2>
          <div className="pipeline">
            {[
              ["Visitor's phone", '01', 'Identify', 'They open their private link and scan the kiosk.', 'GET /api/people/:token'],
              ['Backend', '02', 'Claim', "The person is tied to the kiosk's waiting session.", 'POST /api/claim'],
              ['Kiosk app', '03', 'Session', 'It starts the camera pipeline and waits.', 'bash scripts/run1.sh'],
              ['Meditation app', '04', 'Report', 'It writes a PDF. The kiosk spots it and draws it.', 'newest *.pdf -> PDFium'],
            ].map(([actor, n, title, copy, code]) => (
              <div className="stage" key={n}>
                <span className="actor">{actor}</span>
                <span className="stage-n">{n}</span>
                <h3>{title}</h3>
                <p>{copy}</p>
                <code>{code}</code>
              </div>
            ))}

            <figure className="report-shot">
              <Shot
                primary="shots/real-report.png"
                fallback="shots/app-04-report.png"
                alt="The finished report rendered inside the kiosk"
              />
              <figcaption>What the visitor is handed</figcaption>
            </figure>

            <div className="bnd rest">
              <b>01 — 02</b>
              <span>REST over HTTPS. The phone and the kiosk only ever talk to the backend, never to each other.</span>
            </div>
            <div className="bnd local">
              <b>03 — 04</b>
              <span>A launched process and a file on disk — deliberately not an API.</span>
            </div>
          </div>
          <p className="flow-note">
            Nobody presses a button to begin. Being identified is what starts the session.
          </p>
        </Slide>

        {/* 5 — PROBLEMS */}
        <Slide id="issues" n={5}>
          <p className="kicker">Problems I had to solve</p>
          <h2>Two real problems</h2>
          <div className="problems">
            <div className="problem">
              <span className="tag">Problem 01</span>
              <h3>Identifying someone with no scanner</h3>
              <p>
                Every obvious answer needed hardware — a QR reader, a card reader, or a keyboard
                strangers would share. I tried putting the visitor's data in the QR code, then
                putting an ID in it, and both still needed a reader.
              </p>
              <div className="fix">
                <b>Approach</b>
                Turn it around: the kiosk displays the QR and the visitor's phone does the scanning.
                The constraint made the design simpler.
              </div>
            </div>
            <div className="problem">
              <span className="tag">Problem 02</span>
              <h3>Talking to another team's app without changing it</h3>
              <p>
                The meditation software shipped as a separate <span className="mono">.deb</span>{' '}
                application. It had no API to call, and I could not modify it — it kept changing
                on their side all summer.
              </p>
              <div className="fix">
                <b>Approach</b>
                My app launches their program and then simply watches the folder. It keeps checking
                whether the report PDF has been created, and only accepts a file newer than the
                moment the session started — so nobody gets the previous visitor's report. Once the
                file appears, the kiosk renders it.
              </div>
            </div>
          </div>
          <div className="note">
            One process to launch and one file to watch — so their internals could change freely
            without ever breaking my application.
          </div>
        </Slide>

        {/* 6 — FULL DEMO */}
        <Slide id="demo" n={6} className="demo-slide">
          <div className="demo-head">
            <div>
              <p className="kicker">See it run</p>
              <h2>The full walkthrough</h2>
            </div>
            <p className="lede">
              Recorded on the real setup: the phone logs in, scans the kiosk, and the session begins
              on its own.
            </p>
          </div>
          <Clip
            className="feature"
            src="video/demo.mp4"
            still="shots/app-02-authenticated.png"
            alt="Full walkthrough of the Diya kiosk"
            controls
            playsInline
            preload="metadata"
          />
        </Slide>

        {/* 7 — THANKS */}
        <Slide id="thanks" n={7} className="thanks-slide">
          <p className="kicker">Thank you</p>
          <h2>Thanks for the opportunity</h2>
          <p className="lede">
            This internship taught me a great deal. I got to work in C# and .NET, build a real
            desktop application with Avalonia, write a backend and web pages, package software for
            Linux, and integrate with hardware I did not control. All of it will help me going
            forward.
          </p>
          <div className="thanks-grid">
            <div className="thanks-card">
              <b>Eshwar Teja</b>
              <p>For mentoring me through the project.</p>
            </div>
            <div className="thanks-card">
              <b>Kalyan Sir</b>
              <p>For his encouragement throughout.</p>
            </div>
          </div>
        </Slide>
      </main>
    </>
  );
}
