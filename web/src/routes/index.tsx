import React from 'react'
import { Routes, Route } from 'react-router-dom'
import ProtectedRoute from '../components/ProtectedRoute'
import Login from '../pages/Login'
import Dashboard from '../pages/Dashboard'
import Kanban from '../pages/Kanban'
import Discovery from '../pages/Discovery'
import Forbidden from '../pages/Forbidden'

export default function AppRoutes(){
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<ProtectedRoute element={<Dashboard />} />} />
      <Route path="/board/dev" element={<ProtectedRoute roles={['ADMIN','PO','DEV','QA']} element={<Kanban type="DEV" />} />} />
      <Route path="/board/commercial" element={<ProtectedRoute roles={['ADMIN','COMMERCIAL']} element={<Kanban type="COMERCIAL" />} />} />
      <Route path="/discovery" element={<ProtectedRoute roles={['ADMIN','PO']} element={<Discovery />} />} />
      <Route path="/403" element={<Forbidden />} />
    </Routes>
  )
}
