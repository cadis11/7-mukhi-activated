/* nav */
(function(){
  const b=document.getElementById('burger'),n=document.getElementById('navLinks');
  if(b&&n){b.addEventListener('click',()=>{const o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});}
  /* reveal */
  const els=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));}
  else{
    const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:.12});
    els.forEach(el=>io.observe(el));
  }
  /* tilt */
  if(matchMedia('(pointer:fine)').matches){
    document.querySelectorAll('[data-tilt]').forEach(card=>{
      card.addEventListener('mousemove',e=>{
        const r=card.getBoundingClientRect();
        const x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
        card.style.transform='rotateY('+(x*8)+'deg) rotateX('+(-y*8)+'deg) translateZ(6px)';
      });
      card.addEventListener('mouseleave',()=>{card.style.transform='';});
    });
  }
  /* language toggle (Nepali / English blocks) */
  document.querySelectorAll('[data-lang-toggle]').forEach(wrap=>{
    wrap.querySelectorAll('button').forEach(btn=>btn.addEventListener('click',()=>{
      const l=btn.dataset.l;
      wrap.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===btn));
      document.querySelectorAll('[data-lang]').forEach(s=>{s.hidden=(s.dataset.lang!==l);});
    }));
  });
  /* bead price picker */
  const fmt=n=>'NRS '+n.toLocaleString('en-US');
  document.querySelectorAll('[data-bead]').forEach(card=>{
    const act=+card.dataset.act,nat=+card.dataset.nat,pen=+card.dataset.pendant,name=card.dataset.name;
    const price=card.querySelector('[data-price]'),sub=card.querySelector('[data-pricesub]'),
          btn=card.querySelector('[data-order]'),note=card.querySelector('[data-optnote]'),
          pend=card.querySelector('[data-pendant]');
    function upd(){
      const tier=card.querySelector('input[type=radio]:checked').value;
      const withP=pend.checked;
      const total=(tier==='act'?act:nat)+(withP?pen:0);
      price.textContent=fmt(total);
      sub.textContent=tier==='act'?'Consecrated · Guru dakshina included':'Natural certified · not consecrated';
      note.textContent=tier==='act'
        ?'54-day Vedic & Tantric consecration, 2 lakh chants and havan.'
        :'Same Nepal-sourced selection with certificate. Can be consecrated later.';
      const msg='Namaste, I would like to order the '+name+' Rudraksha — '+(tier==='act'?'Activated':'Natural certified')+(withP?' with pendant':'')+' ('+fmt(total)+').';
      btn.href='https://wa.me/9779823783486?text='+encodeURIComponent(msg);
    }
    card.querySelectorAll('input').forEach(i=>i.addEventListener('change',upd));
    upd();
  });
})();
