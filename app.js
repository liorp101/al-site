// ===== LEAD CAPTURE =====
// Each lead is POSTed to FormSubmit (AJAX) -> emailed to office@a-l-service.com, BEFORE WhatsApp opens,
// so it is saved even if the customer never presses "send" in WhatsApp.
// One-time: the first submission makes FormSubmit send an activation email to office@ — click "Activate".
// To switch to a DB later (Supabase etc.) just change LEAD_ENDPOINT.
const LEAD_ENDPOINT = "https://formsubmit.co/ajax/office@a-l-service.com";
const WA = "972549395950";
function storeLead(lead){
  if(!LEAD_ENDPOINT) return;
  try{ fetch(LEAD_ENDPOINT,{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(lead),keepalive:true}).catch(()=>{}); }catch(e){}
}
const phoneOk = p => /^(?:\+972|0)[\d -]{8,14}$/.test(p.trim());
const T={he:{tow:s=>`שלום א.ל שירותי תעבורה, אבקש לתאם ${s}.`,and:" ו",towing:"גרירה",rescue:"חילוץ",name:"שם איש קשר",phone:"טלפון לחזרה",veh:"סוג רכב",loc:"מיקום הרכב",dest:"יעד הגרירה המבוקש",det:"פרטים נוספים",end:"אשמח לאישור זמינות, מחיר ותיאום הגעה.",fault:"שלום א.ל שירותי תעבורה, יש לי תקלה ברכב.",model:"יצרן ודגם",desc:"תיאור התקלה"},
 ar:{tow:s=>`مرحبًا أ.ل لخدمات النقل، أطلب تنسيق ${s}.`,and:" و",towing:"قَطر",rescue:"إنقاذ",name:"اسم جهة الاتصال",phone:"هاتف للرد",veh:"نوع المركبة",loc:"موقع المركبة",dest:"وجهة القَطر المطلوبة",det:"تفاصيل إضافية",end:"أرجو تأكيد التوفر والسعر وتنسيق الوصول.",fault:"مرحبًا أ.ل لخدمات النقل، لديّ عطل في المركبة.",model:"الشركة المصنّعة والطراز",desc:"وصف العطل"}};
document.querySelectorAll("form[data-lead]").forEach(f=>f.addEventListener("submit",e=>{
  e.preventDefault(); const d=Object.fromEntries(new FormData(f)); const err=f.querySelector(".err"); const type=f.dataset.lead; const t=T[f.dataset.lang||"he"];
  if(d._honey) return;
  if(type==="towing" && !d.towing && !d.rescue) return err.textContent=err.dataset.e1;
  if(!f.checkValidity() || !phoneOk(d.phone||"")) return err.textContent=err.dataset.e2;
  err.textContent="";
  let lines;
  if(type==="towing"){ const s=[d.towing?t.towing:"",d.rescue?t.rescue:""].filter(Boolean).join(t.and);
    lines=[t.tow(s),`${t.name}: ${d.name}`,`${t.phone}: ${d.phone}`,`${t.veh}: ${d.vehicle}`,`${t.loc}: ${d.location}`,d.destination&&`${t.dest}: ${d.destination}`,d.details&&`${t.det}: ${d.details}`,t.end];
  } else lines=[t.fault,`${t.name}: ${d.name}`,`${t.phone}: ${d.phone}`,`${t.veh}: ${d.vehicle}`,d.model&&`${t.model}: ${d.model}`,`${t.desc}: ${d.details}`];
  const text=lines.filter(Boolean).join("\n");
  const {consent,_honey,...clean}=d;
  storeLead({_subject:`פנייה חדשה מהאתר – ${type==="towing"?"גרירה/חילוץ":"תקלה"} – ${d.name}`,_template:"table",_captcha:"false",type,...clean,lang:f.dataset.lang,page:location.pathname,created_at:new Date().toISOString(),message:text});
  window.open(`https://wa.me/${WA}?text=${encodeURIComponent(text)}`,"_blank","noopener");
}));
