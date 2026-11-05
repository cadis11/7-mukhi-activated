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
    const base=+card.dataset.base,add=+card.dataset.add,name=card.dataset.name,tier=card.dataset.tier;
    const price=card.querySelector('[data-price]'),sub=card.querySelector('[data-pricesub]'),
          btn=card.querySelector('[data-order]'),pend=card.querySelector('[data-pendant]');
    function upd(){
      const withP=pend&&pend.checked,total=base+(withP?add:0);
      price.textContent=fmt(total);
      sub.textContent=withP?card.dataset.subLocket:card.dataset.subPlain;
      const msg='Namaste, I would like to order the '+name+' Rudraksha — '+tier+(withP?' in a Panchadhatu Om locket':'')+' ('+fmt(total)+').';
      btn.href='https://wa.me/9779823783486?text='+encodeURIComponent(msg);
    }
    if(pend)pend.addEventListener('change',upd);
    upd();
  });
  /* gaurishankar size picker */
  document.querySelectorAll('[data-gauri]').forEach(box=>{
    const price=box.querySelector('[data-gprice]'),btn=box.querySelector('[data-gorder]');
    function upd(){
      const r=box.querySelector('input[type=radio]:checked');
      price.textContent=r.dataset.text;
      btn.href='https://wa.me/9779823783486?text='+encodeURIComponent('Namaste, I am interested in a Gaurishankar Rudraksha — '+r.dataset.label+' ('+r.dataset.text+').');
    }
    box.querySelectorAll('input[type=radio]').forEach(i=>i.addEventListener('change',upd));
    upd();
  });
})();
