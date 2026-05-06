import { configureStore } from "@reduxjs/toolkit";

import authReducer from "@/store/authSlice";
import { authApi } from "@/services/authApi";
import { patientsApi } from "@/services/patientsApi";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    [patientsApi.reducerPath]: patientsApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(authApi.middleware, patientsApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
