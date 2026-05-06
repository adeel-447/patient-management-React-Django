import { useDispatch, useSelector } from "react-redux";

import type { AppDispatch, RootState } from "@/store/store";
import { setCredentials } from "@/store/authSlice";

export function useAuthSession() {
  const dispatch = useDispatch<AppDispatch>();
  const token = useSelector((s: RootState) => s.auth.accessToken);

  const logout = () => {
    dispatch(setCredentials(null));
  };

  return { token, logout };
}
