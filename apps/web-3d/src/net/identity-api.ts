const BASE = '/api/identity/v1';

type TokenPair = { accessToken: string; refreshToken: string; expiresIn: number };
export type AccountProfile = { id: string; email: string | null; displayName: string | null };

export class IdentityError extends Error {
  constructor(readonly code: string) {
    super(code);
  }
}

async function request<T>(path: string, body?: object, accessToken?: string): Promise<T> {
  const response = await fetch(`${BASE}/${path}`, {
    method: body ? 'POST' : 'GET',
    headers: {
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
    cache: 'no-store',
    redirect: 'error',
    signal: AbortSignal.timeout(15000),
  }).catch(() => {
    throw new IdentityError('CLIENT.UNAVAILABLE');
  });
  const envelope = (await response.json().catch(() => null)) as {
    code?: string;
    result?: T;
  } | null;
  if (!response.ok) {
    const fallback = response.status === 429 ? 'COMMON.RATE_LIMITED' : 'CLIENT.UNAVAILABLE';
    throw new IdentityError(envelope?.code ?? fallback);
  }
  if (envelope?.code !== 'SUCCESS' || envelope.result == null) {
    throw new IdentityError('CLIENT.UNAVAILABLE');
  }
  return envelope.result;
}

export const identityApi = {
  register: (email: string, password: string, displayName: string) =>
    request('auth/register', { email, password, ...(displayName ? { displayName } : {}) }),
  verify: (email: string, code: string) => request('auth/verify-email', { email, code }),
  resend: (email: string) => request('auth/resend-verification', { email }),
  login: (email: string, password: string) => request<TokenPair>('auth/login', { email, password }),
  forgot: (email: string) => request('auth/password/forgot', { email }),
  reset: (email: string, code: string, newPassword: string) =>
    request('auth/password/reset', { email, code, newPassword }),
  refresh: (refreshToken: string) => request<TokenPair>('auth/refresh', { refreshToken }),
  logout: (refreshToken: string) => request('auth/logout', { refreshToken }),
  profile: (accessToken: string) => request<AccountProfile>('me', undefined, accessToken),
};
