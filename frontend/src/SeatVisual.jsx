import React from 'react';

export function SeatVisual({ look, seat, material, color, onClick, compact = false }) {
  const seatName = seat?.name || 'Sport';
  const matName = material?.name || 'Leather';
  const colName = color?.name || 'Black';
  const colHex = color?.hex_code || look?.interior;
  let cushionColor = colHex || '#1e2026';
  if (cushionColor === '#101010' || cushionColor === '#080808' || cushionColor === '#111111' || cushionColor === '#000000') {
    cushionColor = '#252932';
  }
  const isRacing = /racing/i.test(seatName);
  const isLuxury = /luxury/i.test(seatName);
  const isCarbonMat = /carbon/i.test(matName);
  const isAlcantara = /alcantara/i.test(matName);

  return (
    <div 
      className={`seat-showcase ${compact ? 'compact' : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      title="Customize Interior & Seats"
      aria-label={`${seatName} Seat in ${matName} ${colName}`}
    >
      <div className="seat-badge">
        <span className="type">{seatName.toUpperCase()} SEAT</span>
        <span className="spec">{matName} · {colName}</span>
      </div>
      <svg viewBox="0 0 240 320" className="seat-svg" role="img">
        <defs>
          <linearGradient id="seatShade" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.25" />
            <stop offset="40%" stopColor="#ffffff" stopOpacity="0.05" />
            <stop offset="100%" stopColor="#000000" stopOpacity="0.65" />
          </linearGradient>
          <pattern id="carbonPattern" width="8" height="8" patternUnits="userSpaceOnUse">
            <rect width="4" height="4" fill="#202228" />
            <rect x="4" width="4" height="4" fill="#121316" />
            <rect y="4" width="4" height="4" fill="#121316" />
            <rect x="4" y="4" width="4" height="4" fill="#202228" />
          </pattern>
          <filter id="seatGlowBlur">
            <feGaussianBlur stdDeviation="6" />
          </filter>
        </defs>

        {/* Ambient Floor Shadow */}
        <ellipse cx="120" cy="298" rx="80" ry="14" fill="#000" opacity="0.65" filter="url(#seatGlowBlur)" />

        {/* Outer Backing Shell & Frame */}
        <path
          d="M 60 40 C 60 18, 180 18, 180 40 C 192 70, 208 135, 202 195 C 196 235, 186 272, 175 288 L 65 288 C 54 272, 44 235, 38 195 C 32 135, 48 70, 60 40 Z"
          fill={isRacing || isCarbonMat ? 'url(#carbonPattern)' : '#141519'}
          stroke="#2d313b"
          strokeWidth="3"
        />

        {/* Racing Harness Pass-through Openings */}
        {isRacing && (
          <g transform="translate(0, 10)">
            <rect x="80" y="62" width="30" height="14" rx="4" fill="#060608" stroke="#555" strokeWidth="2" />
            <rect x="130" y="62" width="30" height="14" rx="4" fill="#060608" stroke="#555" strokeWidth="2" />
            <path d="M 85 69 H 105 M 135 69 H 155" stroke="#ff2b2b" strokeWidth="3" strokeLinecap="round" />
          </g>
        )}

        {/* Headrest Cushion */}
        <path
          d="M 78 30 C 78 20, 162 20, 162 30 C 168 46, 164 68, 156 75 L 84 75 C 76 68, 72 46, 78 30 Z"
          fill={cushionColor}
          stroke="#0a0b0d"
          strokeWidth="2"
        />
        <path
          d="M 78 30 C 78 20, 162 20, 162 30 C 168 46, 164 68, 156 75 L 84 75 C 76 68, 72 46, 78 30 Z"
          fill="url(#seatShade)"
          opacity={isAlcantara ? 0.6 : 0.8}
        />

        {/* Headrest Logo */}
        <text x="120" y="52" textAnchor="middle" fontSize="10" fontWeight="800" letterSpacing="2" fill="#ffffff" opacity="0.75">
          VELOCITY
        </text>

        {/* Main Backrest Cushion */}
        <path
          d="M 74 82 L 166 82 C 176 120, 182 170, 174 216 L 66 216 C 58 170, 64 120, 74 82 Z"
          fill={cushionColor}
          stroke="#0e1014"
          strokeWidth="2.5"
        />
        <path
          d="M 74 82 L 166 82 C 176 120, 182 170, 174 216 L 66 216 C 58 170, 64 120, 74 82 Z"
          fill="url(#seatShade)"
          opacity={isAlcantara ? 0.5 : 0.75}
        />

        {/* Quilted / Stitching Accents */}
        {isLuxury ? (
          <g stroke="#ffffff" strokeOpacity="0.25" strokeWidth="1.2" fill="none">
            <path d="M 85 98 L 155 178 M 100 88 L 165 163 M 120 84 L 170 144 M 155 98 L 85 178 M 140 88 L 75 163 M 120 84 L 70 144" />
          </g>
        ) : (
          <g stroke="#000000" strokeOpacity="0.45" strokeWidth="2" fill="none">
            <path d="M 94 85 L 90 210 M 146 85 L 150 210 M 120 88 L 120 210" />
            <path d="M 94 85 L 90 210 M 146 85 L 150 210" stroke="#ffffff" strokeOpacity="0.2" strokeWidth="1" />
          </g>
        )}

        {/* Side Support Bolsters */}
        <path d="M 50 135 C 46 175, 56 218, 68 228 L 74 208 C 65 188, 60 158, 64 132 Z" fill={isRacing ? cushionColor : '#1b1d24'} stroke="#2a2d36" strokeWidth="1.5" />
        <path d="M 190 135 C 194 175, 184 218, 172 228 L 166 208 C 175 188, 180 158, 176 132 Z" fill={isRacing ? cushionColor : '#1b1d24'} stroke="#2a2d36" strokeWidth="1.5" />

        {/* Bottom Cushion Base */}
        <path
          d="M 54 220 C 54 210, 186 210, 186 220 C 196 245, 193 276, 179 286 L 61 286 C 47 276, 44 245, 54 220 Z"
          fill={cushionColor}
          stroke="#000"
          strokeWidth="2.5"
        />
        <path
          d="M 54 220 C 54 210, 186 210, 186 220 C 196 245, 193 276, 179 286 L 61 286 C 47 276, 44 245, 54 220 Z"
          fill="url(#seatShade)"
          opacity={isAlcantara ? 0.5 : 0.75}
        />

        {/* Center Thigh Cushion Pad */}
        <path
          d="M 74 230 C 74 224, 166 224, 166 230 C 172 254, 168 278, 158 283 L 82 283 C 72 278, 68 254, 74 230 Z"
          fill={cushionColor}
          stroke="#0a0b0d"
          strokeWidth="1.5"
        />

        {/* Seat Mounting Brackets */}
        <rect x="68" y="286" width="14" height="16" rx="2" fill="#242730" stroke="#111" strokeWidth="1.5" />
        <rect x="158" y="286" width="14" height="16" rx="2" fill="#242730" stroke="#111" strokeWidth="1.5" />
        <rect x="58" y="299" width="124" height="6" rx="3" fill="#121317" />
      </svg>
    </div>
  );
}
