(function(){
var el=document.getElementById('poll');if(!el)return;
var KEY='warheit-sonntagsfrage-v1',base=[41,33,17,9],opts=el.querySelectorAll('button');
function show(v){var tot=base.reduce(function(a,b){return a+b},0)+(v!==null?1:0);
opts.forEach(function(b,i){var n=base[i]+(v===i?1:0);var p=Math.round(n/tot*100);b.querySelector('.bar').style.width=p+'%';b.querySelector('.pc').textContent=p+' %';b.disabled=true;b.style.cursor='default'});
el.querySelector('small').textContent='Ergebnis vorläufig, nicht repräsentativ und nicht wahr.'}
var s=null;try{s=localStorage.getItem(KEY)}catch(e){}
if(s!==null)show(parseInt(s,10));
opts.forEach(function(b,i){b.addEventListener('click',function(){try{localStorage.setItem(KEY,String(i))}catch(e){}show(i)})});
})();
