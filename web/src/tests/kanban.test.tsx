import { render, screen } from '@testing-library/react'
import Kanban from '../pages/Kanban'
import { vi } from 'vitest'
import api from '../services/api'
vi.mock('../services/api')

test('move card updates', async () => {
  ;(api.post as any).mockResolvedValue({data:{}})
  render(<Kanban type="DEV" />)
  ;(window as any).testMove(1,2)
  expect(api.post).toHaveBeenCalled()
  expect(screen.getByTestId('col-2')).toHaveTextContent('Task')
})
