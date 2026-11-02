/* Wspólne skrypty wariantów: lightbox, osadzanie gry, wideo, menu */
(()=>{
const y=document.getElementById('y');if(y)y.textContent=new Date().getFullYear();
const burger=document.querySelector('[data-burger]'),menu=document.querySelector('[data-menu]');
if(burger&&menu){burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>menu.classList.remove('open')))}
const items=[...document.querySelectorAll('[data-full]')];
if(items.length){
 const lb=document.createElement('div');lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');
 lb.innerHTML='<button class="lb-x" aria-label="Zamknij">✕</button><button class="lb-p" aria-label="Poprzednie">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" aria-label="Następne">›</button>';
 document.body.appendChild(lb);
 const st=document.createElement('style');st.textContent='.lb{position:fixed;inset:0;z-index:999;background:rgba(6,5,9,.94);display:flex;align-items:center;justify-content:center}.lb[hidden]{display:none}.lb figure{margin:0;text-align:center}.lb img{max-width:88vw;max-height:84vh;border-radius:10px;box-shadow:0 20px 80px rgba(0,0,0,.6)}.lb figcaption{color:#ccc;margin-top:10px;font:14px/1.4 system-ui,sans-serif}.lb button{position:absolute;width:48px;height:48px;border-radius:50%;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;font-size:26px;cursor:pointer}.lb-x{top:18px;right:18px;font-size:18px!important}.lb-p{left:18px}.lb-n{right:18px}@media(max-width:700px){.lb-p,.lb-n{top:auto;bottom:18px}}';
 document.head.appendChild(st);
 const img=lb.querySelector('img'),cap=lb.querySelector('figcaption');let i=0;
 const show=k=>{i=(k+items.length)%items.length;const b=items[i];img.src=b.dataset.full;img.alt=b.querySelector('img')?.alt||'';cap.textContent=b.dataset.cap||''};
 const close=()=>{lb.hidden=true;document.body.style.overflow='';items[i].focus()};
 items.forEach((b,k)=>b.addEventListener('click',e=>{e.preventDefault();show(k);lb.hidden=false;document.body.style.overflow='hidden';lb.querySelector('.lb-x').focus()}));
 lb.querySelector('.lb-x').onclick=close;lb.querySelector('.lb-p').onclick=()=>show(i-1);lb.querySelector('.lb-n').onclick=()=>show(i+1);
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 document.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
 let tx=0;lb.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)show(i+(d<0?1:-1))});
}
document.querySelectorAll('video[data-hover]').forEach(v=>{if(matchMedia('(hover:hover)').matches){v.addEventListener('mouseenter',()=>v.play().catch(()=>{}));v.addEventListener('mouseleave',()=>v.pause())}});
document.querySelectorAll('[data-embed]').forEach(box=>{const btn=box.querySelector('[data-play]');if(!btn)return;btn.addEventListener('click',()=>{const f=document.createElement('iframe');f.src=box.dataset.embed;f.title=box.dataset.title||"Gra Eve's Café";f.allow='autoplay; fullscreen';f.allowFullscreen=true;f.style.cssText='position:absolute;inset:0;width:100%;height:100%;border:0';box.appendChild(f);btn.remove()})});
})();
