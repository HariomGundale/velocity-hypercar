"""Idempotent seed data. Run manually with `python -m app.db.seed`.

Only cars that have a real 3D model are served. To add a car: add it to CARS (+ its ENGINES/PACKAGES/AEROS),
drop `<slug>.glb` into assets/models/, and re-run the seed. Cars not listed in CARS are deactivated automatically."""
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db.database import Base, SessionLocal, engine
from app.models import (
    AeroPackage, Caliper, Car, Configuration, Engine, InteriorColor, InteriorMaterial,
    Paint, PerformancePackage, SeatType, Wheel,
)

CARS = [
    dict(
        name="Porsche 911 GT3 RS",
        slug="porsche-911-gt3-rs",
        base_price=35_000_000,
        horsepower=525,
        top_speed=296,
        acceleration=3.2,
        handling=98,
        braking=97,
        image_url="/assets/porsche-911-gt3-rs.png",
        description="Uncompromising track-bred sports car with naturally aspirated flat-six power, central radiator concept, and extreme active aerodynamics.",
    ),
    dict(
        name="Suzuki Swift",
        slug="suzuki-swift",
        base_price=849_000,
        horsepower=82,
        top_speed=165,
        acceleration=12.5,
        handling=72,
        braking=70,
        image_url="/assets/suzuki-swift.png",
        description="Light, nimble Japanese hatchback with a 1.2L three-cylinder petrol engine, efficient packaging and agile city handling.",
    ),
    dict(
        name="Ferrari 296 GTB",
        slug="ferrari-296-gtb",
        base_price=54_000_000,
        horsepower=830,
        top_speed=330,
        acceleration=2.9,
        handling=99,
        braking=98,
        image_url="/assets/ferrari-296-gtb.png",
        description="Mid-rear Berlinetta plug-in hybrid V6 with electric boost, active rear spoiler, and 830 hp of Italian track performance.",
    ),
    dict(
        name="Mercedes-Benz GLC 300e",
        slug="glc-300e",
        base_price=8_500_000,
        horsepower=313,
        top_speed=218,
        acceleration=6.7,
        handling=82,
        braking=84,
        image_url="/assets/glc-300e.png",
        description="Sophisticated luxury hybrid SUV with 4MATIC all-wheel drive, air suspension, and electric range capability.",
    ),
    dict(
        name="Lamborghini Huracán Tecnica",
        slug="lamborghini-huracan-tecnica",
        base_price=40_400_000,
        horsepower=640,
        top_speed=325,
        acceleration=3.2,
        handling=97,
        braking=96,
        image_url="/assets/lamborghini-huracan-tecnica.png",
        description="Naturally aspirated 5.2L V10 with rear-wheel steering, direct steering ratio, and aggressive aerodynamic downforce.",
    ),
    dict(
        name="Mercedes-Benz EQS 580",
        slug="eqs-580",
        base_price=16_000_000,
        horsepower=523,
        top_speed=210,
        acceleration=4.3,
        handling=86,
        braking=88,
        image_url="/assets/eqs-580.png",
        description="Ultra-luxury all-electric sedan featuring dual-motor 4MATIC AWD, hyperscreen dashboard, and whisper-quiet cabin comfort.",
    ),
    dict(
        name="Mazda 3",
        slug="mazda-3",
        base_price=2_800_000,
        horsepower=186,
        top_speed=216,
        acceleration=8.1,
        handling=80,
        braking=78,
        image_url="/assets/mazda-3.png",
        description="Sleek Japanese hatchback with Skyactiv-G 2.5L engine, G-Vectoring Control Plus, and premium interior trim.",
    ),
]

PAINTS = [
    dict(
        name="Obsidian Black",
        hex_code="#080808",
        price_modifier=0,
        category="solid",
    ),
    dict(
        name="Pearl White",
        hex_code="#F5F5F0",
        price_modifier=150_000,
        category="pearl",
    ),
    dict(
        name="Racing Red",
        hex_code="#C8102E",
        price_modifier=200_000,
        category="metallic",
    ),
    dict(
        name="Electric Blue",
        hex_code="#0A5CFF",
        price_modifier=250_000,
        category="metallic",
    ),
    dict(
        name="Neon Green",
        hex_code="#39FF14",
        price_modifier=300_000,
        category="special",
    ),
]

WHEELS = [
    dict(
        name="Aero",
        description="Closed-face aero wheels for reduced drag.",
        price_modifier=100_000,
    ),
    dict(
        name="Carbon",
        description="Lightweight full carbon-fibre wheels.",
        price_modifier=450_000,
    ),
    dict(
        name="Forged",
        description="Forged alloy wheels with a classic multi-spoke design.",
        price_modifier=300_000,
    ),
    dict(
        name="Performance",
        description="Track-focused wheels with a wide contact patch.",
        price_modifier=200_000,
    ),
]

CALIPERS = [
    dict(
        name="Red",
        hex_code="#D00000",
        price_modifier=25_000,
    ),
    dict(
        name="Yellow",
        hex_code="#FFD60A",
        price_modifier=25_000,
    ),
    dict(
        name="Blue",
        hex_code="#1E6FFF",
        price_modifier=25_000,
    ),
    dict(
        name="Black",
        hex_code="#111111",
        price_modifier=0,
    ),
]

MATERIALS = [
    dict(
        name="Leather",
        description="Hand-stitched premium leather.",
        price_modifier=200_000,
    ),
    dict(
        name="Alcantara",
        description="Grippy suede-like microfibre.",
        price_modifier=350_000,
    ),
    dict(
        name="Carbon",
        description="Exposed carbon-fibre with minimal trim.",
        price_modifier=600_000,
    ),
]

INTERIOR_COLORS = [
    dict(
        name="Black",
        hex_code="#101010",
        price_modifier=0,
    ),
    dict(
        name="White",
        hex_code="#F2F2F2",
        price_modifier=0,
    ),
    dict(
        name="Red",
        hex_code="#B3122B",
        price_modifier=50_000,
    ),
    dict(
        name="Tan",
        hex_code="#B08968",
        price_modifier=50_000,
    ),
]

SEATS = [
    dict(
        name="Sport",
        description="Supportive everyday sport seats.",
        price_modifier=0,
    ),
    dict(
        name="Racing",
        description="Fixed-back carbon racing shells with harness points.",
        price_modifier=250_000,
    ),
    dict(
        name="Luxury",
        description="Heated, ventilated, massaging comfort seats.",
        price_modifier=400_000,
    ),
]

ENGINES = [
    dict(
        car_slug="porsche-911-gt3-rs",
        name="4.0L Naturally Aspirated Flat-Six",
        description="High-revving atmospheric 4.0L six-cylinder boxer producing 525 hp at 9,000 RPM.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="porsche-911-gt3-rs",
        name="4.0L Flat-Six Weissach Power Spec",
        description="Lightweight titanium valvetrain and sport exhaust delivering 545 hp.",
        price_modifier=1_800_000,
        horsepower_modifier=20,
        top_speed_modifier=4,
        acceleration_modifier=-0.1,
        handling_modifier=1,
        braking_modifier=0,
    ),
    dict(
        car_slug="suzuki-swift",
        name="1.2L Z-Series Three-Cylinder",
        description="Standard 1.2L three-cylinder petrol engine producing 82 hp.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="suzuki-swift",
        name="1.2L Z-Series Sport Tune",
        description="Remapped ECU and free-flow intake for 88 hp and sharper response.",
        price_modifier=45_000,
        horsepower_modifier=6,
        top_speed_modifier=4,
        acceleration_modifier=-0.4,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="ferrari-296-gtb",
        name="3.0L Twin-Turbo 120° V6 Hybrid",
        description="PHEV architecture combining twin-turbo V6 with MGU-K axial flux motor producing 830 hp.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="ferrari-296-gtb",
        name="Assetto Fiorano Power Spec V6",
        description="Titanium exhaust and race ECU map unlocking 850 hp with active boost logic.",
        price_modifier=2_800_000,
        horsepower_modifier=20,
        top_speed_modifier=5,
        acceleration_modifier=-0.1,
        handling_modifier=2,
        braking_modifier=0,
    ),
    dict(
        car_slug="glc-300e",
        name="2.0L Turbo Inline-4 Plug-in Hybrid",
        description="PHEV powertrain with 136 hp electric motor producing 313 hp combined.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="glc-300e",
        name="AMG Performance Hybrid Tune",
        description="AMG tuned ECU and battery discharge curve delivering 335 hp.",
        price_modifier=420_000,
        horsepower_modifier=22,
        top_speed_modifier=6,
        acceleration_modifier=-0.3,
        handling_modifier=1,
        braking_modifier=0,
    ),
    dict(
        car_slug="lamborghini-huracan-tecnica",
        name="5.2L Naturally Aspirated V10",
        description="High-revving 5.2L atmospheric V10 delivering 640 hp at 8,000 RPM.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="lamborghini-huracan-tecnica",
        name="5.2L V10 Squadra Corse Spec",
        description="Titanium valves and free-flowing exhaust pushing 660 hp with track acoustics.",
        price_modifier=2_200_000,
        horsepower_modifier=20,
        top_speed_modifier=4,
        acceleration_modifier=-0.1,
        handling_modifier=2,
        braking_modifier=0,
    ),
    dict(
        car_slug="eqs-580",
        name="Dual Permanently Excited Synchronous Motors",
        description="Dual motor 4MATIC electric drive producing 523 hp and 855 Nm torque.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="eqs-580",
        name="AMG Electric Power Boost",
        description="Inverter overclock delivering 560 hp with launch control boost.",
        price_modifier=850_000,
        horsepower_modifier=37,
        top_speed_modifier=10,
        acceleration_modifier=-0.3,
        handling_modifier=1,
        braking_modifier=0,
    ),
    dict(
        car_slug="mazda-3",
        name="2.5L Skyactiv-G Four-Cylinder",
        description="Naturally aspirated 2.5L 4-cylinder petrol engine with 186 hp.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="mazda-3",
        name="2.5L Skyactiv-Turbo Engine",
        description="Dynamic pressure turbocharger delivering 227 hp and 420 Nm torque.",
        price_modifier=350_000,
        horsepower_modifier=41,
        top_speed_modifier=14,
        acceleration_modifier=-1.2,
        handling_modifier=2,
        braking_modifier=0,
    ),
]

PACKAGES = [
    dict(
        car_slug="porsche-911-gt3-rs",
        name="Clubsport Package",
        description="Track-ready road calibration with steel roll-cage prep.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="porsche-911-gt3-rs",
        name="Weissach Package",
        description="Carbon-weave anti-roll bars, magnesium suspension components, and track brakes.",
        price_modifier=3_500_000,
        horsepower_modifier=50,
        top_speed_modifier=5,
        acceleration_modifier=-0.1,
        handling_modifier=8,
        braking_modifier=8,
    ),
    dict(
        car_slug="suzuki-swift",
        name="Standard City Setup",
        description="Comfort-focused road calibration.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="suzuki-swift",
        name="Sport Handling Package",
        description="Stiffer springs, front strut brace and upgraded brake pads.",
        price_modifier=60_000,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=6,
        braking_modifier=4,
    ),
    dict(
        car_slug="ferrari-296-gtb",
        name="Standard Berlinetta Setup",
        description="Factory adaptive suspension and electronic side slip control (eSSC).",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="ferrari-296-gtb",
        name="Assetto Fiorano Performance Package",
        description="Multimatic GT-race dampers, carbon front bumper appendages, and carbon door panels (-15kg).",
        price_modifier=4_500_000,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=-0.1,
        handling_modifier=8,
        braking_modifier=6,
    ),
    dict(
        car_slug="glc-300e",
        name="Avantgarde Comfort Line",
        description="Agility control suspension with selective damping.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="glc-300e",
        name="AMG Line Dynamic Package",
        description="Sports suspension, perforated front brake discs, and sport steering.",
        price_modifier=480_000,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=5,
        braking_modifier=5,
    ),
    dict(
        car_slug="lamborghini-huracan-tecnica",
        name="Standard Tecnica Dynamic Control",
        description="LDVI (Lamborghini Dinamica Veicolo Integrata) with rear wheel steering.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="lamborghini-huracan-tecnica",
        name="Track Telemetry & Carbon Ceramic Spec",
        description="Carbon ceramic brake cooling ducts and track telemetry system.",
        price_modifier=2_600_000,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=7,
        braking_modifier=9,
    ),
    dict(
        car_slug="eqs-580",
        name="Electric Art Executive Package",
        description="Airmatic air suspension with rear-axle 4.5° steering.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="eqs-580",
        name="AMG Line Executive Ride",
        description="Rear-axle 10° steering upgrade with lowered sport air suspension.",
        price_modifier=650_000,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=6,
        braking_modifier=4,
    ),
    dict(
        car_slug="mazda-3",
        name="Standard Drive Calibration",
        description="Skyactiv vehicle dynamics with G-Vectoring Control.",
        price_modifier=0,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=0.0,
        handling_modifier=0,
        braking_modifier=0,
    ),
    dict(
        car_slug="mazda-3",
        name="AWD Sport Package",
        description="i-Activ AWD system with stiffer rear sway bar.",
        price_modifier=180_000,
        horsepower_modifier=0,
        top_speed_modifier=0,
        acceleration_modifier=-0.2,
        handling_modifier=6,
        braking_modifier=3,
    ),
]

AEROS = [
    dict(
        car_slug="porsche-911-gt3-rs",
        name="Standard GT3 RS Aero",
        description="Factory carbon swan-neck rear wing and front diffuser blades.",
        price_modifier=0,
        downforce=0,
        drag=0,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="porsche-911-gt3-rs",
        name="Active DRS Aero Package",
        description="Hydraulic Drag Reduction System (DRS) with active upper wing flap and underfloor diffuser flaps.",
        price_modifier=900_000,
        downforce=30,
        drag=10,
        handling_modifier=8,
        top_speed_modifier=-3,
    ),
    dict(
        car_slug="suzuki-swift",
        name="Standard Bodywork",
        description="Factory bodywork with roof-end spoiler.",
        price_modifier=0,
        downforce=0,
        drag=0,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="suzuki-swift",
        name="Sport Body Kit",
        description="Front lip, side skirts and rear under-spoiler.",
        price_modifier=40_000,
        downforce=4,
        drag=1,
        handling_modifier=2,
        top_speed_modifier=-1,
    ),
    dict(
        car_slug="ferrari-296-gtb",
        name="Active Tea-Tray Rear Spoiler",
        description="Integrated active rear spoiler inspired by LaFerrari generating 360 kg downforce at 250 km/h.",
        price_modifier=0,
        downforce=36,
        drag=8,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="ferrari-296-gtb",
        name="High-Downforce Assetto Aero Kit",
        description="Extended carbon front splitter, high-load active spoiler extension, and rear carbon diffuser.",
        price_modifier=1_200_000,
        downforce=50,
        drag=14,
        handling_modifier=7,
        top_speed_modifier=-2,
    ),
    dict(
        car_slug="glc-300e",
        name="Standard SUV Aerodynamics",
        description="Aerodynamically optimized underbody panels and roof spoiler.",
        price_modifier=0,
        downforce=0,
        drag=0,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="glc-300e",
        name="AMG Aerodynamics Package",
        description="Front apron with larger air intakes and roof spoiler lip.",
        price_modifier=150_000,
        downforce=8,
        drag=2,
        handling_modifier=2,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="lamborghini-huracan-tecnica",
        name="Fixed Rear Wing Tecnica Aero",
        description="Fixed rear wing improving rear downforce by 35% with reduced drag.",
        price_modifier=0,
        downforce=35,
        drag=6,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="lamborghini-huracan-tecnica",
        name="High-Downforce Track Aero",
        description="Front splitter with front wheel arch deflectors and underbody diffuser.",
        price_modifier=850_000,
        downforce=48,
        drag=12,
        handling_modifier=6,
        top_speed_modifier=-2,
    ),
    dict(
        car_slug="eqs-580",
        name="Streamlined Bow Design (Cd 0.20)",
        description="Ultra-low drag coefficient 0.20 body shape with automated flush door handles.",
        price_modifier=0,
        downforce=0,
        drag=0,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="eqs-580",
        name="AMG Rear Spoiler Lip & Aero Wheels",
        description="Discreet AMG spoiler lip and underbody air deflectors.",
        price_modifier=220_000,
        downforce=10,
        drag=3,
        handling_modifier=3,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="mazda-3",
        name="Kodo Design Aerodynamics",
        description="Smooth Kodo body contours with integrated rear roof lip.",
        price_modifier=0,
        downforce=0,
        drag=0,
        handling_modifier=0,
        top_speed_modifier=0,
    ),
    dict(
        car_slug="mazda-3",
        name="Aero Kit Package",
        description="Gloss black front air dam, side sill extensions, and rear diffuser.",
        price_modifier=95_000,
        downforce=6,
        drag=1,
        handling_modifier=2,
        top_speed_modifier=0,
    ),
]


def _ensure_schema(db: Session) -> None:
    """Ensure car_id column exists on option tables if running on an existing SQLite DB."""
    tables = [
        "paints", "wheels", "calipers", "interior_materials",
        "interior_colors", "seat_types", "engines", "performance_packages", "aero_packages",
    ]
    for table in tables:
        try:
            res = db.execute(text(f"PRAGMA table_info({table})")).fetchall()
            columns = [r[1] for r in res]
            if columns and "car_id" not in columns:
                db.execute(text(f"ALTER TABLE {table} ADD COLUMN car_id INTEGER REFERENCES cars(id)"))
                db.commit()
        except Exception:
            pass


def _cleanup_fictional_data(db: Session) -> None:
    """Safely remove or deactivate legacy fictional cars and options."""
    # Fictional cars
    for slug in ("vortex-x1", "apex-r", "phantom-gt"):
        old_car = db.scalar(select(Car).where(Car.slug == slug))
        if old_car:
            has_cfg = db.scalar(select(Configuration.id).where(Configuration.car_id == old_car.id))
            if has_cfg:
                old_car.is_active = False
            else:
                db.delete(old_car)

    # Legacy fictional options if unreferenced
    legacy_options = {
        Engine: ("V8", "V10", "V12", "Hybrid"),
        PerformancePackage: ("Street", "Track", "Race"),
        AeroPackage: ("Stock", "Sport", "Extreme"),
    }
    for model, names in legacy_options.items():
        fk = {
            Engine: Configuration.engine_id,
            PerformancePackage: Configuration.performance_package_id,
            AeroPackage: Configuration.aero_package_id,
        }[model]
        for opt in db.scalars(select(model).where(model.name.in_(names))).all():
            has_cfg = db.scalar(select(Configuration.id).where(fk == opt.id))
            if has_cfg:
                opt.is_active = False
            else:
                db.delete(opt)

    db.flush()


def _sync_active_cars(db: Session) -> None:
    """Serve exactly the cars listed in CARS; deactivate the rest (kept, not deleted, so saved builds still resolve)."""
    served = {c["slug"] for c in CARS}
    for car in db.scalars(select(Car)).all():
        car.is_active = car.slug in served
    db.flush()


def _seed_table(db: Session, model, rows: list[dict], key: str = "name") -> int:
    existing = set(db.scalars(select(getattr(model, key))).all())
    created = 0
    for row in rows:
        if row[key] not in existing:
            db.add(model(**row))
            created += 1
    return created


def seed_database(db: Session) -> int:
    """Insert missing seed rows and link vehicle options. Safe to call repeatedly."""
    _ensure_schema(db)
    _cleanup_fictional_data(db)

    total = 0
    total += _seed_table(db, Car, CARS, key="slug")
    db.flush()
    _sync_active_cars(db)

    car_slug_to_id = {c.slug: c.id for c in db.scalars(select(Car)).all()}

    def _prepare_rows(row_list: list[dict]) -> list[dict]:
        prepared = []
        for r in row_list:
            item = dict(r)
            if "car_slug" in item:
                slug = item.pop("car_slug")
                item["car_id"] = car_slug_to_id.get(slug)
            prepared.append(item)
        return prepared

    for model, rows in (
        (Paint, PAINTS),
        (Wheel, WHEELS),
        (Caliper, CALIPERS),
        (InteriorMaterial, MATERIALS),
        (InteriorColor, INTERIOR_COLORS),
        (SeatType, SEATS),
        (Engine, _prepare_rows(ENGINES)),
        (PerformancePackage, _prepare_rows(PACKAGES)),
        (AeroPackage, _prepare_rows(AEROS)),
    ):
        total += _seed_table(db, model, rows)

    db.commit()
    return total


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        print(f"Seeded {seed_database(session)} new rows.")
