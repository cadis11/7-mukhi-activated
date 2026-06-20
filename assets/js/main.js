// ============ UTILS ============
function switchLang(lang, btn) {
    document.querySelectorAll('.lang').forEach(e => e.classList.remove('active'));
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    const target = document.getElementById(lang);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
}

async function sbFetch(path, opts = {}) {
    const res = await fetch(CONFIG.SUPABASE_URL + path, {
        headers: {
            'apikey': CONFIG.SUPABASE_ANON_KEY,
            'Authorization': 'Bearer ' + CONFIG.SUPABASE_ANON_KEY,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
            ...opts.headers
        },
        ...opts
    });
    return res;
}

// ============ CART LOGIC ============
let cart = JSON.parse(localStorage.getItem('rudra_cart') || '[]');

function saveCart() {
    localStorage.setItem('rudra_cart', JSON.stringify(cart));
    renderCart();
}

function addToCart(id, name, mukhi, price) {
    const existing = cart.find(i => i.id === id);
    if (existing) {
        existing.qty++;
    } else {
        cart.push({ id, name, mukhi, price, qty: 1 });
    }
    saveCart();
    showNotification(`Sacred ${mukhi} Mukhi bead added to cart`);
}

function showNotification(msg) {
    let note = document.getElementById('rudra-notification');
    if (!note) {
        note = document.createElement('div');
        note.id = 'rudra-notification';
        document.body.appendChild(note);
    }
    note.textContent = msg;
    note.classList.add('show');
    setTimeout(() => {
        note.classList.remove('show');
    }, 3000);
}

function changeQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) cart = cart.filter(i => i.id !== id);
    saveCart();
}

function getTotal() {
    return cart.reduce((s, i) => s + (i.price * i.qty), 0);
}

function renderCart() {
    const totalItems = cart.reduce((s, i) => s + i.qty, 0);
    const countEls = document.querySelectorAll('.cart-count');
    countEls.forEach(el => {
        el.textContent = totalItems;
        el.classList.toggle('show', totalItems > 0);
    });

    const body = document.getElementById('cartBody');
    const footer = document.getElementById('cartFooter');
    if (!body) return;

    if (!cart.length) {
        body.innerHTML = `<div class="cart-empty"><span class="cart-empty-icon">🪬</span><p>Your cart is empty.<br>Add a sacred bead to begin.</p></div>`;
        if (footer) footer.style.display = 'none';
        return;
    }

    if (footer) footer.style.display = 'block';
    const totalEl = document.getElementById('cartTotalPrice');
    if (totalEl) totalEl.textContent = 'NRS ' + getTotal().toLocaleString();

    body.innerHTML = cart.map(i => `
    <div class="cart-item">
      <div>
        <div class="cart-item-name">${i.name}</div>
        <div class="cart-item-sub">${i.mukhi} Mukhi · NRS ${i.price.toLocaleString()} each</div>
        <div class="cart-item-controls">
          <button class="qty-btn" onclick="changeQty('${i.id}',-1)">−</button>
          <span class="qty-num">${i.qty}</span>
          <button class="qty-btn" onclick="changeQty('${i.id}',1)">+</button>
        </div>
        <button class="cart-item-remove" onclick="changeQty('${i.id}',-999)">Remove</button>
      </div>
      <div style="text-align:right">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--gold-light)">NRS ${(i.price * i.qty).toLocaleString()}</div>
      </div>
    </div>`).join('');
}

function openCart() {
    const overlay = document.getElementById('cartOverlay');
    const drawer = document.getElementById('cartDrawer');
    if (overlay && drawer) {
        overlay.classList.add('open');
        drawer.classList.add('open');
        document.body.style.overflow = 'hidden';
    }
}

function closeCart() {
    const overlay = document.getElementById('cartOverlay');
    const drawer = document.getElementById('cartDrawer');
    if (overlay && drawer) {
        overlay.classList.remove('open');
        drawer.classList.remove('open');
        document.body.style.overflow = '';
    }
}

// ============ REVEAL OBSERVER ============
const revealObserver = new IntersectionObserver(
    entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.08 }
);

function initReveal() {
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
}

// ============ ADMIN TRIGGER ============
let adminBuffer = '';
document.addEventListener('keydown', e => {
    adminBuffer += e.key.toLowerCase();
    if (adminBuffer.includes('admin')) {
        adminBuffer = '';
        if (window.location.pathname.includes('collection.html')) {
            if (typeof openAdmin === 'function') openAdmin();
        } else {
            window.location.href = 'collection.html?admin=1';
        }
    }
    if (adminBuffer.length > 10) adminBuffer = adminBuffer.slice(-10);
});

// ============ INITIALIZATION ============
document.addEventListener('DOMContentLoaded', () => {
    // Set active nav link
    const path = window.location.pathname.split('/').pop() || 'index.html';
    const navMap = {
        'index.html': 'nav-home',
        'collection.html': 'nav-shop',
        'about.html': 'nav-about',
        'learn.html': 'nav-learn',
        'contact.html': 'nav-contact'
    };
    const activeId = navMap[path];
    if (activeId) {
        const activeLink = document.getElementById(activeId);
        if (activeLink) activeLink.classList.add('active');
    }

    renderCart();
    initReveal();

    // Smooth page fade in
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 10);
});
