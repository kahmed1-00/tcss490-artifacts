// ===== pixel art sprites (16 wide, bottom-aligned) =====
  var COM={k:'#1a1020',s:'#f4b783',S:'#d98c5c',w:'#fff',z:'#00000047'};
  var PAL={
    luffy:{y:'#f2b83c',r:'#d42f2a',h:'#1d1d2b',t:'#d42f2a',T:'#9e2020',a:'#f5c242',p:'#3d63cc',P:'#2a3f96',c:'#fff',l:'#f4b783',L:'#d98c5c',f:'#2a2030'},
    zoro:{h:'#3fa341',x:'#b33',t:'#232323',T:'#111',a:'#3fa341',p:'#2c2f3a',P:'#1d1f27',c:'#111',l:'#111',L:'#000',f:'#111'},
    nami:{h:'#ff8a1f',m:'#c0392b',t:'#f4f1ea',T:'#cfc9b8',a:'#3a73d8',p:'#3a73d8',P:'#264aa0',c:'#3a73d8',l:'#f4b783',L:'#d98c5c',f:'#d94f4f'},
    sanji:{h:'#f6df5a',r:'#e8412f',t:'#16161e',T:'#000',a:'#fff',p:'#16161e',P:'#000',c:'#16161e',l:'#16161e',L:'#000',f:'#0a0a0a'},
    usopp:{h:'#2b2018',y:'#f5c242',m:'#c0392b',t:'#c99a2e',T:'#8c6a1d',a:'#6b4a1e',p:'#7a5a2b',P:'#523a1a',c:'#7a5a2b',l:'#f4b783',L:'#d98c5c',f:'#3a2a1a'},
    robin:{h:'#14141c',m:'#c0392b',t:'#7e4bd0',T:'#5a2fa0',a:'#7e4bd0',p:'#5a2fa0',P:'#3d1f78',c:'#5a2fa0',l:'#f4b783',L:'#d98c5c',f:'#222'},
    franky:{h:'#3aa0ff',t:'#f4b783',T:'#d98c5c',a:'#e8412f',p:'#e8412f',P:'#b02a1e',c:'#f4b783',l:'#f4b783',L:'#d98c5c',f:'#222'},
    brook:{y:'#2b3fa8',h:'#1a1a24',s:'#eee',S:'#bbc',t:'#111118',T:'#000',a:'#fff',p:'#111118',P:'#000',c:'#111',l:'#111',L:'#000',f:'#000'},
    jinbe:{h:'#101018',s:'#6aa6e8',S:'#4a82c4',t:'#6b3fa0',T:'#4a2a78',a:'#f5c242',p:'#34508c',P:'#233a6a',c:'#34508c',l:'#6aa6e8',L:'#4a82c4',f:'#222'},
    chopper:{y:'#ff9ec4',s:'#e9b27a',S:'#a56a3a',p:'#3a7bd5',b:'#2f5fd0'}
  };
  var BODY=[".....kssssk.....","..kkttksskttkk..",".kttTksSSskTttk.",".ksskaaaaaakssk.",".ksskppppppkssk.","..kkppppppppkk..","...kpppPppPpk...","...kpppkkpppk...","...kccck.kccck..","...klllk.klllk..","...klLlk.klLlk..","..kkfffk.kfffkk.","..kkkkkk.kkkkkk."];
  var HEAD={
    luffy:["....kkkkkkkk....","...kyyyyyyyyk...","..kyyyyyyyyyyk..","..kyrrrrrrrryk..","kkyyyyyyyyyyyykk",".kkkhhhhhhhhkkk.","...khhhhhhhhk...","...khhsssshhk...","...kssksskssk...","...kssssssssk...","...kskwwwwksk..."],
    zoro:["....kkkkkkkk....","...khhhhhhhhk...","..khhhhhhhhhhk..","..khhhhhhhhhhk..","..khhhhhhhhhhk..","...khhhhhhhhk...","...khhsssshhk...","...kxsksskssk...","...kxsssssssk...","...ksskkkkssk...","....kkkkkkkk...."],
    nami:["....kkkkkkkk....","...khhhhhhhhk...","..khhhhhhhhhhk..","..khhhhhhhhhhk..","..khhhhhhhhhhk..","..khhh"+"ssss"+"hhk...","..kh"+"ssksskss"+"hk..","..kh"+"ssssssss"+"hk..","..kh"+"sssmmsss"+"hk..","..khh"+"ssssss"+"hhk.."],
    sanji:["....kkkkkkkk....","...khhhhhhhhk...","..khhhhhhhhhhk..","..khhhhhhhhhhk..","...k"+"hhhhhhhh"+"k...","...k"+"hhhhhhss"+"k...","...k"+"hhhhssks"+"k...","...k"+"shhsssss"+"k...","...k"+"ssssssss"+"wwr.","....kkkkkkkk...."],
    usopp:["....kkkkkkkk....","...khhhhhhhhk...","..khhhhhhhhhhk..","..khhhhhhhhhhk..","..kh"+"yyyyyyyy"+"hk..","..kh"+"ssksskss"+"hk..","..kh"+"ssssssss"+"SSk.","..kh"+"sssmmsss"+"hk..","...k"+"hssssssh"+"k..."],
    franky:[".....kkkkkk.....","....khhhhhhk....","...khhhhhhhhk...","...khhhhhhhhk...","...k"+"kkkkkkkk"+"k...","...k"+"ssssssss"+"k...","...k"+"sskwwkss"+"k...","....kkkkkkkk...."],
    brook:[".....kkkkkk.....",".....kyyyyk.....",".....kyyyyk.....","..kkkkkkkkkkkk..",".kkhhhhhhhhhhkk.",".khhhhhhhhhhhhk.",".khh"+"ssssssss"+"hhk.",".khh"+"ssksskss"+"hhk.",".khh"+"ssssssss"+"hhk.",".khh"+"skskskss"+"hhk.","..kh"+"ssssssss"+"hk.."],
    jinbe:["....kkkkkkkk....","...khhhhhhhhk...","..khhhhhhhhhhk..","..khh"+"ssssss"+"hhk..","..kh"+"ssksskss"+"hk..","..kh"+"ssssssss"+"hk..","..kh"+"skwkkwks"+"hk..","...k"+"ssssssss"+"k..."]
  };
  HEAD.robin=HEAD.nami;
  var CH=["...kk......kk...","...kSkkkkkkSk...","....kyyyyyyk....","....kywyywyk....","....kyywwyyk....","....kywyywyk....","...kkkkkkkkkk...","...kssksskssk...","...ksssbbsssk...","....kssssssk....","...ksSssssSsk...","...kssppppssk...","....kppppppk....","....ksk..ksk....","....kkk..kkk...."];
  var GR={};
  function grid(k){if(GR[k])return GR[k];var r=(k==='chopper'?CH:HEAD[k].concat(BODY)).slice();while(r.length<26)r.unshift('');r=r.slice(-26);r.push('..zzzzzzzzzzzz..');return GR[k]=r}
  function blit(g,k,ox,oy,ns){var p=PAL[k],r=grid(k);for(var y=0;y<r.length;y++){var row=r[y];for(var x=0;x<16&&x<row.length;x++){var ch=row[x];if(ch==='.'||(ns&&ch==='z'))continue;var c=p[ch]||COM[ch];if(c){g.fillStyle=c;g.fillRect(ox+x,oy+y,1,1)}}}}
  [].forEach.call(document.querySelectorAll('canvas.spr'),function(c){c.width=16;c.height=27;blit(c.getContext('2d'),c.dataset.c,0,0)});

  