import React, { useState } from 'react';
import { login } from '../api/auth';

export default function LoginPage(){
  const [username,setUsername]=useState('');
  const [password,setPassword]=useState('');
  const [msg,setMsg]=useState('');

  async function submit(e){
    e.preventDefault();
    try{
      const data = await login(username, password);
      localStorage.setItem('token', data.access_token);
      const roles = data.roles || [];
      if(roles.includes('admin')){ window.location.href = '/admin'; return; }
      if(roles.includes('approver')){ window.location.href = '/approver'; return; }
      window.location.href = '/creator';
    }catch(err){
      setMsg('Login failed');
    }
  }

  return (
    <div style={{maxWidth:400,margin:'40px auto',fontFamily:'sans-serif'}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder='username' value={username} onChange={e=>setUsername(e.target.value)} style={{display:'block',width:'100%',marginBottom:8,padding:8}}/>
        <input type='password' placeholder='password' value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',width:'100%',marginBottom:8,padding:8}}/>
        <button type='submit' style={{padding:'8px 16px'}}>Login</button>
      </form>
      {msg && <p style={{color:'red'}}>{msg}</p>}
    </div>
  )
}
