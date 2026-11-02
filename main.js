document.getElementById('y').textContent=new Date().getFullYear();
const burger=document.querySelector('.burger'),nav=document.querySelector('.nav nav');
burger.addEventListener('click',()=>{const o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nav.classList.remove('open')));
// reveal
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
// lightbox
const items=[...document.querySelectorAll('.gallery button')],lb=document.querySelector('.lightbox'),lbImg=lb.querySelector('img'),lbCap=lb.querySelector('.lb-cap');let idx=0;
function show(i){idx=(i+items.length)%items.length;const b=items[idx];lbImg.src=b.dataset.full;lbImg.alt=b.querySelector('img').alt;lbCap.textContent=b.parentElement.querySelector('figcaption').textContent}
items.forEach((b,i)=>b.addEventListener('click',()=>{show(i);lb.hidden=false;document.body.style.overflow='hidden';lb.querySelector('.lb-close').focus()}));
function close(){lb.hidden=true;document.body.style.overflow='';items[idx].focus()}
lb.querySelector('.lb-close').onclick=close;lb.querySelector('.lb-prev').onclick=()=>show(idx-1);lb.querySelector('.lb-next').onclick=()=>show(idx+1);
lb.addEventListener('click',e=>{if(e.target===lb)close()});
document.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1)});
let tx=0;lb.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)show(idx+(d<0?1:-1))});
// videos: hover play on desktop
document.querySelectorAll('.vcard video').forEach(v=>{if(matchMedia('(hover:hover)').matches){v.addEventListener('mouseenter',()=>v.play().catch(()=>{}));v.addEventListener('mouseleave',()=>v.pause())}});
// lazy game embed
document.querySelectorAll('.embed[data-src]').forEach(box=>box.querySelector('.play').addEventListener('click',()=>{const f=document.createElement('iframe');f.src=box.dataset.src;f.title=box.dataset.title||'Gra Eve\'s Café';f.allow='autoplay; fullscreen';f.allowFullscreen=true;f.loading='lazy';box.appendChild(f);box.querySelector('.play').remove()}));
