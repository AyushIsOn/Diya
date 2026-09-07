import { useEffect, useState } from 'react';
import { motion, useScroll, useSpring } from 'motion/react';

import Aurora from './reactbits/Aurora';
import DecryptedText from './reactbits/DecryptedText';
import GlareHover from './reactbits/GlareHover';
import Particles from './reactbits/Particles';
import ShinyText from './reactbits/ShinyText';
import SpotlightCard from './reactbits/SpotlightCard';

const SECTIONS = [
  ['hero', 'Opening'],
  ['brief', 'Mission'],
  ['scope', 'Boundary'],
  ['problem', 'Constraint'],
  ['attempts', 'Evolution'],
  ['inversion', 'Breakthrough'],
  ['proof', 'Live proof'],
  ['flow', 'System flow'],
  ['interface', 'Kiosk'],
  ['field', 'Field evidence'],
  ['architecture', 'Architecture'],
  ['testing', 'Testing'],
  ['shipping', 'Shipping'],
  ['roadmap', 'Handover'],
  ['close', 'Close'],
];

const EASE = [0.22, 1, 0.36, 1];

function Reveal({ children, delay = 0, y = 36, className = '' }) {
  return (
    <motion.div
      className={`reveal ${className}`}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.18 }}
      transition={{ duration: 0.72, delay, ease: EASE }}
    >
      {children}
    </motion.div>
  );
}

function Eyebrow({ code, children }) {
  return (
    <div className="eyebrow">
      <span>{code}</span>
      <ShinyText text={children} speed={4} color="#ffb35c" shineColor="#fff3d7" spread={92} />
    </div>
  );
}

function Slide({ id, index, children, className = '' }) {
  return (
    <section id={id} className={`slide ${className}`} data-slide={String(index).padStart(2, '0')}>
      <div className="slide-no">{String(index).padStart(2, '0')} / 15</div>
      <div className="slide-grid" aria-hidden="true" />
      <div className="slide-inner">{children}</div>
    </section>
  );
}

function GlassCard({ code, title, children, accent = 'violet', className = '' }) {
  return (
    <SpotlightCard className={`glass-card ${accent} ${className}`} spotlightColor="rgba(255,179,92,.18)">
      <div className="card-code">{code}</div>
      <h3>{title}</h3>
      <p>{children}</p>
    </SpotlightCard>
  );
}

function Metric({ value, suffix = '', label }) {
  return (
    <div className="metric">
      <div className="metric-value">{value}{suffix}</div>
      <div className="metric-label">{label}</div>
    </div>
  );
}

function CodeLine({ children }) {
  return (
    <div className="code-line mono">
      <span>›</span>
      <DecryptedText
        text={children}
        animateOn="view"
        speed={22}
        maxIterations={12}
        sequential
        characters="ABCDEF0123456789/:._-"
      />
    </div>
  );
}

function DemoVideo() {
  const [failed, setFailed] = useState(false);

  return (
    <div className="demo-frame">
      <div className="demo-chrome"><i /><i /><i /><span>LIVE RUN / LOCAL CAPTURE</span></div>
      {!failed ? (
        <video controls preload="metadata" playsInline poster="shots/app-02-authenticated.png" onError={() => setFailed(true)}>
          <source src="video/demo.mp4" type="video/mp4" onError={() => setFailed(true)} />
        </video>
      ) : (
        <img src="shots/app-02-authenticated.png" alt="Diya authenticated visitor screen" />
      )}
      <img className="print-video" src="shots/app-02-authenticated.png" alt="Diya authenticated visitor screen" />
    </div>
  );
}

function AppChrome({ active, go, progress }) {
  return (
    <>
      <motion.div className="progress" style={{ scaleX: progress }} />
      <header className="chrome">
        <button className="brand" onClick={() => go('hero')} aria-label="Back to opening">
          <span className="brand-mark">D</span>
          <span><b>DIYA</b><small>MEDITATION KIOSK</small></span>
        </button>
        <div className="chrome-status"><i /> SYSTEM CASE STUDY</div>
        <button className="print-button" onClick={() => window.print()}>EXPORT PDF ↗</button>
      </header>
      <nav className="rail" aria-label="Presentation sections">
        {SECTIONS.map(([id, label], i) => (
          <button key={id} className={active === id ? 'active' : ''} onClick={() => go(id)} aria-label={`Go to ${label}`}>
            <span>{String(i + 1).padStart(2, '0')}</span><b>{label}</b>
          </button>
        ))}
      </nav>
    </>
  );
}

export default function App() {
  const [active, setActive] = useState('hero');
  const { scrollYProgress } = useScroll();
  const progress = useSpring(scrollYProgress, { stiffness: 120, damping: 28, restDelta: 0.001 });

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => entries.forEach(entry => entry.isIntersecting && setActive(entry.target.id)),
      { rootMargin: '-42% 0px -42% 0px' },
    );
    SECTIONS.forEach(([id]) => {
      const node = document.getElementById(id);
      if (node) observer.observe(node);
    });
    return () => observer.disconnect();
  }, []);

  const go = id => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });

  return (
    <main>
      <AppChrome active={active} go={go} progress={progress} />

      <Slide id="hero" index={1} className="hero-slide">
        <div className="hero-aurora"><Aurora colorStops={['#6e39ff', '#ff7a45', '#ffc857']} amplitude={1.35} blend={0.6} /></div>
        <div className="hero-particles">
          <Particles particleCount={260} particleSpread={12} speed={0.045} particleColors={['#ffb35c', '#a38bff', '#ffffff']} alphaParticles particleBaseSize={64} sizeRandomness={1.3} cameraDistance={20} />
        </div>
        <div className="hero-copy">
          <Reveal><Eyebrow code="01 / EXPERIENCE">INTERNSHIP PROJECT REPORT</Eyebrow></Reveal>
          <Reveal delay={0.08} className="hero-title-wrap">
            <h1 className="hero-title"><span>DI</span><span>YA</span></h1>
          </Reveal>
          <Reveal delay={0.18}>
            <p className="hero-statement">A self-running meditation experience where the visitor’s phone becomes the kiosk’s missing hardware.</p>
          </Reveal>
          <Reveal delay={0.26}>
            <div className="hero-tags"><span>IDENTITY</span><span>COMPUTER VISION</span><span>ZERO-TOUCH FLOW</span></div>
          </Reveal>
        </div>
        <div className="diya-orbit" aria-hidden="true">
          <div className="orbit orbit-a"><i /></div>
          <div className="orbit orbit-b"><i /></div>
          <div className="orbit orbit-c" />
          <div className="flame"><span /></div>
          <div className="orbit-label label-a">PHONE</div>
          <div className="orbit-label label-b">KIOSK</div>
          <div className="orbit-label label-c">REPORT</div>
        </div>
        <div className="scroll-hint">SCROLL TO ENTER <i /></div>
      </Slide>

      <Slide id="brief" index={2} className="brief-slide">
        <div className="two-col lead-layout">
          <div>
            <Reveal><Eyebrow code="02 / MISSION">THE BRIEF</Eyebrow></Reveal>
            <Reveal delay={0.06}><h2>A visitor walks up.<br /><em>Nobody is there.</em></h2></Reveal>
            <Reveal delay={0.14}><p className="lede">The system must identify a stranger, run a camera-guided meditation, deliver a personal report, and reset itself—unattended, all day.</p></Reveal>
          </div>
          <div className="constraint-grid">
            <Reveal delay={0.06}><GlassCard code="C-01" title="No staff" accent="orange">No one is present to check visitors in or recover a stalled session.</GlassCard></Reveal>
            <Reveal delay={0.12}><GlassCard code="C-02" title="No keyboard">A shared input surface creates friction, hygiene, and accessibility problems.</GlassCard></Reveal>
            <Reveal delay={0.18}><GlassCard code="C-03" title="No scanner">Dedicated reader hardware adds cost, procurement, and another failure point.</GlassCard></Reveal>
            <Reveal delay={0.24}><GlassCard code="C-04" title="Always on" accent="cyan">A kiosk that crashes once and stays down is not an installation.</GlassCard></Reveal>
          </div>
        </div>
      </Slide>

      <Slide id="scope" index={3} className="scope-slide">
        <Reveal><Eyebrow code="03 / OWNERSHIP">THE SYSTEM BOUNDARY</Eyebrow></Reveal>
        <Reveal delay={0.06}><h2>Two teams.<br />One deliberately thin seam.</h2></Reveal>
        <div className="seam-map">
          <Reveal delay={0.12} className="seam-side">
            <div className="owner hardware">HARDWARE TEAM</div>
            <h3>Cameras · Servos · CV</h3>
            <p>Depth and thermal capture, posture and gaze analysis, and the external meditation application.</p>
            <div className="seam-list"><span>HOME1.py</span><span>SHOOT1.py</span><span>CHEST1.py</span><span>EYE1.py</span></div>
          </Reveal>
          <div className="seam-line" aria-hidden="true"><b>PROCESS</b><i /><b>PDF</b></div>
          <Reveal delay={0.18} className="seam-side owned">
            <div className="owner mine">MY SCOPE</div>
            <h3>Everything around it</h3>
            <p>Kiosk UI, identity flow, backend, web pages, packaging, deployment, and the contract between both sides.</p>
            <div className="seam-list"><span>AVALONIA</span><span>EXPRESS</span><span>POSTGRES</span><span>SYSTEMD</span></div>
          </Reveal>
        </div>
        <Reveal delay={0.24}><div className="thesis"><span>DESIGN DECISION</span> Launch one process. Read one file. Let both teams evolve independently.</div></Reveal>
      </Slide>

      <Slide id="problem" index={4} className="problem-slide">
        <div className="problem-noise" aria-hidden="true">NO SCANNER · NO SCANNER · NO SCANNER ·</div>
        <div className="problem-layout">
          <div>
            <Reveal><Eyebrow code="04 / CONSTRAINT">THE HARD PART</Eyebrow></Reveal>
            <Reveal delay={0.08}><h2>How do you identify someone with <em>nothing to scan them?</em></h2></Reveal>
            <Reveal delay={0.16}><p className="lede">Every obvious answer adds hardware: a QR reader, a card reader, or a shared keyboard.</p></Reveal>
          </div>
          <Reveal delay={0.14} className="scanner-void">
            <div className="void-ring"><span>?</span></div>
            <div className="void-caption mono">DEVICE_NOT_FOUND</div>
            <div className="crosshair a" /><div className="crosshair b" />
          </Reveal>
        </div>
      </Slide>

      <Slide id="attempts" index={5} className="attempts-slide">
        <Reveal><Eyebrow code="05 / ITERATION">DESIGN EVOLUTION</Eyebrow></Reveal>
        <Reveal delay={0.06}><h2>Three attempts.<br /><em>One inversion.</em></h2></Reveal>
        <div className="attempt-track">
          <Reveal delay={0.10} className="attempt rejected">
            <div className="attempt-mark">01</div><span className="status">REJECTED</span>
            <h3>Data inside the QR</h3><p>Offline, but personal data sits on paper and the kiosk still needs a reader.</p>
            <CodeLine>DIYA1:&lt;base64_json&gt;</CodeLine>
          </Reveal>
          <Reveal delay={0.16} className="attempt rejected">
            <div className="attempt-mark">02</div><span className="status">INCOMPLETE</span>
            <h3>QR as lookup ID</h3><p>Better privacy. Same physical scanner problem.</p>
            <CodeLine>GET /api/visitors/:id</CodeLine>
          </Reveal>
          <Reveal delay={0.22} className="attempt shipped">
            <div className="attempt-mark">03</div><span className="status">SHIPPED</span>
            <h3>Invert the interaction</h3><p>The kiosk shows the code. The visitor’s phone scans it. Zero added hardware.</p>
            <CodeLine>POST /api/claim</CodeLine>
          </Reveal>
        </div>
      </Slide>

      <Slide id="inversion" index={6} className="inversion-slide">
        <div className="inversion-bg"><Aurora colorStops={['#111827', '#6e39ff', '#ff7a45']} amplitude={1.1} blend={0.72} /></div>
        <Reveal><Eyebrow code="06 / BREAKTHROUGH">THE DECISION THAT MATTERED</Eyebrow></Reveal>
        <div className="inversion-layout">
          <div>
            <Reveal delay={0.06}><h2>The phone is<br /><em>the scanner.</em></h2></Reveal>
            <Reveal delay={0.14}><p className="lede">Move the QR from the person to the kiosk. The visitor already carries a camera, keyboard, display, and network connection.</p></Reveal>
            <Reveal delay={0.20}><blockquote>“A constraint produced a simpler design than a budget would have.”</blockquote></Reveal>
          </div>
          <Reveal delay={0.12} className="handoff-visual">
            <div className="device phone"><span className="device-top" /><img src="shots/real-scan.png" alt="Phone scanning the kiosk QR" /></div>
            <div className="signal"><i /><i /><i /><b>CLAIM</b></div>
            <div className="device kiosk"><span className="device-top" /><img src="shots/app-01-idle-qr.png" alt="Kiosk displaying a QR code" /></div>
          </Reveal>
        </div>
      </Slide>

      <Slide id="proof" index={7} className="proof-slide">
        <Reveal><Eyebrow code="07 / EVIDENCE">WATCH IT WORK</Eyebrow></Reveal>
        <div className="proof-head">
          <Reveal delay={0.06}><h2>The scan.<br /><em>On real hardware.</em></h2></Reveal>
          <Reveal delay={0.12}><p className="lede">The phone opens a private link, reads the kiosk, and the kiosk advances without a touch.</p></Reveal>
        </div>
        <div className="proof-grid">
          <Reveal delay={0.12} className="mini-video phone-video">
            <video src="clips/scan-phone.mp4" autoPlay muted loop playsInline preload="metadata" />
            <img className="print-video" src="shots/real-scan.png" alt="Phone scanning the QR" />
            <div><span>01</span><b>PHONE READS KIOSK</b></div>
          </Reveal>
          <Reveal delay={0.18} className="mini-video kiosk-video">
            <video src="clips/kiosk-authed.mp4" autoPlay muted loop playsInline preload="metadata" />
            <img className="print-video" src="shots/real-kiosk.png" alt="Kiosk after authentication" />
            <div><span>02</span><b>KIOSK RESPONDS</b></div>
          </Reveal>
          <Reveal delay={0.24} className="full-demo"><DemoVideo /></Reveal>
        </div>
      </Slide>

      <Slide id="flow" index={8} className="flow-slide">
        <Reveal><Eyebrow code="08 / SEQUENCE">END TO END</Eyebrow></Reveal>
        <Reveal delay={0.06}><h2>Four stages.<br /><em>One uninterrupted flow.</em></h2></Reveal>
        <div className="flow-track">
          {[
            ['01', 'IDENTIFY', 'Private roster link', 'GET /api/people/:token'],
            ['02', 'CLAIM', 'Bind person to kiosk', 'POST /api/claim'],
            ['03', 'SESSION', 'Launch CV pipeline', 'bash scripts/run1.sh'],
            ['04', 'REPORT', 'Render newest PDF', 'PDFium → images'],
          ].map(([n, title, copy, code], i) => (
            <Reveal key={n} delay={0.08 + i * 0.06} className="flow-node">
              <div className="flow-num">{n}</div><i />
              <h3>{title}</h3><p>{copy}</p><code>{code}</code>
            </Reveal>
          ))}
        </div>
        <Reveal delay={0.28}><div className="boundary-note"><b>NETWORK BOUNDARY</b><span>Phone ↔ Backend ↔ Kiosk</span><i /><b>LOCAL BOUNDARY</b><span>Process + filesystem</span></div></Reveal>
      </Slide>

      <Slide id="interface" index={9} className="interface-slide">
        <Reveal><Eyebrow code="09 / INTERFACE">THE KIOSK</Eyebrow></Reveal>
        <Reveal delay={0.05}><h2>Four states.<br /><em>No dead ends.</em></h2></Reveal>
        <div className="screen-stack">
          {[
            ['shots/app-01-idle-qr.png', '01', 'WAITING', 'Session QR owns the screen'],
            ['shots/app-02-authenticated.png', '02', 'IDENTIFIED', 'Identity resolves automatically'],
            ['shots/app-03-session-running.png', '03', 'RUNNING', 'Pipeline status streams live'],
            ['shots/app-04-report.png', '04', 'REPORT', 'PDF remains inside the kiosk'],
          ].map(([src, n, title, copy], i) => (
            <Reveal key={src} delay={0.08 + i * 0.06} className={`screen-card screen-${i + 1}`}>
              <img src={src} alt={`${title} kiosk state`} />
              <div><span>{n}</span><b>{title}</b><small>{copy}</small></div>
            </Reveal>
          ))}
        </div>
      </Slide>

      <Slide id="field" index={10} className="field-slide">
        <Reveal><Eyebrow code="10 / REALITY">FIELD EVIDENCE</Eyebrow></Reveal>
        <div className="field-layout">
          <div>
            <Reveal delay={0.06}><h2>Not mockups.<br /><em>Running screens.</em></h2></Reveal>
            <Reveal delay={0.12}><p className="lede">Captured from the live phone flow, kiosk application, and administration pages.</p></Reveal>
            <Reveal delay={0.18}><div className="field-proof"><span>7</span><p>real interfaces across the visitor, kiosk, and operator journey</p></div></Reveal>
          </div>
          <div className="evidence-wall">
            {[
              ['shots/real-greeting.png', 'PRIVATE GREETING'],
              ['shots/real-scan.png', 'CAMERA SCAN'],
              ['shots/real-kiosk.png', 'KIOSK CLAIM'],
              ['shots/web-02-login.png', 'PERSONAL LINK'],
              ['shots/web-01-register.png', 'FALLBACK SIGN-UP'],
              ['shots/web-03-admin.png', 'ROSTER ADMIN'],
            ].map(([src, label], i) => (
              <Reveal key={src} delay={0.05 * i} className="evidence-card"><img src={src} alt={label} /><span>{label}</span></Reveal>
            ))}
          </div>
        </div>
      </Slide>

      <Slide id="architecture" index={11} className="architecture-slide">
        <Reveal><Eyebrow code="11 / SYSTEM">ARCHITECTURE</Eyebrow></Reveal>
        <div className="architecture-layout">
          <div>
            <Reveal delay={0.05}><h2>Three products.<br /><em>One experience.</em></h2></Reveal>
            <div className="system-orbit">
              <div className="system-core">DIYA<small>SESSION</small></div>
              <div className="system-node node-kiosk"><b>KIOSK</b><span>C# · .NET 8 · Avalonia</span></div>
              <div className="system-node node-api"><b>BACKEND</b><span>Node · Express · Postgres</span></div>
              <div className="system-node node-web"><b>WEB</b><span>Registration · Scan · Admin</span></div>
            </div>
          </div>
          <div className="architecture-panel">
            <Reveal delay={0.10}><div className="metric-grid"><Metric value={8} label="kiosk source files" /><Metric value={9} label="API endpoints" /><Metric value={3} label="database tables" /><Metric value={2} label="CPU architectures" /></div></Reveal>
            <Reveal delay={0.18}>
              <div className="tech-stack mono">
                <span>QRCoder</span><span>PDFium</span><span>SkiaSharp</span><span>SheetJS</span><span>html5-qrcode</span><span>systemd</span>
              </div>
            </Reveal>
          </div>
        </div>
      </Slide>

      <Slide id="testing" index={12} className="testing-slide">
        <Reveal><Eyebrow code="12 / RESILIENCE">TESTING WITHOUT HARDWARE</Eyebrow></Reveal>
        <div className="testing-layout">
          <div>
            <Reveal delay={0.06}><h2>Swap the boundary.<br /><em>Keep the journey.</em></h2></Reveal>
            <Reveal delay={0.12}><p className="lede">For most of the build, the cameras and meditation application did not exist. Two environment variables made the entire journey testable.</p></Reveal>
            <Reveal delay={0.18}><div className="lesson"><b>BUG FOUND</b><p>“Newest PDF” could show the previous visitor’s report. The fix accepts only files created after the current session began.</p></div></Reveal>
          </div>
          <Reveal delay={0.12} className="terminal">
            <div className="terminal-bar"><i /><i /><i /><span>diya — mock pipeline</span></div>
            <div className="terminal-body mono">
              <p><b>$</b> export DIYA_PIPELINE_SCRIPT=<em>…/run1.mock.sh</em></p>
              <p><b>$</b> export DIYA_REPORT_DIR=<em>/tmp/diya-reports</em></p>
              <p><b>$</b> diya-meditation</p>
              <br />
              <p className="success">✓ Calibrating cameras</p>
              <p className="success">✓ Running meditation session</p>
              <p className="success">✓ Rendering fresh report</p>
              <p className="success">✓ Resetting kiosk</p>
              <br /><p className="comment"># same app · same flow · zero cameras</p>
            </div>
          </Reveal>
        </div>
      </Slide>

      <Slide id="shipping" index={13} className="shipping-slide">
        <Reveal><Eyebrow code="13 / DELIVERY">SHIPPING</Eyebrow></Reveal>
        <Reveal delay={0.06}><h2>From repository<br /><em>to unattended machine.</em></h2></Reveal>
        <div className="shipping-grid">
          {[
            ['01', 'BUILD', 'A single package', './deploy/build-deb.sh 1.6.0', 'Self-contained amd64 and arm64 packages. No .NET installation required.'],
            ['02', 'LOCK', 'A kiosk, not an app', 'Restart=always', 'Autostart, crash recovery, fullscreen enforcement, and disabled escape routes.'],
            ['03', 'DEPLOY', 'Backend as blueprint', 'render.yaml', 'Web service and Postgres provision together and track the repository.'],
          ].map(([n, tag, title, code, copy], i) => (
            <Reveal key={n} delay={0.08 + i * 0.08}>
              <GlareHover width="100%" height="100%" background="rgba(15,13,29,.92)" borderRadius="24px" borderColor="rgba(255,255,255,.1)" glareColor={i === 1 ? '#8f7cff' : '#ffb35c'} glareOpacity={0.18} className="ship-card">
                <div className="ship-top"><span>{n}</span><b>{tag}</b></div><h3>{title}</h3><code>{code}</code><p>{copy}</p>
              </GlareHover>
            </Reveal>
          ))}
        </div>
        <Reveal delay={0.28}><div className="delivery-line"><span>CODE</span><i /><span>PACKAGE</span><i /><span>BOOT</span><i /><span>RECOVER</span></div></Reveal>
      </Slide>

      <Slide id="roadmap" index={14} className="roadmap-slide">
        <Reveal><Eyebrow code="14 / HANDOVER">WHAT COMES NEXT</Eyebrow></Reveal>
        <Reveal delay={0.06}><h2>The path works today.<br /><em>The risks are explicit.</em></h2></Reveal>
        <div className="roadmap-grid">
          {[
            ['01', 'PERSONALISE', 'Pass visitor context into the report pipeline.'],
            ['02', 'TIME-BOUND', 'Add cancellation and a recovery screen for dead cameras.'],
            ['03', 'CONSENT', 'Ask before cameras observe and identity data is retained.'],
            ['04', 'INTEGRATE', 'Connect the production computer-vision hardware.'],
          ].map(([n, title, copy], i) => (
            <Reveal key={n} delay={0.08 + i * 0.06} className="roadmap-item"><span>{n}</span><div><h3>{title}</h3><p>{copy}</p></div></Reveal>
          ))}
        </div>
        <Reveal delay={0.28}><div className="handover-state"><i /> CURRENT STATE <b>END-TO-END FLOW OPERATIONAL</b></div></Reveal>
      </Slide>

      <Slide id="close" index={15} className="close-slide">
        <div className="close-aurora"><Aurora colorStops={['#ff7a45', '#6e39ff', '#ffc857']} amplitude={1.4} blend={0.64} /></div>
        <div className="close-particles"><Particles particleCount={180} particleSpread={11} speed={0.04} particleColors={['#ffb35c', '#8f7cff']} alphaParticles particleBaseSize={72} cameraDistance={20} /></div>
        <div className="close-content">
          <Reveal><Eyebrow code="15 / CLOSE">THE OUTCOME</Eyebrow></Reveal>
          <Reveal delay={0.08}><h2>Walk up.<br />Breathe.<br /><em>Leave with insight.</em></h2></Reveal>
          <Reveal delay={0.18}><p>A constraint became the interaction. The interaction became a system. The system now runs without a guide.</p></Reveal>
          <Reveal delay={0.26}><div className="questions">THANK YOU <span>QUESTIONS?</span></div></Reveal>
        </div>
        <div className="close-orb" aria-hidden="true"><i /><i /><i /><b>DIYA</b></div>
      </Slide>
    </main>
  );
}
