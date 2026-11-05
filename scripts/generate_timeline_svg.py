#!/usr/bin/env python3
import os

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" width="860" height="376" viewBox="0 0 860 376">
  <defs>
    <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3FB950" />
      <stop offset="100%" stop-color="#A371F7" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <style>
    .font-mono { font-family: 'JetBrains Mono', -apple-system, BlinkMacSystemFont, monospace; }
  </style>

  <rect width="860" height="376" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="1.2" />

  <line x1="60" y1="44" x2="780" y2="44" stroke="#21262D" stroke-width="3" stroke-linecap="round" />
  <line x1="60" y1="44" x2="770" y2="44" stroke="url(#lineGrad)" stroke-width="3" stroke-linecap="round" filter="url(#glow)" />
  <polygon points="782,44 770,39 770,49" fill="#A371F7" />

  <g>
    <rect x="135" y="14" width="160" height="20" rx="10" fill="#162F1E" stroke="#3FB950" stroke-width="0.8" />
    <text x="215" y="27.5" class="font-mono" font-size="9" font-weight="700" fill="#3FB950" text-anchor="middle">AUG 2025 — SEP 2025</text>
    <circle cx="215" cy="44" r="7" fill="#0D1117" stroke="#3FB950" stroke-width="2.5" />
    <circle cx="215" cy="44" r="3" fill="#3FB950" />
  </g>

  <g>
    <rect x="565" y="14" width="160" height="20" rx="10" fill="#2E1B4E" stroke="#A371F7" stroke-width="0.8" />
    <text x="645" y="27.5" class="font-mono" font-size="9" font-weight="700" fill="#A371F7" text-anchor="middle">JUL 2026 — SEP 2026</text>
    <circle cx="645" cy="44" r="7" fill="#0D1117" stroke="#A371F7" stroke-width="2.5" />
    <circle cx="645" cy="44" r="3" fill="#A371F7" />
  </g>

  <g>
    <rect x="24" y="66" width="385" height="290" rx="8" fill="#161B22" stroke="#30363D" stroke-width="1" />
    <text x="42" y="90" class="font-mono" font-size="12.5" font-weight="700" fill="#FFFFFF">📡 Project Trainee</text>
    <text x="42" y="106" class="font-mono" font-size="10" font-weight="600" fill="#3FB950">Tata Communications  ·  Pune, India</text>
    <line x1="42" y1="114" x2="391" y2="114" stroke="#21262D" stroke-width="1" />

    <text x="42" y="132" class="font-mono" font-size="9.5" font-weight="700" fill="#58A6FF">▸ Automated Incident Management (AIMS)</text>
    <text x="50" y="147" class="font-mono" font-size="9" fill="#8B949E">Analyzed requirements &amp; designed RESTful endpoints</text>
    <text x="50" y="161" class="font-mono" font-size="9" fill="#8B949E">integrating New Relic alerts with ServiceNow.</text>
    <text x="50" y="175" class="font-mono" font-size="9" fill="#8B949E">Covered ingestion, deduplication &amp; status sync</text>
    <text x="50" y="189" class="font-mono" font-size="9" fill="#8B949E">to completely remove manual triage steps.</text>

    <text x="42" y="212" class="font-mono" font-size="9.5" font-weight="700" fill="#3FB950">▸ Operational Impact &amp; Staffing</text>
    <text x="50" y="227" class="font-mono" font-size="9" fill="#8B949E">Reported deployment readiness &amp; system metrics.</text>
    <text x="50" y="241" class="font-mono" font-size="9" fill="#8B949E">Positioned solution to reduce NOC triage staffing</text>
    <text x="50" y="255" class="font-mono" font-size="9" font-weight="700" fill="#3FB950">from 5 engineers to 1 upon full deployment.</text>

    <text x="42" y="278" class="font-mono" font-size="9.5" font-weight="700" fill="#E3B341">▸ Real-time Alert Telemetry</text>
    <text x="50" y="293" class="font-mono" font-size="9" fill="#8B949E">Engineered automated webhook event processing</text>
    <text x="50" y="307" class="font-mono" font-size="9" fill="#8B949E">with structured error recovery &amp; SLA audits.</text>
  </g>

  <g>
    <rect x="425" y="66" width="415" height="290" rx="8" fill="#161B22" stroke="#30363D" stroke-width="1" />
    <text x="443" y="90" class="font-mono" font-size="12.5" font-weight="700" fill="#FFFFFF">🤖 AI Engineer Intern</text>
    <text x="443" y="106" class="font-mono" font-size="10" font-weight="600" fill="#A371F7">Rtifact  ·  Remote / Bengaluru</text>
    <line x1="443" y1="114" x2="822" y2="114" stroke="#21262D" stroke-width="1" />

    <text x="443" y="132" class="font-mono" font-size="9.5" font-weight="700" fill="#58A6FF">▸ Issue Grounding:</text>
    <text x="548" y="132" class="font-mono" font-size="9.5" fill="#C9D1D9">Python/FastAPI engine</text>
    <text x="451" y="146" class="font-mono" font-size="9" fill="#8B949E">Maps issues &amp; stack traces to file:function:line</text>
    <text x="451" y="159" class="font-mono" font-size="9" font-weight="700" fill="#3FB950">@ 70ms warm latency and 0.95 direct seed confidence.</text>

    <text x="443" y="177" class="font-mono" font-size="9.5" font-weight="700" fill="#58A6FF">▸ Signal Cascade:</text>
    <text x="548" y="177" class="font-mono" font-size="9.5" fill="#C9D1D9">Sub-50ms retrieval endpoint,</text>
    <text x="451" y="191" class="font-mono" font-size="9" fill="#8B949E">indexing repos to 11,600+ nodes &amp; 23,700+ edges with</text>
    <text x="451" y="204" class="font-mono" font-size="9" fill="#8B949E">automated unified-diff fix &amp; LLM cost telemetry.</text>

    <text x="443" y="222" class="font-mono" font-size="9.5" font-weight="700" fill="#58A6FF">▸ AST Pipeline:</text>
    <text x="532" y="222" class="font-mono" font-size="9.5" fill="#C9D1D9">Tree-sitter AST parsing across 37 langs,</text>
    <text x="451" y="236" class="font-mono" font-size="9" fill="#8B949E">OpenAI enrichment, cross-service call-graph indexing,</text>
    <text x="451" y="249" class="font-mono" font-size="9" fill="#8B949E">and config-driven microservice discovery.</text>

    <text x="443" y="267" class="font-mono" font-size="9.5" font-weight="700" fill="#FFA657">▸ Cloud Cartography:</text>
    <text x="566" y="267" class="font-mono" font-size="9.5" fill="#C9D1D9">EventBridge (&lt;50ms Neo4j mutations)</text>
    <text x="451" y="281" class="font-mono" font-size="9" fill="#8B949E">&amp; 6h APScheduler batch reconciliation, materializing</text>
    <text x="451" y="294" class="font-mono" font-size="9" font-weight="700" fill="#3FB950">EC2/S3/RDS/Lambda collections in &lt;185ms/event.</text>

    <text x="443" y="312" class="font-mono" font-size="9.5" font-weight="700" fill="#A371F7">▸ GraphRAG NLQ:</text>
    <text x="540" y="312" class="font-mono" font-size="9.5" fill="#C9D1D9">FAISS router over 50 Cypher templates</text>
    <text x="451" y="326" class="font-mono" font-size="9" font-weight="700" fill="#3FB950">in &lt;30ms at zero LLM cost, with dynamic Cypher</text>
    <text x="451" y="339" class="font-mono" font-size="9" fill="#8B949E">generation and Neo4j EXPLAIN self-healing.</text>
  </g>
</svg>"""

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(repo_root, "assets", "timeline-horizontal.svg")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(SVG_CONTENT.strip() + "\n")
    print(f"✅ Generated horizontal timeline SVG: {out_path}")
