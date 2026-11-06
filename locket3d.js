(function(){
  const stage=document.getElementById('locket3d'),tilt=document.getElementById('locketTilt');
  if(!stage||!tilt)return;
  const shine=tilt.querySelector('.locket-shine');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ty=0,tx=0,cy=0,cx=0,active=false,t0=performance.now();
  function aim(e){
    const r=stage.getBoundingClientRect();
    const nx=Math.max(-1.4,Math.min(1.4,(e.clientX-(r.left+r.width/2))/(r.width*.9)));
    const ny=Math.max(-1.4,Math.min(1.4,(e.clientY-(r.top+r.height/2))/(r.height*.9)));
    ty=nx*38; tx=-ny*14; active=true;
  }
  const area=stage.parentElement||stage;
  area.addEventListener('pointermove',aim);
  area.addEventListener('pointerleave',()=>{active=false});
  stage.addEventListener('pointerdown',aim);
  if(reduced){tilt.style.transform='rotateY(-10deg)';return;}
  function frame(now){
    const s=(now-t0)/1000;
    if(!active){ty=Math.sin(s*.9)*20;tx=Math.cos(s*.6)*4;}
    cy+=(ty-cy)*.08; cx+=(tx-cx)*.08;
    const bob=Math.sin(s*1.3)*5;
    tilt.style.transform='translateY('+bob.toFixed(2)+'px) rotateX('+cx.toFixed(2)+'deg) rotateY('+cy.toFixed(2)+'deg)';
    shine.style.setProperty('--sx',(-120+(cy/40+.5)*240).toFixed(1)+'%');
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
