const ALLOWED_ORIGINS = new Set([
  "https://recklessrashdan.github.io",
  "http://localhost:8000",
  "http://127.0.0.1:8000"
]);

function corsHeaders(origin) {
  if (!origin || !ALLOWED_ORIGINS.has(origin)) {
    return {};
  }

  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  };
}

function jsonResponse(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(origin)
    }
  });
}

function sanitize(value, maxLength) {
  return String(value || "").trim().slice(0, maxLength);
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(origin)
      });
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "Method not allowed" }, 405, origin);
    }

    if (!env.DISCORD_WEBHOOK_URL) {
      return jsonResponse({ error: "Contact service is not configured" }, 503, origin);
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return jsonResponse({ error: "Invalid JSON body" }, 400, origin);
    }

    const name = sanitize(payload.name, 120);
    const email = sanitize(payload.email, 254);
    const message = sanitize(payload.message, 4000);

    if (!name || !email || !message) {
      return jsonResponse({ error: "Name, email, and message are required" }, 400, origin);
    }

    const discordPayload = {
      embeds: [
        {
          title: "New portfolio contact message",
          color: 0x5865f2,
          fields: [
            { name: "Name", value: name, inline: true },
            { name: "Email", value: email, inline: true },
            { name: "Message", value: message }
          ],
          timestamp: new Date().toISOString()
        }
      ]
    };

    const discordResponse = await fetch(env.DISCORD_WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(discordPayload)
    });

    if (!discordResponse.ok) {
      return jsonResponse({ error: "Could not deliver message" }, 502, origin);
    }

    return jsonResponse({ ok: true }, 200, origin);
  }
};
