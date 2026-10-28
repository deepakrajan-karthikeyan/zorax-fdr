const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { URL } = require("node:url");
const { Client } = require("pg");
const { getDatabaseConfig } = require("../db/config");

const root = path.resolve(__dirname, "..");
const port = Number(process.env.PORT || 5500);
const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8"
};

function sendJson(response, status, payload) {
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store"
  });
  response.end(JSON.stringify(payload));
}

function serveStatic(request, response) {
  const requested = new URL(request.url, "http://localhost").pathname;
  const relative = requested === "/" ? "index.html" : requested.slice(1);
  const file = path.resolve(root, relative);
  if (!file.startsWith(root + path.sep)) {
    sendJson(response, 403, { error: "Path is not allowed" });
    return;
  }
  fs.stat(file, (error, stats) => {
    if (error || !stats.isFile()) {
      sendJson(response, 404, { error: "Not found" });
      return;
    }
    response.writeHead(200, {
      "Content-Type": mimeTypes[path.extname(file)] || "application/octet-stream"
    });
    fs.createReadStream(file).pipe(response);
  });
}

async function databaseStatus() {
  const database = getDatabaseConfig();
  if (!database.configured) {
    return { provider: "supabase-postgresql", host: database.host, configured: false, connected: false };
  }
  const client = new Client({
    connectionString: database.connectionString,
    ssl: { rejectUnauthorized: false },
    connectionTimeoutMillis: 5000
  });
  try {
    await client.connect();
    await client.query("select 1");
    return { provider: "supabase-postgresql", host: database.host, configured: true, connected: true };
  } catch (error) {
    return {
      provider: "supabase-postgresql",
      host: database.host,
      configured: true,
      connected: false,
      error: error.code || "connection_failed"
    };
  } finally {
    await client.end().catch(() => {});
  }
}

const server = http.createServer(async (request, response) => {
  if (request.method !== "GET") {
    sendJson(response, 405, { error: "Only GET is available in this demo API" });
    return;
  }
  const url = new URL(request.url, "http://localhost");
  if (url.pathname === "/api/health") {
    sendJson(response, 200, {
      service: "zorax-api",
      environment: process.env.ZORAX_ENV || "demo",
      extractionMode: process.env.AI_EXTRACTION_MODE || "demo",
      database: await databaseStatus(),
      status: "ok"
    });
    return;
  }
  if (url.pathname === "/api/intelligence/capabilities") {
    sendJson(response, 200, {
      mode: "DEMO",
      capabilities: [
        "layout-analysis",
        "schema-extraction",
        "anomaly-detection",
        "fuzzy-matching",
        "confidence-review",
        "deadline-prioritization",
        "lifecycle-state-machine",
        "regulatory-search",
        "hash-chained-audit"
      ]
    });
    return;
  }
  serveStatic(request, response);
});

server.listen(port, "127.0.0.1", () => {
  console.log(`ZORAX API and static server listening on http://127.0.0.1:${port}`);
});
