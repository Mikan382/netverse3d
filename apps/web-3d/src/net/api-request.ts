export class ApiError extends Error {
  readonly code: string;

  constructor(code: string) {
    super(code);
    this.code = code;
  }
}

type Options = {
  method?: 'GET' | 'POST';
  body?: object;
  accessToken?: string;
  signal?: AbortSignal;
};

export async function apiRequest<T>(
  path: string,
  { body, accessToken, method = body ? 'POST' : 'GET', signal }: Options = {},
): Promise<T> {
  const timeout = AbortSignal.timeout(15000);
  const response = await fetch(path, {
    method,
    headers: {
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
    cache: 'no-store',
    redirect: 'error',
    signal: signal ? AbortSignal.any([signal, timeout]) : timeout,
  }).catch(() => {
    throw new ApiError('CLIENT.UNAVAILABLE');
  });
  const envelope = (await response.json().catch(() => null)) as {
    code?: string;
    result?: T;
  } | null;
  if (!response.ok) {
    const fallback = response.status === 429 ? 'COMMON.RATE_LIMITED' : 'CLIENT.UNAVAILABLE';
    throw new ApiError(envelope?.code ?? fallback);
  }
  if (envelope?.code !== 'SUCCESS' || envelope.result == null) {
    throw new ApiError('CLIENT.UNAVAILABLE');
  }
  return envelope.result;
}
