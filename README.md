# Missouri Civic Action Hub 🏛️

A web application giving Missouri residents transparent, real-time access to their elected representatives and upcoming state legislation. Built with vanilla HTML, CSS, and JavaScript — powered by a secure local Node.js proxy that keeps all API keys off the browser.

**Live site:** [civicdata.homehosted.space](https://civicdata.homehosted.space)

---

## Features

### Representative Discovery
Two ways to find your officials:

- **Browse by name** — Search all Missouri representatives with a live-filter search box and a result limit selector (10, 25, 50, or All).
- **Find by address** — Enter any Missouri street address to instantly identify the specific representatives for that district, including both state and federal officials.

### Representative Cards
Each result card displays:
- **Party badge** — Color-coded: 🔵 Blue (Democrat), 🔴 Red (Republican), ⬜ Gray (Other/Independent)
- **Level badge** — 🟢 Green (State) or 🟣 Purple (Federal)
- District, chamber, and jurisdiction
- **Reelection year** — When their current term ends (if available from the API)
- Click-to-call phone number
- Links to official website and Facebook page

### Legislative Tracking
- **Upcoming Bills** — A dynamic grid of the latest Missouri bills pulled from `data.json`, showing bill title, ID, and current status.

### User Experience
- **Dark mode** — Persistent toggle in the header, saved across sessions via `localStorage`
- **Skeleton loaders** — Animated placeholder cards while data is fetching
- **Inline error messages** — User-facing feedback if an API call fails or an address isn't found
- **Keyboard support** — Press Enter in the address field to trigger a lookup
- **Accessible** — Screen-reader-friendly labels, `aria-live` regions, and semantic list markup

---

## Project Structure

```
/
├── index.html              # Main application — all UI, styles, and JS in one file
├── data.json               # Missouri bills data (masterlist format)
├── enriched_people.json    # Representative data with contact details
└── README.md               # This file
```

### Proxy Server (separate machine)

```
/home/dietpi/civic-proxy/
├── server.js               # Express.js proxy — handles API routing and key injection
└── .env                    # API keys (never committed to version control)
```

---

## Architecture

### Frontend (`index.html`)

Pure HTML/CSS/JS — no frameworks or build tools required. Key design decisions:

- **CSS custom properties** power the light/dark theme system
- **DOM refs cached at startup** — no repeated `getElementById` calls in render loops
- **Debounced search** — 200ms delay prevents excessive filtering on fast typing
- **`escHtml()` helper** — all dynamic content is sanitized before being inserted into the DOM

### Backend Proxy (`server.js` on `192.168.50.191:3005`)

The proxy is the security backbone of the application. The browser never sees any API keys.

| Proxy Endpoint | Purpose |
|---|---|
| `GET /api/geocode?address=...` | Converts a street address to `{ lat, lng }` using Google Maps Geocoding API |
| `GET /api/reps?lat=...&lng=...` | Fetches representatives for coordinates from the OpenStates API |

The proxy:
- Loads `GOOGLE_API_KEY` and `OPENSTATES_KEY` from `.env` via `dotenv`
- Injects the appropriate key into each outbound request
- Handles CORS so the frontend can call it across the local network
- Returns clean, formatted JSON to the browser

### Data Flow

```
User enters address
        ↓
Browser → POST /api/geocode → Proxy → Google Maps API
        ↓ returns { lat, lng }
Browser → GET /api/reps?lat&lng → Proxy → OpenStates API
        ↓ returns representative data
Browser renders cards
```

---

## API Dependencies

| Service | Used For | Key Location |
|---|---|---|
| [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding) | Address → coordinates | `GOOGLE_API_KEY` in `.env` |
| [OpenStates API v3](https://docs.openstates.org/api-v3/) | Representatives by location | `OPENSTATES_KEY` in `.env` |

### Expected Proxy Response Shapes

**`/api/geocode`** must return:
```json
{ "lat": 38.6270, "lng": -90.1994 }
```

**`/api/reps`** must return data in OpenStates format:
```json
{
  "results": [
    {
      "name": "Jane Smith",
      "party": "Democratic",
      "jurisdiction": { "name": "Missouri" },
      "current_role": {
        "org_classification": "upper",
        "end_date": "2026-01-01"
      }
    }
  ]
}
```

---

## Local Data Files

### `data.json`
Bills data in OpenStates masterlist format:
```json
{
  "masterlist": {
    "1": {
      "bill_id": "HB 123",
      "title": "An act relating to...",
      "url": "https://...",
      "status": "In Committee",
      "last_action": "Referred to Rules"
    }
  }
}
```

### `enriched_people.json`
Array of representative objects:
```json
[
  {
    "name": "Jane Smith",
    "party": "Democratic",
    "district": "15",
    "jurisdiction": "Missouri",
    "current_role": { "end_date": "2026-01-01" },
    "bio": {
      "social": {
        "capitol_phone": "573-555-0100",
        "biography": "https://house.mo.gov/..."
      },
      "links": {
        "official": { "facebook": "https://facebook.com/..." }
      }
    }
  }
]
```

---

## Setup & Deployment

### Frontend
No build step required. Deploy `index.html`, `data.json`, and `enriched_people.json` to any static web server.

### Proxy Server
The proxy runs on a dedicated Intel i5 device at `192.168.50.191:3005`.

**Requirements:**
- Node.js
- npm packages: `express`, `dotenv`, `node-fetch` (or `axios`)
- A `.env` file in the proxy directory:

```env
GOOGLE_API_KEY=your_google_key_here
OPENSTATES_KEY=your_openstates_key_here
```

**Start the proxy:**
```bash
cd /home/dietpi/civic-proxy
node server.js
```

**Recommended:** Use `pm2` to keep the proxy running across reboots:
```bash
pm2 start server.js --name civic-proxy
pm2 save
pm2 startup
```

### CORS Configuration
Ensure `server.js` restricts CORS to your domain in production:
```javascript
const cors = require('cors');
app.use(cors({ origin: 'https://civicdata.homehosted.space' }));
```

---

## Security Notes

- ✅ API keys are stored only in `.env` on the proxy server
- ✅ The browser source code contains no keys — only the proxy URL
- ✅ `config.js` has been removed from the project
- ✅ All dynamic content rendered to the DOM is HTML-escaped to prevent XSS
- ⚠️ The proxy IP (`192.168.50.191`) is on a local network — ensure the proxy machine's firewall only exposes port `3005` to trusted sources

---

## Browser Support

Works in all modern browsers (Chrome, Firefox, Safari, Edge). No polyfills required — uses standard `fetch`, `async/await`, and CSS custom properties.

---

## Support

If this tool is useful to you, consider [supporting the project](https://cash.app/$toyz4me).
