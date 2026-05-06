import { type FormEvent, useState } from "react";

import { Button } from "@/components/ui/Button";
import { useLoginMutation } from "@/services/authApi";

export function LoginForm() {
  const [username, setUsername] = useState("demo");
  const [password, setPassword] = useState("demo1234");
  const [login, { isLoading, error }] = useLoginMutation();

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await login({ username, password }).unwrap();
    } catch (err) {
      console.warn("Sign-in request failed", err);
    }
  };

  return (
    <main className="card narrow">
      <h2>Sign in</h2>
      <p className="muted small">
        Demo: <code>demo</code> / <code>demo1234</code> (after <code>seed_demo</code>).
      </p>
      <form className="form" onSubmit={onSubmit}>
        <label>
          Username
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />
        </label>
        {error && <p className="error">Invalid username or password.</p>}
        <Button type="submit" variant="primary" disabled={isLoading}>
          {isLoading ? "Signing in…" : "Sign in"}
        </Button>
      </form>
    </main>
  );
}
