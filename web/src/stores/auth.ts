import { create } from 'zustand'
import api from '../services/api'

interface User { id:number; name:string; roles:string[] }
interface AuthState {
  user?: User
  token?: string
  login: (email:string, password:string)=>Promise<void>
  logout: ()=>void
}

export const useAuth = create<AuthState>((set)=>({
  user: undefined,
  token: undefined,
  login: async (email, password)=>{
    const res = await api.post('/auth/login', {email,password})
    const token = res.data.access_token
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    const me = await api.get('/auth/me')
    set({token, user: me.data})
  },
  logout: ()=>{ set({user:undefined, token:undefined}); delete api.defaults.headers.common['Authorization'] }
}))
