import React,{useState}from'react';import{login}from'../api/auth';
export default function LoginPage(){
const[u,setU]=useState('');const[p,setP]=useState('');const[m,setM]=useState('');
async function s(e){e.preventDefault();try{const d=await login(u,p);localStorage.setItem('token',d.access_token);
const r=d.roles||[];if(r.includes('admin')){window.location='/admin';return;}
if(r.includes('approver')){window.location='/approver';return;}window.location='/creator';}
catch(err){setM('Login failed');}}
return(<div style={{maxWidth:420,margin:'40px auto',fontFamily:'sans-serif'}}><h2>Login</h2>
<form onSubmit={s}><input placeholder='username'value={u}onChange={e=>setU(e.target.value)}style={{display:'block',width:'100%',marginBottom:8,padding:8}}/>
<input type='password'placeholder='password'value={p}onChange={e=>setP(e.target.value)}style={{display:'block',width:'100%',marginBottom:8,padding:8}}/>
<button type='submit'style={{padding:'8px 16px'}}>Login</button></form>{m&&<p style={{color:'red'}}>{m}</p>}</div>)}