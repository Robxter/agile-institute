/** Logotipo Agile Institute con el lema "leading human revolution". */
export function Logo() {
  return (
    <svg viewBox="0 0 172 48" width="172" height="48" role="img" aria-label="Agile Institute™ · leading human revolution">
      <g fill="#0b3a4a">
        {/* figura */}
        <circle cx="12" cy="9" r="3.4" fill="#1fa3a3" />
        <path d="M2 15.5c5-2.2 15-2.2 20 0" stroke="#1685b8" strokeWidth="3" fill="none" strokeLinecap="round" />
        <path d="M12 14v18M7 32l5-8 5 8" stroke="#0b3a4a" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <text x="24" y="31" fontFamily="'Montserrat Variable', Montserrat, sans-serif" fontWeight="700" fontSize="24" letterSpacing="-1">
          Agile
        </text>
        <text x="81" y="16" fontFamily="'Montserrat Variable', Montserrat, sans-serif" fontWeight="600" fontSize="7">
          ™
        </text>
        <text x="3" y="45" fontFamily="'Montserrat Variable', Montserrat, sans-serif" fontWeight="600" fontSize="8.2" letterSpacing="2.4">
          INSTITUTE
        </text>
      </g>
      <path d="M95 8v36" stroke="#0b3a4a" strokeWidth="1" opacity=".5" />
      <g fill="#6f7377" fontFamily="'Montserrat Variable', Montserrat, sans-serif" fontWeight="500" fontSize="10">
        <text x="102" y="18">leading</text>
        <text x="102" y="30">human</text>
        <text x="102" y="42">revolution</text>
      </g>
    </svg>
  );
}
