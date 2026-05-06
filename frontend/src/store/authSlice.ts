import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const TOKEN_KEY = "clinic_app_access_token";

function readStoredToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (err) {
    console.warn("Could not read stored session token from localStorage", err);
    return null;
  }
}

type AuthState = {
  accessToken: string | null;
};

const initialState: AuthState = {
  accessToken: readStoredToken(),
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials(state, action: PayloadAction<string | null>) {
      state.accessToken = action.payload;
      try {
        if (action.payload) {
          localStorage.setItem(TOKEN_KEY, action.payload);
        } else {
          localStorage.removeItem(TOKEN_KEY);
        }
      } catch (err) {
        console.warn("Could not persist session token to localStorage", err);
      }
    },
  },
});

export const { setCredentials } = authSlice.actions;
export default authSlice.reducer;
