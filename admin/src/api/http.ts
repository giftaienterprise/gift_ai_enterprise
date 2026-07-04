export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

type ApiEnvelope<T> = {
  code: number
  message: string
  data: T
}

function isEnvelope(value: unknown): value is ApiEnvelope<unknown> {
  return (
    typeof value === 'object' &&
    value !== null &&
    'code' in value &&
    'message' in value &&
    'data' in value
  )
}

export type ApiRequestOptions = RequestInit & {
  token?: string
}

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const { token, headers: initHeaders, ...init } = options
  const headers = new Headers(initHeaders)

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  if (!headers.has('Content-Type') && init.body && !(init.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  const response = await fetch(`/api${normalizedPath}`, {
    ...init,
    headers,
  })

  const contentType = response.headers.get('content-type') ?? ''
  const hasJson = contentType.includes('application/json')
  const body: unknown = hasJson ? await response.json() : null

  if (!response.ok) {
    const message =
      (isEnvelope(body) ? body.message : null) ??
      (typeof body === 'object' && body !== null && 'detail' in body
        ? String((body as { detail: unknown }).detail)
        : null) ??
      response.statusText
    throw new ApiError(response.status, message)
  }

  if (isEnvelope(body)) {
    if (body.code !== 200) {
      throw new ApiError(body.code, body.message)
    }
    return body.data as T
  }

  return body as T
}
