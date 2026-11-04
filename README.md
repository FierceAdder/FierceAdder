<!-- ════════════════════════════════════════
     §1  TERMINAL NEOFETCH SYSTEM CARD
     ════════════════════════════════════════ -->

<div align="center">

### `$ neofetch --full`

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="./assets/dark_mode.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/light_mode.svg" />
  <img alt="Ashmit's neofetch system card" src="./assets/dark_mode.svg" width="860" />
</picture>

</div>

---

<!-- ════════════════════════════════════════
     §2  CONTRIBUTIONS GRAPH (TERMINAL EDITION)
     ════════════════════════════════════════ -->

## 🌱 Activity Graph — Terminal Edition

> *Real-time contribution streaks — auto-updated nightly via GitHub Actions*

<div align="center">

<!-- Terminal-style contribution heatmap -->
<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="./assets/contrib-heatmap-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/contrib-heatmap-light.svg" />
  <img alt="contribution heatmap" src="./assets/contrib-heatmap-dark.svg" width="860" />
</picture>

</div>

---

<!-- ════════════════════════════════════════
     §3  GITHUB STATS GRID
     ════════════════════════════════════════ -->

## 📊 GitHub Stats

<div align="center">

<table>
  <tr>
    <td>
      <img src="https://github-readme-stats-eight-theta.vercel.app/api?username=FierceAdder&show_icons=true&theme=github_dark&hide_border=true&bg_color=0D1117&title_color=58A6FF&icon_color=58A6FF&text_color=C9D1D9&rank_icon=github" width="420" />
    </td>
    <td>
      <img src="https://streak-stats.demolab.com/?user=FierceAdder&theme=github-dark-blue&hide_border=true&background=0D1117&ring=58A6FF&fire=FF7B72&currStreakLabel=58A6FF" width="420" />
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="https://github-readme-stats-eight-theta.vercel.app/api/top-langs/?username=FierceAdder&layout=compact&theme=github_dark&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=C9D1D9&langs_count=8" width="420" />
    </td>
  </tr>
</table>

</div>

---

<!-- ════════════════════════════════════════
     §4  TECH STACK — 3D KEYBOARD STYLE
     ════════════════════════════════════════ -->

## 🎹 Tech Stack

> Keys I press daily — 24 tools, 4 rows, one keyboard

<div align="center">

<img src="./assets/techstack-3d-dark.svg" alt="3D Tech Stack — Languages · ML/AI · Backend · Frontend" width="860" />

</div>

---

<!-- ════════════════════════════════════════
     §5  COMPETITIVE PROGRAMMING (LEETCODE & CODEFORCES)
     ════════════════════════════════════════ -->

## ⚔️ Competitive Programming

<div align="center">

<table>
  <tr>
    <td align="center" width="50%">

### LeetCode

[![LeetCode Stats](https://leetcard.jacoblin.cool/Trying_out?theme=dark&font=JetBrains+Mono&ext=heatmap&border=0&bg=0D1117)](https://leetcode.com/Trying_out)

<p align="center">
  <img src="https://img.shields.io/badge/LeetCode-Knight_🏅-FFA116?style=flat-square" />
  <img src="https://img.shields.io/badge/Max_Rating-2073-58A6FF?style=flat-square" />
  <img src="https://img.shields.io/badge/Solved-700+-3FB950?style=flat-square" />
</p>

</td>
    <td align="center" width="50%">

### Codeforces
![CF Card](https://codeforces-stats-vlx.vercel.app/api/card?username=Scarceflyer7&theme=github_dark)

<p align="center">
  <img src="https://img.shields.io/badge/Codeforces-Pupil-1F8ACB?style=flat-square" />
  <img src="https://img.shields.io/badge/Rating-1385-58A6FF?style=flat-square" />
</p>

</td>
  </tr>
</table>

</div>

---

<!-- ════════════════════════════════════════
     §6  PROJECTS
     ════════════════════════════════════════ -->

## 🛸 Projects

<div align="center">

<table>
  <tr>

<!-- Project Card 1 -->
<td width="50%" valign="top">

### 📈 FinSocial
**Full-stack NSE/BSE Paper Trading Platform**

```
Stack  →  React · FastAPI · PostgreSQL
         XGBoost · FinBERT · Socket.IO
         Nginx · Docker · Vercel
```
- 🤖 3-class XGBoost signal classifier (BUY/HOLD/SELL) trained on 10 yrs OHLCV + FinBERT sentiment — 52.8% precision vs 33% random
- 💬 RAG-backed AI chatbot (Gemini + pgvector)
- ⚡ Real-time WebSocket leaderboard & community forums
- 🚀 Microservices behind Nginx reverse proxy + CI/CD

[![View Repo](https://img.shields.io/badge/GitHub-FinSocial-58A6FF?style=flat-square&logo=github)](https://github.com/FierceAdder/FinSocial)

</td>

<!-- Project Card 2 -->
<td width="50%" valign="top">

### 🧠 SENTINEL
**Privacy-first LLM Message Classifier**

```
Stack  →  Python · Gemini / OpenAI / Claude
         Tesseract OCR · faster-whisper
         scikit-learn · TF-IDF
```
- 🛡️ 96.7% macro-avg accuracy (5-fold CV) — classify notify/digest/mute
- 🔒 On-device OCR/ASR — raw media never leaves device
- ⚡ Sub-10ms TF-IDF/LR classifier for prompt-injection & phishing
- 🗜️ Context compressed 60–95% before LLM call

[![View Repo](https://img.shields.io/badge/GitHub-SENTINEL-FF7B72?style=flat-square&logo=github)](https://github.com/FierceAdder/SENTINEL)

</td>

  </tr>
  <tr>

<!-- Project Card 3 -->
<td width="50%" valign="top">

### 🔗 SyncSpace
**Collaborative Resource-Sharing Platform**

```
Stack  →  React · Node.js · Express
         MongoDB · AWS S3 · Socket.IO
```
- 📁 Share links, files, notes, rich-text articles in real-time
- ✍️ Live threads + typing indicators via Socket.IO
- 🔑 JWT auth + RBAC with presigned AWS S3 URLs
- 🔗 Open Graph link previews

[![View Repo](https://img.shields.io/badge/GitHub-SyncSpace-3FB950?style=flat-square&logo=github)](https://github.com/FierceAdder/SyncSpace)

</td>

<!-- Project Card 4 — Research -->
<td width="50%" valign="top">

### 🔬 MESA *(Research)*
**Moment Enriched Self Attention**

```
Domain →  NLP · Transformer Architecture
Venue  →  Scaler Rethesis (2nd Prize 🥈)
```
- 📐 Augments Q/K projections with learnable higher-order statistical moments via Cross-Moment Projection (CMP) module
- 🧪 Evaluated on AG News with multi-seed validation
- Co-authored independent research

[![View Paper](https://img.shields.io/badge/Paper-MESA-A371F7?style=flat-square&logo=arxiv)](https://github.com/FierceAdder)

</td>

  </tr>
</table>

</div>

---

<!-- ════════════════════════════════════════
     §7  ACHIEVEMENTS
     ════════════════════════════════════════ -->

## 🏆 Achievements

<div align="center">

| 🏅 Achievement | Details |
|:---|:---|
| **LeetCode Knight** | Worldwide **top 1%** · Max rating **2073** · **700+** problems solved |
| **Rank 417 / 27,000+** | LeetCode Weekly Contest 500 |
| **Codeforces Pupil** | Current rating **1385** |
| **Fidelity India Hackathon** | Finalist — Top 50 of 1200+ teams |
| **NER Tech 2.0** | Top 60 of 2000+ teams |
| **MSRIT Whackiest Hackathon** | Top 25 |
| **Scaler Rethesis** | 2nd Prize — MESA research paper |

</div>

---

<!-- ════════════════════════════════════════
     §8  EXPERIENCE & EDUCATION TIMELINE
     ════════════════════════════════════════ -->

## 🏢 Experience & Education

<div align="center">

<img src="./assets/timeline-horizontal.svg" alt="Experience & Education Horizontal Timeline" width="860" />

</div>

---

<!-- ════════════════════════════════════════
     §9  CERTIFICATIONS & LEARNING
     ════════════════════════════════════════ -->

## 📜 Certifications & Learning

<div align="center">

| Provider | Course |
|:---:|:---|
| ![DeepLearning.AI](https://img.shields.io/badge/DeepLearning.AI-0059B3?style=flat-square&logo=coursera&logoColor=white) | Transformers in Practice · ML Specialization · Agentic AI |
| ![TakeUForward](https://img.shields.io/badge/TakeUForward-FF6B00?style=flat-square&logoColor=white) | DSA — Basics to Advanced |

</div>

---

<!-- ════════════════════════════════════════
     §10  FOOTER
     ════════════════════════════════════════ -->

<div align="center">

<a href="mailto:ashmitv704@gmail.com"><img src="https://img.shields.io/badge/Email-ashmitv704%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" /></a>
&nbsp;
<a href="https://linkedin.com/in/ashmit-kumar-verma-9ba14a274"><img src="https://img.shields.io/badge/LinkedIn-Ashmit%20Kumar%20Verma-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
&nbsp;
<a href="https://github.com/FierceAdder"><img src="https://img.shields.io/badge/GitHub-FierceAdder-181717?style=for-the-badge&logo=github&logoColor=white" /></a>

<br/><br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=14&duration=4000&pause=1000&color=3FB950&center=true&vCenter=true&width=600&lines=Thanks+for+stopping+by!+Have+a+great+day+%F0%9F%91%BE;Building+at+the+intersection+of+AI+%26+Systems+Engineering;Always+learning%2C+always+building+%F0%9F%9A%80" alt="Footer Typing" />

<br/>

<sub>Crafted with precision &amp; code · Ashmit Kumar Verma © 2026</sub>

</div>

<br/>

*⭐ Star something interesting? Feel free to reach out!*

</div>
