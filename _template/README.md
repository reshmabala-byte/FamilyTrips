# 🧭 Trip Journal Template

A plug-and-play template for adding a new family trip. No build tools, no server — just edit and push.

## Create a new trip in 5 steps

**1. Copy this folder** and rename it to your trip (lowercase, hyphens):
```powershell
cd C:\Users\reshm\Documents\Family-Trips
Copy-Item _template japan-2027 -Recurse
```

**2. Open `japan-2027/index.html`** and edit:
- The **HERO** block — title, description, dates, travelers, key stops.
- The page `<title>` near the top.
- The **footer** contact directory.

**3. Replace the `EXPENSES` array** (in the `<script>` near the bottom) with your real bookings. Each row:
```js
{cat:"Air", desc:"PHX ➔ NRT", ref:"ABC123", pts:"60,000 mi", cash:"$45.00", status:"Confirmed"},
```
Then tweak the four summary cards in `buildDash()` to your totals.

**4. Replace the `DAYS` array** with your itinerary. Per day:
| Field | Required? | Notes |
|-------|-----------|-------|
| `n` | ✅ | Day number (1, 2, 3…) |
| `icon` | ✅ | Any emoji |
| `date` | ✅ | e.g. `"Wed · Jul 15"` |
| `title` | ✅ | Short day title |
| `transport` | ✅ | How you get around |
| `acts` | ✅ | Array of activity strings |
| `lodging` | ✅ | Where you sleep |
| `ref` | ✅ | Confirmation reference |
| `extras` | optional | Array → shows the blue **💡 Don't-Miss** card |
| `note` | optional | String → shows the amber **⚠️ Pacing Note** card |

**5. Add a card to the repo-root `index.html`** so it shows on the hub.
Paste this block right before the dashed "Next Adventure" placeholder and edit it:

```html
<a href="japan-2027/index.html" class="card-rise group block rounded-3xl overflow-hidden bg-white border border-fjord-100 shadow-sm">
  <div class="relative h-52 overflow-hidden">
    <img src="PASTE_IMAGE_URL?w=800&q=80" alt="Japan" class="w-full h-full object-cover transition duration-500" />
    <span class="absolute top-4 left-4 bg-white/90 text-fjord-700 text-xs font-bold px-3 py-1 rounded-full">🇯🇵 Japan</span>
    <span class="absolute top-4 right-4 bg-fjord-700/90 text-white text-xs font-semibold px-3 py-1 rounded-full">Upcoming</span>
  </div>
  <div class="p-6">
    <div class="text-xs text-fjord-400 font-semibold uppercase tracking-wide">Dates · N Days</div>
    <h3 class="font-serif text-2xl font-700 mt-2 group-hover:text-fjord-600 transition">Trip Name</h3>
    <p class="text-sm text-fjord-800/80 mt-2 leading-relaxed">One-line description.</p>
    <div class="mt-5 inline-flex items-center gap-1 text-fjord-600 font-semibold text-sm">
      Open journal <span class="group-hover:translate-x-1 transition">→</span>
    </div>
  </div>
</a>
```

**Then publish:**
```powershell
git add .
git commit -m "Add Japan 2027 trip"
git push
```
GitHub Pages redeploys in ~1 minute.

## Good to know
- **Comments** are stored in each browser's localStorage, scoped per trip folder — trips never share comments.
- **Photo uploads** are live previews (blob URLs) and reset on refresh. For permanent photos, drop image files in the trip folder and reference them in the gallery.
- Free hero images: [unsplash.com](https://unsplash.com) → right-click → Copy Image Address, add `?w=800&q=80`.
- The `_template` folder is ignored by the hub — it never appears as a trip.
