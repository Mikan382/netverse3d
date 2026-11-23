import assert from 'node:assert/strict';
import type { IncomingMessage, ServerResponse } from 'node:http';

export const identityCalls: string[] = [];
const email = 'player@example.test';
const displayName = 'Người chơi thử';
const initialPassword = 'test-password-1';
let password = initialPassword;
let verified = false;
let generation = 0;
let refreshToken = '';

function tokens() {
  generation += 1;
  refreshToken = `browser-test-refresh-${generation}`;
  return {
    refreshToken,
    accessToken: `browser-test-access-${generation}`,
    expiresIn: generation === 1 ? 3 : 900,
  };
}

function success(response: ServerResponse, result: unknown = { accepted: true }) {
  response
    .writeHead(200, { 'Content-Type': 'application/json' })
    .end(JSON.stringify({ code: 'SUCCESS', result }));
}

function fail(response: ServerResponse, status: number, code: string) {
  response
    .writeHead(status, { 'Content-Type': 'application/json' })
    .end(JSON.stringify({ code, message: 'Fixture error' }));
}

export async function serveIdentityFixture(request: IncomingMessage, response: ServerResponse) {
  const path = request.url?.replace('/api/identity/v1/', '');
  identityCalls.push(path ?? '');
  try {
    if (path === 'me') {
      assert.equal(request.method, 'GET');
      assert.equal(request.headers.authorization, `Bearer browser-test-access-${generation}`);
      success(response, { id: 'test-player', email, displayName });
      return;
    }
    assert.equal(request.method, 'POST');
    let json = '';
    for await (const chunk of request) json += chunk;
    const body = JSON.parse(json);
    switch (path) {
      case 'auth/register':
        assert.deepEqual(body, { email, displayName, password: initialPassword });
        break;
      case 'auth/resend-verification':
      case 'auth/password/forgot':
        assert.deepEqual(body, { email });
        break;
      case 'auth/verify-email':
        assert.equal(body.email, email);
        if (body.code !== '091234') {
          fail(response, 400, 'IDENTITY.INVALID_OTP');
          return;
        }
        verified = true;
        break;
      case 'auth/login':
        if (!verified || body.email !== email || body.password !== password) {
          fail(response, 401, 'IDENTITY.INVALID_CREDENTIALS');
          return;
        }
        success(response, tokens());
        return;
      case 'auth/refresh':
        if (!refreshToken || body.refreshToken !== refreshToken) {
          fail(response, 401, 'IDENTITY.REFRESH_INVALID');
          return;
        }
        success(response, tokens());
        return;
      case 'auth/logout':
        assert.equal(body.refreshToken, refreshToken);
        refreshToken = '';
        break;
      case 'auth/password/reset':
        assert.deepEqual(body, { email, code: '004322', newPassword: 'test-password-2' });
        password = body.newPassword;
        refreshToken = '';
        break;
      default:
        throw new Error(`Unexpected route: ${path}`);
    }
    success(response);
  } catch (error) {
    response.writeHead(500).end(String(error));
  }
}
