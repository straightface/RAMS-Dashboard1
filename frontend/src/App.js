import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardAdmin from './pages/DashboardAdmin';
import DashboardCreator from './pages/DashboardCreator';
import DashboardApprover from './pages/DashboardApprover';

export default function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<LoginPage/>} />
        <Route path='/login' element={<LoginPage/>} />
        <Route path='/admin' element={<DashboardAdmin/>} />
        <Route path='/creator' element={<DashboardCreator/>} />
        <Route path='/approver' element={<DashboardApprover/>} />
      </Routes>
    </BrowserRouter>
  )
}
