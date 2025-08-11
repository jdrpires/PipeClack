import { render, screen, fireEvent } from '@testing-library/react'
import Discovery from '../pages/Discovery'
import { vi } from 'vitest'
import api from '../services/api'
vi.mock('../services/api')

it('renders discovery form and submits', async () => {
  ;(api.get as any).mockResolvedValue({data:{id:1, sections:[{key:'a', label:'A', type:'text'}]}})
  ;(api.post as any).mockResolvedValue({data:{}})
  render(<Discovery />)
  const input = await screen.findByLabelText('A')
  fireEvent.change(input,{target:{value:'x'}})
  fireEvent.click(screen.getByText('Salvar'))
  expect(api.post).toHaveBeenCalled()
})
