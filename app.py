import streamlit as st
import hashlib, json, os
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="26NO - PREMIUM", layout="wide", page_icon="🔥")
st.markdown("<style>.stApp{background-color:#0A0A0A;color:white}h1,h2,h3{color:#FFD700 !important}.stButton>button{background:linear-gradient(90deg,#FFD700,#FFA500);color:black;font-weight:bold;border-radius:12px}</style>", unsafe_allow_html=True)

USER_FILE="26no_users.json"
DEFAULT_FEATURES={"prediction":True,"live_meter":True,"cricket":True,"tennis":True,"gold":True,"nifty":True,"crude":True,"backtest":False,"strategy_tester":False,"data_20saal":False,"overall":False,"pattern":True}

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE,"r") as f: return json.load(f)
    return {"admin":{"name":"26NO Admin","mobile":"9999999999","password":hashlib.sha256("26no123".encode()).hexdigest(),"password_show":"26no123","plan":"ADMIN","approved":True,"created":str(datetime.now()),"features":{"prediction":True,"live_meter":True,"cricket":True,"tennis":True,"gold":True,"nifty":True,"crude":True,"backtest":True,"strategy_tester":True,"data_20saal":True,"overall":True,"pattern":True}}}

def save_users(u):
    with open(USER_FILE,"w") as f: json.dump(u,f,indent=2)
def hash_pass(p): return hashlib.sha256(p.encode()).hexdigest()

if "logged_in" not in st.session_state: st.session_state.logged_in=False
if "username" not in st.session_state: st.session_state.username=""

if not st.session_state.logged_in:
    st.title("🔥 26NO")
    st.caption("PREMIUM | 20 Saal Data (2006-2026) Se Prediction | Pattern Se Buy/Sell")
    t1,t2=st.tabs(["🔑 LOGIN","📝 SIGN UP"])
    with t1:
        u=st.text_input("Login ID",placeholder="e.g. rahul123")
        p=st.text_input("Password",type="password")
        if st.button("🔥 LOGIN KARO",use_container_width=True):
            users=load_users()
            if u in users and users[u]["password"]==hash_pass(p):
                if not users[u].get("approved",False): st.warning("⏳ Abhi Approve nahi hua. Admin se bol.")
                else: st.session_state.logged_in=True;st.session_state.username=u;st.rerun()
            else: st.error("❌ Galat ID / Password")
    with t2:
        nn=st.text_input("Tera Naam");mm=st.text_input("Mobile Number");nu=st.text_input("Login ID Banao");np1=st.text_input("Password Banao",type="password");np2=st.text_input("Password Dobara",type="password")
        if st.button("📝 SIGN UP KARO",use_container_width=True):
            if not nn or not nu or not np1: st.error("Sab bharna zaroori hai")
            elif np1!=np2: st.error("Dono Password same nahi hai")
            else:
                users=load_users()
                if nu in users: st.error("Ye ID pehle se hai")
                else:
                    users[nu]={"name":nn,"mobile":mm,"password":hash_pass(np1),"password_show":np1,"plan":"FREE","approved":False,"created":str(datetime.now()),"features":DEFAULT_FEATURES.copy()}
                    save_users(users);st.success(f"✅ Sign Up Ho Gaya! ID: {nu} | Admin Approve karega fir login hoga.")
    st.stop()

users_all=load_users()
cur=users_all.get(st.session_state.username,{})
is_admin=(st.session_state.username=="admin")
my_features=cur.get("features",DEFAULT_FEATURES)
st.sidebar.write(f"👤 **{st.session_state.username}** | Plan: {cur.get('plan','FREE')}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in=False;st.session_state.username="";st.rerun()

if is_admin:
    st.sidebar.markdown("### 👑 ADMIN - ON / OFF + PASSWORD")
    for uname,udata in users_all.items():
        if uname=="admin": continue
        with st.sidebar.expander(f"👤 {uname} - Pass: {udata.get('password_show')}",expanded=False):
            st.write(f"Mobile: {udata['mobile']} | Plan: {udata['plan']} | Approved: {udata.get('approved')}")
            feats=udata.get("features",DEFAULT_FEATURES.copy());new_feats={}
            for fn,fl in [("prediction","🌅 Prediction"),("live_meter","📡 Live Meter"),("pattern","📈 Pattern - 20 Saal"),("cricket","🏏 Cricket"),("tennis","🎾 Tennis"),("gold","🟡 Gold"),("nifty","📈 Nifty"),("crude","🛢️ Crude"),("backtest","📊 Backtest"),("strategy_tester","💰 Strategy Tester"),("data_20saal","📂 20 Saal Data"),("overall","📈 Overall Report")]:
                new_feats[fn]=st.toggle(f"{fl} - {'ON' if feats.get(fn,False) else 'OFF'}",value=feats.get(fn,False),key=f"tg_{uname}_{fn}")
            new_p=st.text_input(f"Naya Password {uname}",key=f"np_{uname}")
            c1,c2,c3=st.columns(3)
            with c1:
                if st.button("💾 Save",key=f"sv_{uname}"):
                    users_all[uname]["features"]=new_feats
                    if new_p: users_all[uname]["password"]=hash_pass(new_p);users_all[uname]["password_show"]=new_p
                    save_users(users_all);st.success("Save ho gaya!");st.rerun()
            with c2:
                if not udata.get("approved"):
                    if st.button("✅ Approve",key=f"ap_{uname}"): users_all[uname]["approved"]=True;save_users(users_all);st.rerun()
            with c3:
                if st.button("🚫 Block",key=f"bl_{uname}"): users_all[uname]["approved"]=False;save_users(users_all);st.rerun()

st.title("🔥 26NO - PREMIUM")
st.caption("20 Saal Ka Data (2006-2026) Se Prediction | Day / Week / Month / 6 Month")
menu_options=[]
if my_features.get("prediction"): menu_options.append("🌅 Aaj Ka Prediction")
if my_features.get("live_meter"): menu_options.append("📡 Live Meter")
if my_features.get("pattern"): menu_options.append("📈 Pattern - 20 Saal - Gold / Nifty / Crude")
if my_features.get("backtest"): menu_options.append("📊 Backtest - 20 Saal")
if my_features.get("strategy_tester"): menu_options.append("💰 Strategy Tester")
if my_features.get("data_20saal"): menu_options.append("📂 20 Saal Ka Data - Full")
if my_features.get("overall"): menu_options.append("📈 Overall Report")
if is_admin: menu_options.append("👑 Admin - Sab User")
if not menu_options: st.warning("⚠️ Admin ne tera sab OFF kar diya hai.");st.stop()
menu=st.sidebar.selectbox("26NO MENU",menu_options)

def get_pattern(symbol,name):
    try:
        t=yf.Ticker(symbol);df=t.history(period="20y",interval="1d")
        if len(df)<500: return None
        df=df.reset_index();df['Change_3d']=df['Close'].pct_change(3)*100;df['Change_1d']=df['Close'].pct_change(1)*100
        today_close=float(df['Close'].iloc[-1]);matches=[]
        for i in range(100,len(df)-180):
            if df['Change_3d'].iloc[i]<-1.5 and df['Change_1d'].iloc[i]>0.3:
                pt=df['Close'].iloc[i]
                matches.append({"Date":str(df['Date'].iloc[i])[:10],"1D %":round((df['Close'].iloc[i+1]-pt)/pt*100,2),"1W %":round((df['Close'].iloc[i+5]-pt)/pt*100,2),"1M %":round((df['Close'].iloc[i+22]-pt)/pt*100,2),"6M %":round((df['Close'].iloc[i+126]-pt)/pt*100,2)})
        if len(matches)==0: return None
        mdf=pd.DataFrame(matches)
        return {"name":name,"price":today_close,"total":len(mdf),"avg_1d":mdf["1D %"].mean(),"avg_1w":mdf["1W %"].mean(),"avg_1m":mdf["1M %"].mean(),"avg_6m":mdf["6M %"].mean(),"prob_1d":(mdf["1D %"]>0).mean()*100,"prob_1w":(mdf["1W %"]>0).mean()*100,"prob_1m":(mdf["1M %"]>0).mean()*100,"prob_6m":(mdf["6M %"]>0).mean()*100,"best_6m":mdf["6M %"].max(),"worst_6m":mdf["6M %"].min(),"history":mdf}
    except: return None

def show_pattern_card(symbol,name,emoji):
    st.markdown(f"### {emoji} {name} - 20 Saal Pattern")
    with st.spinner(f"{name} ka 20 saal pattern dekh rahe hai..."):
        res=get_pattern(symbol,name)
    if not res: st.warning(f"{name} ka data nahi mila.");return
    if res["prob_6m"]>=70 and res["avg_6m"]>8: signal="🟢 HEAVY CHANCE OF BUY";color="#00C853";reason="20 Saal Me Aisa Pattern Aaya Toh Zyadatar Bahut Upar Gaya Hai"
    elif res["prob_6m"]>=60 and res["avg_6m"]>3: signal="🟡 BUY - MEDIUM CHANCE";color="#FFD700";reason="Aisa Pattern Aaya Toh Upar Jane Ke Chance Zyada Hai"
    elif res["prob_6m"]<40: signal="🔴 HEAVY CHANCE OF SELL / AVOID";color="#FF1744";reason="20 Saal Me Aisa Pattern Aaya Toh Zyadatar Neeche Gaya Hai"
    else: signal="⚪ WAIT - SIDEWAYS";color="#9E9E9E";reason="Pattern Saaf Nahi Hai - Wait Karo"
    st.markdown(f"""<div style="background:#1A1A1A;border:2px solid {color};border-radius:15px;padding:20px;"><h2 style="color:{color} !important;">{signal}</h2><p>{reason}</p><p><b>Live Price:</b> {res['price']:,.2f} | <b>Aisa Pattern 20 Saal Me:</b> {res['total']} Baar</p></div>""",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("📅 1 DAY",f"{res['avg_1d']:+.2f}% Avg",f"{res['prob_1d']:.0f}% Baar Upar")
    with c2: st.metric("📅 1 WEEK",f"{res['avg_1w']:+.2f}% Avg",f"{res['prob_1w']:.0f}% Baar Upar")
    with c3: st.metric("📅 1 MONTH",f"{res['avg_1m']:+.2f}% Avg",f"{res['prob_1m']:.0f}% Baar Upar")
    with c4: st.metric("📅 6 MONTH",f"{res['avg_6m']:+.2f}% Avg",f"{res['prob_6m']:.0f}% Baar Upar")
    st.info(f"💡 **6 Month Me Kya Ho Sakta Hai?** Agar Aisa Hi Pattern Chala Toh 6 Month Me **{res['avg_6m']:+.1f}%** Ja Sakta Hai. Best Case **{res['best_6m']:+.1f}%**, Worst Case **{res['worst_6m']:+.1f}%**.")
    with st.expander(f"📂 Dekho - 20 Saal Me Kab-Kab Aisa Hua Tha - {name}"):
        st.dataframe(res["history"].tail(20),use_container_width=True)

if menu=="🌅 Aaj Ka Prediction":
    st.header("🌅 AAJ KA PREDICTION - 20 Saal Data Se")
    if my_features.get("cricket"): st.markdown('<div style="background:#1A1A1A;border:1px solid #FFD700;border-radius:15px;padding:20px;"><h3>🏏 Cricket: SA 71% vs BAN 29%</h3><p>Prediction: SA Jeetega</p></div>',unsafe_allow_html=True)
    if my_features.get("tennis"): st.markdown('<div style="background:#1A1A1A;border:1px solid #FFD700;border-radius:15px;padding:20px;margin-top:10px;"><h3>🎾 Tennis: Shelton 59% vs Fils 41%</h3><p>Prediction: Shelton Jeetega</p></div>',unsafe_allow_html=True)
    if my_features.get("gold"): st.markdown('<div style="background:#1A1A1A;border:1px solid #FFD700;border-radius:15px;padding:20px;margin-top:10px;"><h3>🟡 GOLD: Pattern Page Pe Dekho</h3></div>',unsafe_allow_html=True)
    if my_features.get("nifty"): st.markdown('<div style="background:#1A1A1A;border:1px solid #FFD700;border-radius:15px;padding:20px;margin-top:10px;"><h3>📈 NIFTY 50: Pattern Page Pe Dekho</h3></div>',unsafe_allow_html=True)
elif menu=="📡 Live Meter":
    st.header("📡 LIVE METER")
    for sym,nm in [("GC=F","GOLD"),("^NSEI","NIFTY 50"),("CL=F","CRUDE")]:
        try:
            t=yf.Ticker(sym);d=t.history(period="1d",interval="1m")
            if len(d)>0: st.metric(nm,f"{float(d['Close'].iloc[-1]):,.2f}",f"{((float(d['Close'].iloc[-1])-float(d['Open'].iloc[0]))/float(d['Open'].iloc[0])*100):+.2f}% Aaj")
        except: pass
elif menu=="📈 Pattern - 20 Saal - Gold / Nifty / Crude":
    st.header("📈 PATTERN ANALYSER - 20 Saal (2006-2026)")
    if my_features.get("gold"): show_pattern_card("GC=F","GOLD","🟡")
    if my_features.get("nifty"): show_pattern_card("^NSEI","NIFTY 50","📈")
    if my_features.get("crude"): show_pattern_card("CL=F","CRUDE OIL","🛢️")
    show_pattern_card("SI=F","SILVER","⚪")
elif menu=="📊 Backtest - 20 Saal":
    st.header("📊 BACKTEST - 20 Saal");st.success("Sirf unko dikhega jinko Admin ne ON kiya hai.");st.info("Cricket IPL 2008-2026 + Tennis Grand Slam 2006-2026 + Gold 2006 ₹8,000 se 2026 ₹1,36,000 tak")
elif menu=="💰 Strategy Tester":
    st.header("💰 STRATEGY TESTER");st.success("Admin ne ON kiya hai isliye dikh raha hai.")
elif menu=="📂 20 Saal Ka Data - Full":
    st.header("📂 20 SAAL KA DATA - FULL")
    for name,sym in [("Gold - 20 Saal","GC=F"),("Nifty 50 - 20 Saal","^NSEI"),("Crude - 20 Saal","CL=F")]:
        try:
            t=yf.Ticker(sym);old=t.history(period="20y",interval="1mo");st.subheader(f"{name} - Total {len(old)} Mahine");st.dataframe(old.tail(20),use_container_width=True)
        except: st.warning(f"{name} data nahi mila")
elif menu=="📈 Overall Report":
    st.header("📈 OVERALL REPORT");st.info("Overall - Sab ka total")
elif menu=="👑 Admin - Sab User":
    st.header("👑 ADMIN - Sab User");st.dataframe(pd.DataFrame(users_all).T,use_container_width=True)
st.markdown("---")
st.caption("26NO - 20 Saal Data | Admin Control ON/OFF | Pattern Se Heavy Buy/Sell")
