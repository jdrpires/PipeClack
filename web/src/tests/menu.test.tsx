import { render, screen } from '@testing-library/react'
import Dashboard from '../pages/Dashboard'
import { useAuth } from '../stores/auth'

it('menus shown based on role', () => {
  useAuth.setState({user:{id:1,name:'c',roles:['COMMERCIAL']}})
  render(<Dashboard />)
  expect(screen.queryByText('Comercial')).toBeInTheDocument()
  expect(screen.queryByText('Desenvolvimento')).not.toBeInTheDocument()
})
