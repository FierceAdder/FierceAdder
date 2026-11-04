import { execSync } from "child_process";
import fs from "fs";
import path from "path";

const USERNAME = process.env.GH_USERNAME || process.env.GITHUB_USERNAME || "ashmitv704";

// Obtain GitHub token from environment or gh CLI
let token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
if (!token) {
  try {
    token = execSync("gh auth token", { encoding: "utf8" }).trim();
  } catch (err) {
    console.warn("Notice: No GitHub token found via env or `gh auth token`. Proceeding with fallback/public access if available.");
  }
}

const LEVEL_MAP = {
  NONE: 0,
  FIRST_QUARTILE: 1,
  SECOND_QUARTILE: 2,
  THIRD_QUARTILE: 3,
  FOURTH_QUARTILE: 4,
};

async function fetchGitHubContributions() {
  const query = `
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
  `;

  if (!token) {
    console.warn("No token available for GraphQL API. Writing simulated initial github.json.");
    return generateFallback();
  }

  const response = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "portfolio-contribution-fetcher",
    },
    body: JSON.stringify({ query, variables: { login: USERNAME } }),
  });

  if (!response.ok) {
    throw new Error(`GitHub API error: ${response.statusText}`);
  }

  const resJson = await response.json();
  if (resJson.errors) {
    throw new Error(JSON.stringify(resJson.errors));
  }

  const calendar = resJson.data.user.contributionsCollection.contributionCalendar;
  const total = calendar.totalContributions;
  const weeks = calendar.weeks;

  const counts = [];
  let levels = "";
  let startDate = "";
  let bestDay = 0;
  let currentStreak = 0;
  let maxStreak = 0;

  for (const week of weeks) {
    for (const day of week.contributionDays) {
      if (!startDate) startDate = day.date;
      const count = day.contributionCount;
      const level = LEVEL_MAP[day.contributionLevel] ?? 0;

      counts.push(count);
      levels += level.toString();

      if (count > bestDay) bestDay = count;
      if (count > 0) {
        currentStreak++;
        if (currentStreak > maxStreak) maxStreak = currentStreak;
      } else {
        currentStreak = 0;
      }
    }
  }

  return {
    username: USERNAME,
    startDate,
    total,
    counts,
    levels,
    bestDay,
    streak: currentStreak > 0 ? currentStreak : maxStreak,
    fetchedAt: new Date().toISOString(),
  };
}

function generateFallback() {
  const counts = [];
  let levels = "";
  let total = 0;
  let bestDay = 0;
  const today = new Date();
  today.setDate(today.getDate() - 364);
  const startDate = today.toISOString().split("T")[0];

  for (let i = 0; i < 365; i++) {
    const isWeekend = i % 7 === 5 || i % 7 === 6;
    let count = 0;
    let level = 0;
    if (!isWeekend && Math.random() > 0.3) {
      count = Math.floor(Math.random() * 8) + 1;
      level = Math.min(4, Math.ceil(count / 2));
    }
    counts.push(count);
    levels += level.toString();
    total += count;
    if (count > bestDay) bestDay = count;
  }

  return {
    username: USERNAME,
    startDate,
    total,
    counts,
    levels,
    bestDay,
    streak: 14,
    fetchedAt: new Date().toISOString(),
  };
}

async function run() {
  try {
    const data = await fetchGitHubContributions();
    const outPath = path.resolve("data/github.json");
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, JSON.stringify(data, null, 2), "utf8");
    console.log(`Successfully wrote GitHub contribution data to ${outPath}`);
    console.log(`Total: ${data.total}, Days: ${data.counts.length}, Streak: ${data.streak}, Best: ${data.bestDay}`);
  } catch (err) {
    console.error("Error fetching GitHub data:", err);
    process.exit(1);
  }
}

run();

