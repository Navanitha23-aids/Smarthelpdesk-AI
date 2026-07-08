const SIDEBAR_CSS = `
.layout{display:flex;min-height:100vh;}
.sidebar{
  width:240px;flex-shrink:0;
  background:#0a0f1e;
  display:flex;flex-direction:column;
  padding:22px 14px;
  border-right:1px solid rgba(255,255,255,0.07);
  position:sticky;top:0;height:100vh;overflow-y:auto;
}
.sb-logo{
  display:flex;align-items:center;gap:10px;
  padding:0 8px 24px;
  border-bottom:1px solid rgba(255,255,255,0.07);
  margin-bottom:18px;
}
.sb-logo-box{
  width:36px;height:36px;
  background:linear-gradient(135deg,#00c6ff,#0072ff);
  border-radius:9px;display:flex;align-items:center;justify-content:center;
}
.sb-logo-box i{color:#fff;font-size:18px;}
.sb-logo span{font-size:14px;font-weight:700;color:#fff;line-height:1.2;}
.sb-nav{display:flex;flex-direction:column;gap:3px;flex:1;}
.sb-link{
  display:flex;align-items:center;gap:10px;
  padding:11px 12px;border-radius:10px;
  font-size:13px;font-weight:500;color:rgba(255,255,255,0.5);
  text-decoration:none;transition:all 0.2s;
}
.sb-link:hover{background:rgba(255,255,255,0.06);color:#fff;}
.sb-link.active{
  background:linear-gradient(135deg,rgba(0,198,255,0.15),rgba(0,114,255,0.15));
  color:#00c6ff;border:1px solid rgba(0,198,255,0.2);
}
.sb-link i{font-size:18px;}
.sb-section{
  font-size:10px;font-weight:700;letter-spacing:0.1em;
  text-transform:uppercase;color:rgba(255,255,255,0.25);
  padding:14px 12px 6px;
}
.sb-bottom{border-top:1px solid rgba(255,255,255,0.07);padding-top:14px;margin-top:8px;}
.sb-user{display:flex;align-items:center;gap:10px;margin-bottom:10px;padding:0 4px;}
.sb-avatar{
  width:34px;height:34px;border-radius:50%;
  background:linear-gradient(135deg,#7b2ff7,#0072ff);
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:700;color:#fff;flex-shrink:0;
}
.sb-uname{font-size:13px;font-weight:600;color:#fff;}
.sb-urole{font-size:11px;color:rgba(255,255,255,0.35);}
.sb-logout{
  display:flex;align-items:center;gap:8px;
  padding:10px 12px;border-radius:10px;
  font-size:13px;color:rgba(255,255,255,0.4);
  text-decoration:none;transition:all 0.2s;width:100%;
}
.sb-logout:hover{background:rgba(231,76,60,0.1);color:#e74c3c;}
.main{flex:1;background:#f0f4ff;overflow-y:auto;min-height:100vh;}
`;

const SIDEBAR_HTML = `
<aside class="sidebar" id="sidebar">
  <div class="sb-logo">
    <div class="sb-logo-box"><i class="ti ti-ticket"></i></div>
    <span>Smart Helpdesk AI</span>
  </div>
  <nav class="sb-nav">
    <div class="sb-section">Main</div>
    <a href="dashboard.html"  class="sb-link" data-page="dashboard"> <i class="ti ti-layout-dashboard"></i> Dashboard</a>
    <a href="create.html"     class="sb-link" data-page="create">    <i class="ti ti-plus"></i> Create Ticket</a>
    <a href="tickets.html"    class="sb-link" data-page="tickets">   <i class="ti ti-ticket"></i> My Tickets</a>
    <div class="sb-section">Support</div>
    <a href="helpcenter.html" class="sb-link" data-page="helpcenter"><i class="ti ti-help-circle"></i> Help Centre</a>
    <a href="history.html"    class="sb-link" data-page="history">   <i class="ti ti-history"></i> History</a>
  </nav>
  <div class="sb-bottom">
    <div class="sb-user">
      <div class="sb-avatar">AK</div>
      <div>
        <div class="sb-uname">Arjun Kumar</div>
        <div class="sb-urole">IT Employee</div>
      </div>
    </div>
    <a href="login.html" class="sb-logout"><i class="ti ti-logout"></i> Logout</a>
  </div>
</aside>`;

function initSidebar(activePage){
  document.head.insertAdjacentHTML('beforeend',`<style>${SIDEBAR_CSS}</style>`);
  const layout = document.getElementById('layout');
  layout.insertAdjacentHTML('afterbegin', SIDEBAR_HTML);
  document.querySelectorAll('.sb-link').forEach(l=>{
    if(l.dataset.page===activePage) l.classList.add('active');
  });
}
