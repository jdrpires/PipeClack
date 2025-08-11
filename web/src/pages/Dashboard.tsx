import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../stores/auth'

export default function Dashboard(){
  const user = useAuth(s=>s.user)
  return (
    <div className="p-4">
      <h1>Dashboard</h1>
      <nav className="flex flex-col gap-2">
        {(user?.roles.includes('ADMIN') || user?.roles.includes('COMMERCIAL')) && <Link to="/board/commercial">Comercial</Link>}
        {(user?.roles.includes('ADMIN') || user?.roles.includes('PO') || user?.roles.includes('DEV') || user?.roles.includes('QA')) && <Link to="/board/dev">Desenvolvimento</Link>}
        {(user?.roles.includes('ADMIN') || user?.roles.includes('PO')) && <Link to="/discovery">Discovery</Link>}
      </nav>
    </div>
  )
}
