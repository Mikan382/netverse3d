import { apiRequest } from './api-request.ts';

const BASE = '/api/identity/v1';

type TokenPair = { accessToken: string; refreshToken: string; expiresIn: number };
export type AccountProfile = { id: string; email: string | null; displayName: string | null };

function request<T>(path: string, body?: object, accessToken?: string): Promise<T> {
  return apiRequest(`${BASE}/${path}`, { body, accessToken });
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
