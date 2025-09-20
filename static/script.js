let artisans = []; // will be filled from backend

// Load artisans from backend
async function loadArtisansFromAPI() {
  try {
    const res = await fetch('/artisans');
    if (!res.ok) throw new Error("Network response was not ok");
    artisans = await res.json();
    renderArtisans(artisans);
    populateCategoryFilter();
  } catch (err) {
    console.error("Could not fetch artisans from API:", err);
    artisans = sampleArtisans || [];
    renderArtisans(artisans);
    populateCategoryFilter();
  }
}

// Render artisans
function renderArtisans(data, aiStory = null) {
  const container = document.getElementById("artisanContainer");
  container.innerHTML = "";

  if (data.length === 0) {
    if (aiStory) {
      container.innerHTML = `
        <div class="card ai-card">
          <div class="card-content">
            <h3>🤖 AI Story</h3>
            <p>${aiStory}</p>
          </div>
        </div>
      `;
    } else {
      container.innerHTML = "<p>No artisans found.</p>";
    }
    return;
  }

  data.forEach(artisan => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${artisan.image_url || 'placeholder.jpg'}" alt="${artisan.product}">
      <div class="card-content">
        <h3>${artisan.product}</h3>
        <p><strong>Artisan:</strong> ${artisan.name}</p>
        <p><strong>Location:</strong> ${artisan.location}</p>
        <p><strong>GI Tag:</strong> ${artisan.gi_tag || 'N/A'} (${artisan.year_gi || ''})</p>
        <p><strong>Story:</strong> ${artisan.story?.en || ""}</p>
        <p class="price">${artisan.price || ''}</p>
      </div>
    `;
    container.appendChild(card);
  });
}

// Populate category dropdown dynamically
async function populateCategoryFilter() {
  try {
    const res = await fetch('/api/categories');
    if (!res.ok) return;
    const cats = await res.json();
    const select = document.getElementById("filterSelect");

    select.innerHTML = `<option value="">All Categories</option>`;
    cats.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error("Failed to load categories:", err);
  }
}

// --- AI Integration ---
async function askAI(query) {
  try {
    const res = await fetch("/ai-search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await res.json();

    // If artisans found → render them
    if (data.results && data.results.length > 0) {
      renderArtisans(data.results);
    } else {
      // If no artisans → render AI story
      renderArtisans([], data.ai_story);
    }

    const aiBox = document.getElementById("aiResponse");
    aiBox.innerHTML = `<p><strong>🤖 AI Keywords:</strong> ${data.keywords.join(", ")}</p>`;
  } catch (err) {
    console.error("AI request failed:", err);
    document.getElementById("aiResponse").innerHTML =
      `<p style="color:red;">❌ AI failed. Try again later.</p>`;
  }
}

// --- Event Listeners ---
document.getElementById("searchBox").addEventListener("input", e => {
  const q = e.target.value.toLowerCase();
  const filtered = artisans.filter(a =>
    a.product.toLowerCase().includes(q) ||
    a.name.toLowerCase().includes(q) ||
    a.gi_tag?.toLowerCase().includes(q) ||
    a.location.toLowerCase().includes(q)
  );
  renderArtisans(filtered);
});

document.getElementById("filterSelect").addEventListener("change", e => {
  const category = e.target.value;
  const filtered = category ? artisans.filter(a => a.category === category) : artisans;
  renderArtisans(filtered);
});

document.getElementById("aiSearchBtn").addEventListener("click", () => {
  const query = document.getElementById("searchBox").value.trim();
  if (!query) {
    document.getElementById("aiResponse").innerHTML = "<p>Please enter something to ask AI.</p>";
    return;
  }
  askAI(query);
});

// Initial load
loadArtisansFromAPI();
