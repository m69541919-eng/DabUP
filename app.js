const tg=window.Telegram?.WebApp;if(tg){tg.ready();tg.expand();}
const $=id=>document.getElementById(id);
const user=tg?.initDataUnsafe?.user;
$("username").textContent=user?.first_name||"гость";
if(user?.photo_url){$("avatar").textContent="";$("avatar").style.backgroundImage=`url("${user.photo_url}")`;$("avatar").style.backgroundSize="cover";}
let data={points:0,boost:0,shield:0,best:0,opened:[]};
try{data={...data,...JSON.parse(localStorage.getItem("dabup_save")||"{}")}}catch{}
function save(){localStorage.setItem("dabup_save",JSON.stringify(data));render()}
function render(){
$("points").textContent=data.points.toLocaleString("ru-RU");
$("bestFlight").textContent=data.best+" м";
$("boostLevel").textContent=`Уровень ${data.boost} · +${data.boost*10}% к награде`;
$("shieldLevel").textContent=`Уровень ${data.shield} · косметика`;
$("boostBuy").disabled=data.points<100||data.boost>=5;
$("shieldBuy").disabled=data.points<50||data.shield>=1;
document.querySelectorAll(".case-open").forEach(b=>{const used=data.opened.includes(b.dataset.name);b.disabled=used;b.textContent=used?"Получено":"Открыть"});
}
document.querySelectorAll(".tab").forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll(".tab,.page").forEach(x=>x.classList.remove("active"));btn.classList.add("active");$(btn.dataset.tab).classList.add("active")}));
let flying=false;
$("launch").addEventListener("click",()=>{
if(flying)return;flying=true;const button=$("launch");button.disabled=true;button.textContent="РАКЕТА НАБИРАЕТ ВЫСОТУ…";
let height=0;const rocket=$("rocketIcon");const start=Date.now();
const timer=setInterval(()=>{
height+=Math.floor(18+Math.random()*13);$("altitude").textContent=height+" м";rocket.style.transform=`translateY(-${Math.min(height/3,85)}px) rotate(-8deg)`;
if(Date.now()-start>=3000){clearInterval(timer);const reward=Math.round((30+Math.floor(height/12))*(1+data.boost*.1));data.points+=reward;data.best=Math.max(data.best,height);$("rocketText").textContent=`Полёт завершён! Ты набрал ${height} м и получил +${reward} очков.`;button.disabled=false;button.textContent="ЗАПУСТИТЬ ЕЩЁ РАЗ";rocket.style.transform="";$("altitude").textContent=height+" м";flying=false;save();if(tg?.HapticFeedback)tg.HapticFeedback.notificationOccurred("success")}
},180);
});
document.querySelectorAll(".case-open").forEach(btn=>btn.addEventListener("click",()=>{
const name=btn.dataset.name;if(data.opened.includes(name))return;
data.opened.push(name);data.points+=Number(btn.dataset.reward);$("caseNote").textContent=`Кейс «${name}» открыт: +${btn.dataset.reward} очков!`;save();
}));
$("boostBuy").addEventListener("click",()=>{if(data.points<100||data.boost>=5)return;data.boost++;save()});
$("shieldBuy").addEventListener("click",()=>{if(data.points<50||data.shield>=1)return;data.shield=1;save();$("rocketIcon").textContent="🛡️🚀"});
render();
