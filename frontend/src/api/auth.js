export async function login(username, password){
  const API = process.env.REACT_APP_API_URL || '';
  const base = API || '';
  const res = await fetch(`${base}/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ username, password })
  });
  if(!res.ok) throw new Error('Login failed');
  return res.json();
}
