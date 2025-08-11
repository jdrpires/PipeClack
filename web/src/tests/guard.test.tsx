import { render, screen } from '@testing-library/react'
import AppRoutes from '../routes'
import { MemoryRouter } from 'react-router-dom'
import { useAuth } from '../stores/auth'

it('commercial cannot access dev board', async () => {
  useAuth.setState({user:{id:1,name:'c',roles:['COMMERCIAL']}})
  render(
    <MemoryRouter initialEntries={['/board/dev']}>
      <AppRoutes />
    </MemoryRouter>
  )
  expect(await screen.findByText('403')).toBeInTheDocument()
})
