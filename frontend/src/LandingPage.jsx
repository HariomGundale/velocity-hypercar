import React, { useState } from 'react';
import CarVisual from './CarVisual.jsx';
import * as C from './catalog.js';

const { short, inr, byId } = C;

export function LandingPage({ cars, opts, onConfigure, go }) {
  const primaryCar = cars.find(c => c.slug === 'porsche-911-gt3-rs') || cars[0];
  const [selectedCarId, setSelectedCarId] = useState(primaryCar.id);
  const currentCar = cars.find(c => c.id === selectedCarId) || primaryCar;

  // Selection state for landing page interactive hero
  const [heroSel, setHeroSel] = useState(() => ({
    ...C.defaultSelection(primaryCar.id, opts),
    paint_id: C.pickPaint(opts, /red/i).id,
  }));

  const co = C.optionsForCar(opts, currentCar.id);
  const look = C.makeLook(opts, heroSel);

  const handleSelectCar = (id) => {
    setSelectedCarId(id);
    setHeroSel(C.defaultSelection(id, opts));
  };

  const scrollToExplore = () => {
    document.getElementById('explore-machines')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <main className="landing">
      {/* SECTION 1: HERO EXPERIENCE */}
      <section className="hero-section">
        <div className="hero-bg-glow" style={{ '--p': look.body }} />
        <div className="hero-content">
          <div className="hero-tag">
            <span className="dot-pulse" /> NEXT-GEN HYPERCAR CONFIGURATOR
          </div>
          <h1 className="hero-headline">
            YOUR GARAGE.<br />
            <span className="hero-highlight">YOUR RULES.</span>
          </h1>
          <p className="hero-subhead">
            Experience bespoke automotive engineering. Customize performance powertrains, 
            active aerodynamics, and tailored bucket seats with server-validated calculations.
          </p>
          <div className="hero-actions">
            <button className="btn dark hero-btn-pri" onClick={() => onConfigure(currentCar.id)}>
              ENTER THE GARAGE
            </button>
            <button className="btn hero-btn-sec" onClick={scrollToExplore}>
              EXPLORE MACHINES ↓
            </button>
          </div>
        </div>

        {/* 3D Showcase Viewport */}
        <div className="hero-stage-container">
          <div className="hero-car-viewport">
            <CarVisual car={currentCar} look={look} />
          </div>

          {/* Quick Hero Customization Controls */}
          <div className="hero-quick-bar">
            <div className="hero-bar-group">
              <span className="bar-label">SELECT MACHINE</span>
              <div className="hero-car-pills">
                {cars.map(c => (
                  <button
                    key={c.id}
                    className={`car-pill ${selectedCarId === c.id ? 'active' : ''}`}
                    onClick={() => handleSelectCar(c.id)}
                  >
                    {c.name}
                  </button>
                ))}
              </div>
            </div>

            <div className="hero-bar-group">
              <span className="bar-label">BODY PAINT</span>
              <div className="hero-color-row">
                {co.paints.map(p => (
                  <button
                    key={p.id}
                    className={`color-dot ${heroSel.paint_id === p.id ? 'active' : ''}`}
                    title={p.name}
                    onClick={() => setHeroSel(s => ({ ...s, paint_id: p.id }))}
                  >
                    <span style={{ background: p.hex_code }} />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 2: EXPLORE THE MACHINES */}
      <section id="explore-machines" className="machines-section">
        <div className="section-header">
          <span className="section-lbl">CURATED FLEET</span>
          <h2>EXPLORE THE MACHINES</h2>
          <p>Every vehicle in our catalog is backed by real server-side specs, physics, and options.</p>
        </div>

        <div className="machines-grid">
          {cars.map(c => {
            const cSel = C.defaultSelection(c.id, opts);
            const cLook = C.makeLook(opts, cSel);
            return (
              <article key={c.id} className="machine-card">
                <div className="card-stage">
                  <CarVisual car={c} look={cLook} compact />
                  <span className="card-price-tag">FROM {short(c.base_price)}</span>
                </div>
                <div className="card-info">
                  <h3>{c.name}</h3>
                  <p className="card-desc">{c.description}</p>
                  <div className="card-specs-row">
                    <div><b>{c.horsepower}</b><span>HP</span></div>
                    <div><b>{c.top_speed}</b><span>KM/H</span></div>
                    <div><b>{c.acceleration}s</b><span>0–100</span></div>
                  </div>
                  <button className="btn dark card-cta" onClick={() => onConfigure(c.id)}>
                    CONFIGURE {c.name.toUpperCase()}
                  </button>
                </div>
              </article>
            );
          })}
        </div>
      </section>

      {/* SECTION 3: THE CUSTOMIZATION EXPERIENCE */}
      <section className="features-section">
        <div className="section-header">
          <span className="section-lbl">ENGINEERING & STYLING</span>
          <h2>BESPOKE CUSTOMIZATION</h2>
          <p>Modify every dimension of your vehicle with real-time performance calculation.</p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feat-num">01</div>
            <h3>Exterior Aesthetics & Paint</h3>
            <p>Select from solid, metallic, pearl, and special paints paired with customizable caliper finishes.</p>
            <div className="feat-preview-swatches">
              {opts.paints.slice(0, 5).map(p => (
                <span key={p.id} className="fswatch" style={{ background: p.hex_code }} title={p.name} />
              ))}
            </div>
          </div>

          <div className="feature-card">
            <div className="feat-num">02</div>
            <h3>Seat & Interior Architecture</h3>
            <p>Customize Sport, Racing Bucket, or Luxury comfort seats with hand-stitched leather and carbon weaves.</p>
            <div className="feat-preview-swatches">
              {opts.interior_colors.map(c => (
                <span key={c.id} className="fswatch" style={{ background: c.hex_code }} title={c.name} />
              ))}
            </div>
          </div>

          <div className="feature-card">
            <div className="feat-num">03</div>
            <h3>Powertrains & Aero Kits</h3>
            <p>Upgrade to high-revving flat-six, hybrid V6, or ECU sport tunes with active DRS aerodynamics.</p>
            <div className="feat-badge-row">
              <span className="fbadge">ACTIVE DRS</span>
              <span className="fbadge">ASSETTO FIORANO</span>
              <span className="fbadge">WEISSACH SPEC</span>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 4: HOW IT WORKS */}
      <section className="journey-section">
        <div className="section-header">
          <span className="section-lbl">THE JOURNEY</span>
          <h2>HOW IT WORKS</h2>
        </div>

        <div className="steps-container">
          <div className="step-item">
            <div className="step-circle">1</div>
            <h4>Choose Your Vehicle</h4>
            <p>Browse our catalog of hypercars and sports performance models.</p>
          </div>
          <div className="step-arrow">→</div>

          <div className="step-item">
            <div className="step-circle">2</div>
            <h4>Customize Specs & Seats</h4>
            <p>Select paints, wheels, calipers, powertrain tunes, and bucket seats.</p>
          </div>
          <div className="step-arrow">→</div>

          <div className="step-item">
            <div className="step-circle">3</div>
            <h4>Calculate Performance</h4>
            <p>Server verifies all choices and calculates exact price, HP, top speed, and braking.</p>
          </div>
          <div className="step-arrow">→</div>

          <div className="step-item">
            <div className="step-circle">4</div>
            <h4>Save & Share Build ID</h4>
            <p>Store builds in your virtual garage and generate a shareable Build ID.</p>
          </div>
        </div>
      </section>

      {/* SECTION 5: FINAL CTA */}
      <section className="cta-section">
        <div className="cta-box">
          <span className="cta-lbl">START YOUR AUTOMOTIVE VISION</span>
          <h2>READY TO ENTER THE GARAGE?</h2>
          <p>Build, save, and share your hypercar configuration today.</p>
          <button className="btn dark cta-btn" onClick={() => onConfigure(primaryCar.id)}>
            START CONFIGURATION NOW
          </button>
        </div>
      </section>

      {/* SECTION 6: FOOTER */}
      <footer className="landing-footer">
        <div className="footer-top">
          <div className="footer-brand">
            <span className="flogo">VELOCITY</span>
            <p>Hypercar Configurator & Virtual Garage</p>
          </div>
          <div className="footer-nav">
            <a href="#/models">MODELS</a>
            <a href="#/configure">CONFIGURATOR</a>
            <a href="#/garage">MY GARAGE</a>
          </div>
        </div>
        <div className="footer-btm">
          <span>© 2026 VELOCITY Hypercar System. All rights reserved.</span>
          <span>Crafted with Three.js & FastAPI</span>
        </div>
      </footer>
    </main>
  );
}
