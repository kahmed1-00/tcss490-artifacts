(function(){var root=document.documentElement,btns=document.querySelectorAll('.dots button'),T=['sky','wanted','wano'];
function set(t){root.setAttribute('data-theme',t);btns.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===t)});try{localStorage.setItem('op-theme',t)}catch(e){}}
var s='sky';try{s=localStorage.getItem('op-theme')||'sky'}catch(e){}if(T.indexOf(s)<0)s='sky';
btns.forEach(function(b){b.onclick=function(){set(b.dataset.t)}});set(s)})();