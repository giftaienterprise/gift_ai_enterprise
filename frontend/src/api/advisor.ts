import { agentRequest } from './http'

export type AgentRunResponse = {
  success: boolean
  goal: string
  user_id?: string
  plans?: unknown[]
  steps?: unknown[]
  final_answer?: string | null
  profile?: Record<string, unknown>
  compressed_memory?: Record<string, unknown>
  error?: string | null
}

export function runAdvisor(goal: string, token?: string) {
  return agentRequest<AgentRunResponse>('/run', {
    method: 'POST',
    body: JSON.stringify({ goal, use_brain: true }),
    token,
  })
}

export function buildAdvisorGoal(
  relationship: string,
  occasion: string,
  budget: string,
): string {
  return `为${relationship}挑选${occasion}礼物，预算${budget}`
}
