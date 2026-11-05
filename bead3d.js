const fine=matchMedia('(pointer:fine)').matches;
(function(){
  const canvas=document.getElementById('beadCanvas');
  if(!canvas||!window.THREE)return;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;

  const scene=new THREE.Scene();
  const cam=new THREE.PerspectiveCamera(38,1,0.1,100);
  cam.position.set(0,0,4.0);
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));

  function size(){
    const w=canvas.clientWidth,h=canvas.clientHeight;
    renderer.setSize(w,h,false);
    cam.aspect=w/h;cam.updateProjectionMatrix();
  }
  size();addEventListener('resize',size);

  /* procedural rudraksha: sphere carved with mukhi furrows + organic bumps */
  const MUKHI=7;
  const geo=new THREE.SphereGeometry(1.25,196,196);
  const pos=geo.attributes.position;
  const v=new THREE.Vector3();
  const hash=(x,y,z)=>{const s=Math.sin(x*127.1+y*311.7+z*74.7)*43758.5453;return s-Math.floor(s);};
  for(let i=0;i<pos.count;i++){
    v.fromBufferAttribute(pos,i);
    const lon=Math.atan2(v.z,v.x);
    const lat=Math.asin(v.y/v.length());
    /* deep furrows dividing the bead into mukhi segments */
    const furrow=Math.pow(Math.abs(Math.sin(lon*MUKHI/2)),14)*0.16;
    /* organic warty texture, denser near equator like a real bead */
    const bump=(hash(v.x*6,v.y*6,v.z*6)*0.045+hash(v.x*14,v.y*14,v.z*14)*0.028)*Math.cos(lat*0.8);
    /* slightly oblate, flattened at poles */
    const squash=1-0.12*Math.pow(Math.abs(Math.sin(lat)),2);
    const r=(1+bump-furrow)*squash;
    v.setLength(1.25*r);
    pos.setXYZ(i,v.x,v.y,v.z);
  }
  geo.computeVertexNormals();

  const mat=new THREE.MeshStandardMaterial({color:0x8a4b2e,roughness:.78,metalness:.08});
  const bead=new THREE.Mesh(geo,mat);
  scene.add(bead);

  /* faint gold ring of small beads orbiting — the mala suggestion */
  const ring=new THREE.Group();
  const orbGeo=new THREE.SphereGeometry(.045,12,12);
  const orbMat=new THREE.MeshStandardMaterial({color:0xd9a441,roughness:.4,metalness:.55,emissive:0x3a2a08});
  for(let i=0;i<54;i++){
    const a=i/54*Math.PI*2;
    const orb=new THREE.Mesh(orbGeo,orbMat);
    orb.position.set(Math.cos(a)*2.05,Math.sin(a*3)*.06,Math.sin(a)*2.05);
    ring.add(orb);
  }
  ring.rotation.x=.5;
  scene.add(ring);

  /* warm ritual lighting */
  scene.add(new THREE.AmbientLight(0x2a1c12,1.4));
  const key=new THREE.DirectionalLight(0xffd9a0,1.5);key.position.set(3,2.5,4);scene.add(key);
  const ember=new THREE.PointLight(0xc4442a,1.2,12);ember.position.set(-3,-1.5,2.5);scene.add(ember);
  const rim=new THREE.DirectionalLight(0xd9a441,.9);rim.position.set(-2,3,-4);scene.add(rim);

  /* cursor interaction */
  let tx=0,ty=0,cx=0,cy=0;
  addEventListener('pointermove',e=>{
    tx=(e.clientX/innerWidth-.5)*.9;
    ty=(e.clientY/innerHeight-.5)*.6;
  },{passive:true});

  const heroPhoto=document.getElementById('heroPhoto');
  function frame(t){
    cx+=(tx-cx)*.05;cy+=(ty-cy)*.05;
    if(!reduced){
      bead.rotation.y=t*0.00022+cx;
      bead.rotation.x=.15+cy;
      ring.rotation.y=-t*0.00012;
    }else{
      bead.rotation.y=cx;bead.rotation.x=.15+cy;
    }
    if(heroPhoto&&fine){heroPhoto.style.transform=`rotateY(${cx*10}deg) rotateX(${-cy*8}deg)`;}
    renderer.render(scene,cam);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
