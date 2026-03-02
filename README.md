This README focuses exclusively on the Missouri Civic Action Hub application, detailing its frontend features and the proxy architecture that powers it.
Missouri Civic Action Hub 🏛️
A specialized web application designed to provide Missouri residents with transparent, real-time access to state representatives and upcoming legislation.
🚀 Core Functions
1. Representative Discovery
The application provides two distinct methods to identify and contact Missouri officials:
 * Search by Name: A dedicated search interface that allows users to find specific representatives. This includes a "Limit" selector to control the number of results returned (10, 25, or 100/All).
 * Address-Based Lookup: Utilizing Google Maps Geocoding, users can enter a physical address (e.g., "22 Jean Dr, Florissant, MO") to identify their specific district representatives based on geographic coordinates.
2. Legislative Tracking
 * Upcoming Bills: A dynamic grid section that pulls and displays the latest Missouri bills.
 * Status Visibility: Designed to show the current progress and titles of pending legislation.
3. User Experience Features
 * Contact Badges: Search results generate "cards" for each representative, featuring:
   * Party Affiliation: Color-coded badges (Blue for Democrat, Red for Republican, Gray for Neutral/Other).
   * Click-to-Call: Integrated tel: links for immediate phone contact.
   * Official Links: Direct access to official legislative websites.
 * Dark Mode: A persistent UI toggle located in the header for improved accessibility and night-time viewing.
 * Visual Feedback: Integrated "Loading Pulse" animations to signal active data fetching.
🛠️ Technical Architecture
Frontend (Client-Side)
 * Technologies: HTML5, CSS3 (using CSS variables for themes), and Vanilla JavaScript.
 * Key Logic: * Asynchronous fetch calls to handle API requests.
   * Dynamic DOM manipulation to render representative cards and bill grids.
   * Form-based event handling to support "Enter" key searches.
Backend Proxy (Intel i5 Node)
The application communicates with a custom Node.js proxy server located at 192.168.50.191:3005. This proxy is essential for:
 * Credential Masking: It injects the OPENSTATES_KEY and GOOGLE_API_KEY server-side, ensuring they are never exposed in the browser's source code or network tab.
 * CORS Management: It allows the frontend to securely request data across the local network.
 * Data Formatting: Cleans and "hunts" for specific office contact details (like voice phone numbers) from the OpenStates API before sending them to the frontend.
📂 Project Structure
 * index.html: The main application file containing the UI structure and JavaScript logic.
 * .env: (On Proxy Server) Stores the private API keys.
 * server.js: (On Proxy Server) The Express.js logic that handles API routing and key injection.
Would you like me to help you create a "User Guide" section specifically for the Representative Search features?
